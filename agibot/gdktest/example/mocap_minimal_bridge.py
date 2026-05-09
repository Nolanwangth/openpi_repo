#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
最小动捕 -> 机器人 GDK 桥接（仅 Python）。

做什么：
  - 用 rclpy 订阅 ROS2 话题 /remote/mocap_data（与 agibot/motion_cap/noitom_streamer 一致）
  - 用 a2d_sdk.robot.RobotDds 调用 move_head，把「名字里含 neck 的关节」姿态粗映射到头部两轴

不是什么：
  - 不是安全、也不是合理的全身映射；只证明「ROS 动捕数据能进 GDK」这一条链路。
  - 双臂请改用 RobotController + trajectory_tracking_control（见 motion_control 示例），工程量会明显变大。

运行前：
  1) 与 noitom_streamer 使用同一 ROS_DOMAIN_ID，且能收到 genie_msgs（source 你们机器人/遥控端的 overlay）。
  2) 已安装 a2d_sdk（与 gdktest 其它示例相同环境）。
  3) 动捕节点在发 /remote/mocap_data。

用法：
  python3 mocap_minimal_bridge.py
  Ctrl+C 退出。
"""
from __future__ import annotations

import math
import threading

import rclpy
from rclpy.executors import MultiThreadedExecutor
from rclpy.node import Node

try:
    from genie_msgs.msg import MocapData
except ImportError as e:
    raise SystemExit(
        "无法导入 genie_msgs.msg.MocapData。请先 source 包含 genie_msgs 的 ROS2 环境后再运行。\n"
        f"原始错误: {e}"
    ) from e

from a2d_sdk.robot import RobotDds


def quat_xyzw_to_euler_ypr(qx: float, qy: float, qz: float, qw: float) -> tuple[float, float, float]:
    """ZYX 顺序：yaw(Z) pitch(Y) roll(X)，与常见 Tait–Bryan 一致。"""
    sinp = 2.0 * (qw * qy - qz * qx)
    if abs(sinp) >= 1.0:
        pitch = math.copysign(math.pi / 2.0, sinp)
    else:
        pitch = math.asin(sinp)
    siny = 2.0 * (qw * qz + qx * qy)
    cosy = 1.0 - 2.0 * (qy * qy + qz * qz)
    yaw = math.atan2(siny, cosy)
    sinr = 2.0 * (qw * qx + qy * qz)
    cosr = 1.0 - 2.0 * (qx * qx + qy * qy)
    roll = math.atan2(sinr, cosr)
    return yaw, pitch, roll


def pick_neck_like_joint(msg: MocapData):
    for j in msg.mocap_joint_states:
        n = (j.name or "").lower()
        if "neck" in n or "head" in n:
            return j
    return None


class MocapMinimalBridge(Node):
    def __init__(self, robot: RobotDds) -> None:
        super().__init__("mocap_minimal_bridge")
        self._robot = robot
        self._lock = threading.Lock()
        self._last: MocapData | None = None
        self.create_subscription(MocapData, "/remote/mocap_data", self._on_mocap, 10)
        # 动捕可能 100Hz，头部指令不必这么高；10Hz 足够做最小验证
        self.create_timer(0.1, self._tick)

    def _on_mocap(self, msg: MocapData) -> None:
        with self._lock:
            self._last = msg

    def _tick(self) -> None:
        with self._lock:
            msg = self._last
        if msg is None:
            return
        j = pick_neck_like_joint(msg)
        if j is None:
            self.get_logger().warn_throttle(5.0, "消息里没有可识别的 neck/head 关节名，跳过")
            return
        q = j.orientation
        yaw, pitch, roll = quat_xyzw_to_euler_ypr(q.x, q.y, q.z, q.w)
        # 小增益 + 限幅（弧度）；若方向反了或轴对不上，只改这里即可
        gain = 0.2
        lim = 0.35
        h_yaw = max(-lim, min(lim, yaw * gain))
        h_pitch = max(-lim, min(lim, pitch * gain))
        # robot_control 示例里 move_head 使用弧度；两轴顺序若与现场相反，交换下面列表即可
        try:
            self._robot.move_head([h_yaw, h_pitch])
        except Exception as exc:  # noqa: BLE001 — 最小示例保留宽捕获打日志
            self.get_logger().error(f"move_head 失败: {exc}")


def main() -> None:
    rclpy.init()
    robot = RobotDds()
    node = MocapMinimalBridge(robot)
    execu = MultiThreadedExecutor(num_threads=4)
    execu.add_node(node)
    try:
        execu.spin()
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == "__main__":
    main()
