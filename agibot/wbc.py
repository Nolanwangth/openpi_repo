#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
#运行前
conda activate gdk_env
cd /home/nolan/vla/openpi_repo/agibot/a2d_sdk
source env.sh
cd ..
python3 wbc.py

WBC 键盘遥控（底盘 + 头 + 腰）：30Hz ``move_wheel`` + ``move_head`` + ``move_waist``。

底盘（与 GDK ``move_wheel(linear, angular)`` 一致）
  w / s — 线速度 ±0.1  
  a / d — 角速度 ±3.0  
  松开为 0。

头部（绝对 yaw/pitch，弧度下发；用方向键以固定步长增量调节，便于测试）
  ← / → — yaw（手册：向左为正）← 为 yaw 增加，→ 为 yaw 减小  
  ↑ / ↓ — pitch（相对上一版已对调）：↑ 减小 pitch，↓ 增大 pitch
  启动时从 ``head_joint_states`` / ``waist_joint_states`` 读初值；GDK 刚连上时关节量可能短暂为 ``None``，脚本会轮询等待再进入主循环。

限幅（GDK v1.5.0 手册 §5.2）：yaw ∈ [-90°, 90°]，pitch ∈ [-25°, 20°]。

腰部（``move_waist([pitch_rad, lift_cm])``，与 ``hold_body_pose.py`` 一致；限幅 pitch ∈ [0°, 90°]，lift ∈ [0, 50] cm）
  Page Up / Page Down — 升降（物理上向上 / 向下）
  Home / End — 俯仰前倾 / 后仰（步长较小，便于微调）
  启动时从 ``waist_joint_states`` 读当前姿态为初值（与头部一致）；松键后保持最后一次目标。
  升降反馈在 GDK 侧常为 **米**（见仓库内 ``robotstate.py`` 注释），本脚本会换算为 **cm** 再与 ``move_waist`` 一致；启动时连读数帧以避开首包陈旧值。

退出：q 或 Ctrl+C。依赖 ``pip install pynput``。运行前 ``source agibot/a2d_sdk/env.sh``。
"""
from __future__ import annotations

import math
import sys
import termios
import threading
import time

try:
    from pynput import keyboard
except ImportError as e:
    raise SystemExit("需要：pip install pynput\n" + str(e)) from e

from a2d_sdk.robot import RobotDds

HZ = 30.0
LINEAR_W = 0.1
LINEAR_S = -0.1
ANGULAR_A = 3.0
ANGULAR_D = -3.0

# 按住方向键时每帧改变的角度（度），30Hz 下约 0.6°/帧 ≈ 18°/s
HEAD_STEP_DEG = 0.6

# 头部位姿限幅（弧度）
HEAD_YAW_MIN = math.radians(-90.0)
HEAD_YAW_MAX = math.radians(90.0)
HEAD_PITCH_MIN = math.radians(-25.0)
HEAD_PITCH_MAX = math.radians(20.0)

# 腰部：与 hold_body_pose.py / 手册一致 — pitch 弧度，lift 厘米
WAIST_PITCH_MIN = 0.0
WAIST_PITCH_MAX = math.radians(90.0)
WAIST_LIFT_MIN = 0.0
WAIST_LIFT_MAX = 50.0
# 俯仰每帧增量（度）：小于头部 0.6°，避免弧度指令下体感步长过大
WAIST_PITCH_STEP_DEG = 0.1
WAIST_STEP_CM = 0.2
# waist_joint_states 首包常滞后；连读若干帧再采用最后一次（与 HZ 对齐）
WAIST_FEEDBACK_WARMUP_FRAMES = 20
# head/waist 反馈在连接建立初期可能为 None，最长等待（秒）避免卡死无提示
SENSOR_FEEDBACK_WAIT_S = 12.0

INIT_SLEEP_S = 0.5


class _NoEcho:
    def __init__(self) -> None:
        self._fd = sys.stdin.fileno()
        self._old: list | None = None

    def __enter__(self) -> None:
        if not sys.stdin.isatty():
            return None
        self._old = termios.tcgetattr(self._fd)
        new = termios.tcgetattr(self._fd)
        new[3] &= ~termios.ECHO
        new[3] &= ~termios.ICANON
        termios.tcsetattr(self._fd, termios.TCSADRAIN, new)
        return None

    def __exit__(self, *args: object) -> None:
        if self._old is not None:
            termios.tcsetattr(self._fd, termios.TCSADRAIN, self._old)


def _head_feedback_to_rad(h0: float, h1: float) -> tuple[float, float]:
    if max(abs(h0), abs(h1)) > 6.5:
        return (math.radians(h0), math.radians(h1))
    return (float(h0), float(h1))


def _read_head_feedback(r: RobotDds) -> tuple[float, float]:
    h_fb, _ = r.head_joint_states()
    if not h_fb or len(h_fb) != 2 or h_fb[0] is None or h_fb[1] is None:
        raise RuntimeError("head_joint_states 未就绪")
    return _head_feedback_to_rad(float(h_fb[0]), float(h_fb[1]))


def _wait_head_feedback(r: RobotDds, listener: keyboard.Listener) -> tuple[float, float]:
    t0 = time.perf_counter()
    while time.perf_counter() - t0 < SENSOR_FEEDBACK_WAIT_S:
        try:
            return _read_head_feedback(r)
        except (RuntimeError, TypeError, ValueError):
            time.sleep(1.0 / HZ)
    listener.stop()
    raise RuntimeError(
        f"head_joint_states 在 {SENSOR_FEEDBACK_WAIT_S:.0f}s 内未就绪（yaw/pitch 仍为 None 或非数值），"
        "请检查机器人/DDS 或稍后再启动。"
    )


def _waist_pitch_feedback_to_rad(pitch_fb: float) -> float:
    """腰部 pitch 反馈：若为角度制（0~90 量级）则转弧度，否则视为弧度。"""
    if abs(pitch_fb) > 2.2:
        return math.radians(pitch_fb)
    return float(pitch_fb)


def _waist_lift_feedback_to_cm(lift_fb: float) -> float:
    """腰部升降反馈：SDK 常为米 (0~0.5)；``move_waist`` 第二维为 cm。已在 cm 量级的数原样保留。"""
    x = float(lift_fb)
    if 0.0 <= x <= 0.65:
        return x * 100.0
    return x


def _read_waist_feedback(r: RobotDds) -> tuple[float, float]:
    w_fb, _ = r.waist_joint_states()
    if not w_fb or len(w_fb) != 2 or w_fb[0] is None or w_fb[1] is None:
        raise RuntimeError("waist_joint_states 未就绪")
    p = _waist_pitch_feedback_to_rad(float(w_fb[0]))
    l = _waist_lift_feedback_to_cm(float(w_fb[1]))
    return p, l


def _key_tag(key: keyboard.Key | keyboard.KeyCode) -> str | None:
    if key == keyboard.Key.left:
        return "L"
    if key == keyboard.Key.right:
        return "R"
    if key == keyboard.Key.up:
        return "U"
    if key == keyboard.Key.down:
        return "D"
    if key == keyboard.Key.page_up:
        return "PU"
    if key == keyboard.Key.page_down:
        return "PD"
    if key == keyboard.Key.home:
        return "Hm"
    if key == keyboard.Key.end:
        return "En"
    ch = getattr(key, "char", None)
    if ch is not None:
        c = ch.lower()
        if c in "wsadq":
            return c
    return None


def main() -> None:
    pressed: set[str] = set()
    lock = threading.Lock()

    def on_press(key: keyboard.Key | keyboard.KeyCode) -> None:
        try:
            if key == keyboard.Key.esc:
                return
            t = _key_tag(key)
            if t is not None:
                with lock:
                    pressed.add(t)
        except Exception:
            pass

    def on_release(key: keyboard.Key | keyboard.KeyCode) -> None:
        try:
            t = _key_tag(key)
            if t is not None:
                with lock:
                    pressed.discard(t)
        except Exception:
            pass

    try:
        listener = keyboard.Listener(on_press=on_press, on_release=on_release, suppress=True)
    except TypeError:
        listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()

    r = RobotDds()
    print(
        "WBC 30Hz | w/s a/d 底盘 | ←/→/↑/↓ 头 yaw/pitch | q 退出",
        flush=True,
    )
    print(
        "腰部 | PgUp 升高 PgDn 降低 | Home 前倾 End 后仰（初值同头：来自关节反馈）",
        flush=True,
    )
    time.sleep(INIT_SLEEP_S)

    print("等待头部关节反馈就绪…", flush=True)
    yaw_rad, pitch_rad = _wait_head_feedback(r, listener)

    print("同步腰部关节反馈…", flush=True)
    waist_pitch_rad, waist_lift_cm = 0.0, 0.0
    good = 0
    t_w = time.perf_counter()
    while good < WAIST_FEEDBACK_WARMUP_FRAMES and time.perf_counter() - t_w < SENSOR_FEEDBACK_WAIT_S:
        if good > 0:
            time.sleep(1.0 / HZ)
        try:
            waist_pitch_rad, waist_lift_cm = _read_waist_feedback(r)
            good += 1
        except RuntimeError:
            time.sleep(1.0 / HZ)
    if good == 0:
        listener.stop()
        raise RuntimeError(
            f"waist_joint_states 在 {SENSOR_FEEDBACK_WAIT_S:.0f}s 内未就绪（含 None 或长度异常），"
            "请检查机器人/DDS 或稍后再启动。"
        )

    step = math.radians(HEAD_STEP_DEG)
    waist_pitch_step = math.radians(WAIST_PITCH_STEP_DEG)
    dt = 1.0 / HZ

    try:
        with _NoEcho():
            while True:
                tic = time.perf_counter()
                with lock:
                    want_quit = "q" in pressed
                    p = set(pressed)
                if want_quit:
                    break

                lin = 0.0
                if "w" in p and "s" not in p:
                    lin = LINEAR_W
                elif "s" in p and "w" not in p:
                    lin = LINEAR_S

                ang = 0.0
                if "a" in p and "d" not in p:
                    ang = ANGULAR_A
                elif "d" in p and "a" not in p:
                    ang = ANGULAR_D

                if "L" in p and "R" not in p:
                    yaw_rad += step
                elif "R" in p and "L" not in p:
                    yaw_rad -= step
                if "U" in p and "D" not in p:
                    pitch_rad -= step
                elif "D" in p and "U" not in p:
                    pitch_rad += step
                yaw_rad = max(HEAD_YAW_MIN, min(HEAD_YAW_MAX, yaw_rad))
                pitch_rad = max(HEAD_PITCH_MIN, min(HEAD_PITCH_MAX, pitch_rad))

                if "PU" in p and "PD" not in p:
                    waist_lift_cm += WAIST_STEP_CM
                elif "PD" in p and "PU" not in p:
                    waist_lift_cm -= WAIST_STEP_CM
                if "Hm" in p and "En" not in p:
                    waist_pitch_rad += waist_pitch_step
                elif "En" in p and "Hm" not in p:
                    waist_pitch_rad -= waist_pitch_step
                waist_pitch_rad = max(WAIST_PITCH_MIN, min(WAIST_PITCH_MAX, waist_pitch_rad))
                waist_lift_cm = max(WAIST_LIFT_MIN, min(WAIST_LIFT_MAX, waist_lift_cm))

                r.move_wheel(lin, ang)
                r.move_head([yaw_rad, pitch_rad])
                r.move_waist([waist_pitch_rad, waist_lift_cm])

                sys.stdout.write(
                    f"\r wheel({lin:+.2f},{ang:+.2f}) "
                    f"head_deg(y={math.degrees(yaw_rad):+.1f},p={math.degrees(pitch_rad):+.1f}) "
                    f"waist_deg(p={math.degrees(waist_pitch_rad):+.1f}),lift_cm={waist_lift_cm:+.1f}   "
                )
                sys.stdout.flush()

                time.sleep(max(0.0, dt - (time.perf_counter() - tic)))
    except KeyboardInterrupt:
        pass
    finally:
        sys.stdout.write("\r" + " " * 120 + "\r")
        sys.stdout.flush()
        try:
            r.move_wheel(0.0, 0.0)
        except Exception:
            pass
        try:
            r.shutdown()
        except Exception:
            pass
        listener.stop()
        print("已停止并断开。")


if __name__ == "__main__":
    main()
