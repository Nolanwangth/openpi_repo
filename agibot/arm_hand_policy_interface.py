"""30Hz 同步读臂/手关节状态并下发指令；下发前做限幅（手：readme 绝对限位；臂：相对当前反馈单步最大角）。

给策略 / PI05 下发的「合适」指令约定（与 a2d_sdk.move_arm / move_hand、finger.py 一致）：

- **手臂（14 维）**：单位 **弧度**，语义为**目标关节角**（绝对位置，不是增量）。
  接口会用当前 `arm_joint_states()` 做**单步限幅**（默认约 ±15°），避免阶跃触发软限位；
  因此即使 chunk 里目标跳变较大，真机也会**平滑地**往目标靠，看起来一直在动。

- **手指（12 维）**：单位 **弧度**，同样是**目标关节角**；顺序与 agibot/readme.md 一致：
  每只手 6 维：拇指旋、食指、中指、无名指、小指、拇指弯；先左手再右手。
  有效范围见 ``HAND_LO_RAD`` / ``HAND_HI_RAD``（由 readme 的度限位换算）。
  若训练或反归一化后数值仍在 **度**（例如四指约 100–176、幅值常 > 4），会先按度转成弧度再限幅。
  默认**不做**单步限幅；若策略输出在弧度空间正确但帧间跳变大，可对 ``ArmHand30Hz`` 传入
  ``max_hand_step_rad``，与手臂类似地平滑手指轨迹。
"""

from __future__ import annotations

import math
import time
from dataclasses import dataclass
from typing import Callable, Optional

import numpy as np
from a2d_sdk.robot import RobotDds

ARM_DOF, HAND_DOF = 14, 12
HZ = 30.0
MOCK_HAND_CYCLE_HZ = 0.12  # 张合周期约 1/0.12 ≈ 8.3s 一整趟
# 与 arm_vrmoods.py 一致：单周期指令相对当前关节角最大变化约 15°，降低超软限位/阶跃告警风险
MAX_ARM_STEP_RAD = 0.2618
# agibot/readme.md：拇指旋、食/中/无/小指、拇指弯（度）→ 左右手相同，共 12 维
_D2R = np.pi / 180.0
_H_MIN_D = np.array([2.2, 100.2, 97.8, 101.4, 98.8, 1.0], dtype=np.float64)
_H_MAX_D = np.array([36.75, 176.0, 173.8, 174.3, 172.6, 89.8], dtype=np.float64)
HAND_LO_RAD = np.concatenate([np.radians(_H_MIN_D), np.radians(_H_MIN_D)])
HAND_HI_RAD = np.concatenate([np.radians(_H_MAX_D), np.radians(_H_MAX_D)])
# 模拟轨迹：在 readme 边界内「伸（偏上限）↔ 弯（偏下限）」
_FINGER_OPEN_D = np.array([36.75, 176.0, 173.8, 174.3, 172.6, 1.0], dtype=np.float64)
_FINGER_CLOSE_D = np.array([2.2, 100.2, 97.8, 101.4, 98.8, 89.8], dtype=np.float64)
_FINGER_OPEN = np.concatenate([_FINGER_OPEN_D, _FINGER_OPEN_D]) * _D2R
_FINGER_CLOSE = np.concatenate([_FINGER_CLOSE_D, _FINGER_CLOSE_D]) * _D2R
# mock_cmd_stream：左右手各「拇指旋、拇指弯」共 4 维，与四指相反相位的 sin 插值
MOCK_THUMB_SIN_OPPOSITE_IDX = (0, 5, 6, 11)


@dataclass
class ArmHandState:
    arm_rad: list[float]
    hand_rad: list[float]  # 与 move_hand 一致：弧度（由 SDK 反馈的度转换）
    arm_ts_ns: int = 0
    hand_ts_ns: int = 0


def _as_cmd(x, n: int) -> list[float]:
    x = np.asarray(x, dtype=np.float64).reshape(-1)
    if x.size != n:
        raise ValueError(f"期望 {n} 维，得到 {x.size}")
    return x.tolist()


def _clamp_hand(hand: list[float]) -> list[float]:
    return np.clip(np.asarray(hand, float), HAND_LO_RAD, HAND_HI_RAD).tolist()


def _clamp_arm_step(arm: list[float], arm_now: list[float], max_step: float) -> list[float]:
    lo = np.asarray(arm_now, float) - max_step
    hi = np.asarray(arm_now, float) + max_step
    return np.clip(np.asarray(arm, float), lo, hi).tolist()


def _clamp_hand_step(hand: list[float], hand_now: list[float], max_step: float) -> list[float]:
    lo = np.asarray(hand_now, float) - max_step
    hi = np.asarray(hand_now, float) + max_step
    return np.clip(np.asarray(hand, float), lo, hi).tolist()


class ArmHand30Hz:
    def __init__(
        self,
        init_sleep_s: float = 0.5,
        *,
        max_arm_step_rad: float = MAX_ARM_STEP_RAD,
        max_hand_step_rad: float | None = None,
        clamp_hand: bool = True,
    ):
        self._r = RobotDds()
        self.max_arm_step_rad = max_arm_step_rad
        self.max_hand_step_rad = max_hand_step_rad
        self.clamp_hand = clamp_hand
        time.sleep(init_sleep_s)

    def read_state(self) -> ArmHandState:
        arm, ats = self._r.arm_joint_states()
        hp = self._r.hand_joint_states()
        if not arm or len(arm) != ARM_DOF:
            raise RuntimeError(f"arm_joint_states 无效: {arm!r}")
        if not hp or not hp[0] or len(hp[0]) != HAND_DOF:
            raise RuntimeError("hand_joint_states 无效（检查灵巧手与服务）")
        hts = int(hp[1]) if len(hp) > 1 and hp[1] is not None else 0
        # 反馈多为度（~100–200）；若已是弧度（量级小）则不再乘 π/180
        hand_raw = [float(x) for x in hp[0]]
        if max(abs(x) for x in hand_raw) > 20.0:
            hand_rad = [math.radians(d) for d in hand_raw]
        else:
            hand_rad = hand_raw
        return ArmHandState(
            [float(x) for x in arm],
            hand_rad,
            int(ats) if ats is not None else 0,
            hts,
        )

    def command(
        self,
        arm_rad,
        hand_rad,
        *,
        state: Optional[ArmHandState] = None,
    ) -> None:
        arm = _as_cmd(arm_rad, ARM_DOF)
        hand = _as_cmd(hand_rad, HAND_DOF)
        if state is not None:
            arm = _clamp_arm_step(arm, state.arm_rad, self.max_arm_step_rad)
            if self.max_hand_step_rad is not None:
                hand = _clamp_hand_step(hand, state.hand_rad, self.max_hand_step_rad)
        if self.clamp_hand:
            hand = _clamp_hand(hand)
        self._r.move_arm(arm)
        self._r.move_hand(np.asarray(hand, dtype=np.float64))

    def shutdown(self) -> None:
        self._r.shutdown()


def run_30hz(
    bot: ArmHand30Hz,
    cmd_fn: Callable[[ArmHandState, float], tuple[list[float], list[float]]],
    *,
    hz: float = HZ,
    max_steps: Optional[int] = None,
    duration_s: Optional[float] = None,
) -> None:
    """每周期：读状态 → cmd_fn(state, t_elapsed) → 下发；周期约 1/hz 秒。"""
    dt = 1.0 / hz
    t_wall0 = time.monotonic()
    k = 0
    while True:
        tic = time.monotonic()
        st = bot.read_state()
        arm, hand = cmd_fn(st, tic - t_wall0)
        bot.command(arm, hand, state=st)
        k += 1
        if max_steps is not None and k >= max_steps:
            break
        if duration_s is not None and (time.monotonic() - t_wall0) >= duration_s:
            break
        time.sleep(max(0.0, dt - (time.monotonic() - tic)))


def mock_cmd_stream(
    arm_amp_rad: float = 0.02,
    hand_cycle_hz: float = MOCK_HAND_CYCLE_HZ,
) -> Callable[[ArmHandState, float], tuple[list[float], list[float]]]:
    """参考 finger.py：双手在「完全张开」与「握拳」之间大幅插值；手臂小幅摆动。"""
    base_arm: Optional[list[float]] = None

    def fn(st: ArmHandState, t: float) -> tuple[list[float], list[float]]:
        nonlocal base_arm
        if base_arm is None:
            base_arm = st.arm_rad[:]
        wa = 2 * math.pi * 0.25
        arm = [base_arm[i] + arm_amp_rad * math.sin(wa * t + 0.1 * i) for i in range(ARM_DOF)]
        # u=0 → OPEN，u=1 → CLOSE，与 finger.py 两阶段一致
        u = 0.5 + 0.5 * math.sin(2 * math.pi * hand_cycle_hz * t)
        u_opp = 1.0 - u  # 反相 sin（拇指 4 维与四指张合节奏相反）
        hand = (1.0 - u) * _FINGER_OPEN + u * _FINGER_CLOSE
        for j in MOCK_THUMB_SIN_OPPOSITE_IDX:
            hand[j] = (1.0 - u_opp) * _FINGER_OPEN[j] + u_opp * _FINGER_CLOSE[j]
        return arm, hand.astype(np.float64).tolist()

    return fn


if __name__ == "__main__":
    bot = ArmHand30Hz()
    try:
        pol = mock_cmd_stream()
        tick = [0]

        def demo(st: ArmHandState, t: float) -> tuple[list[float], list[float]]:
            arm, hand = pol(st, t)
            tick[0] += 1
            if tick[0] % 30 == 1:
                u = 0.5 + 0.5 * math.sin(2 * math.pi * MOCK_HAND_CYCLE_HZ * t)
                print(
                    f"t={t:4.1f}s u={u:.2f}(0开1握) | arm[0]={arm[0]:.3f}rad | "
                    f"食指deg={math.degrees(hand[1]):.1f}"
                )
            return arm, hand

        run_30hz(bot, demo, hz=HZ, duration_s=20)
    except KeyboardInterrupt:
        pass
    finally:
        bot.shutdown()
