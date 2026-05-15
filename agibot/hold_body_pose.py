#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
#运行前
conda activate gdk_env
cd /home/nolan/vla/openpi_repo/agibot/a2d_sdk
source env.sh
cd ..
python3 hold_body_pose.py
"""
from __future__ import annotations
import math
import time
import sys
from typing import Optional
from a2d_sdk.robot import RobotDds
import numpy as np

# --- 用户配置区 ---
HZ = 100.0

HEAD_YAW_DEG = 0         #向右边看
HEAD_PITCH_DEG = 20       #低头
WAIST_PITCH_DEG = 25     #俯身
WAIST_LIFT_CM = 30       #升高
CHASSIS_LINEAR_X = 0     #向前速度
CHASSIS_ANGULAR_Z = 0    #顺时针旋转

# HEAD: [横摆 yaw, 俯仰 pitch] -> 单位：弧度 (rad) 
# PDF 范围：yaw -90°~90° (-1.57~1.57rad), pitch -25°~20° (-0.43~0.35rad) [cite: 435]
HEAD_TARGET: Optional[tuple[float, float]] = (HEAD_YAW_DEG*np.pi/180, HEAD_PITCH_DEG*np.pi/180) 

# WAIST: [俯仰 pitch, 升降 lift] 
# 注意：pitch 单位是弧度 (rad)，lift 单位是厘米 (cm)！！ 
# PDF 范围：pitch 0~90° (0~1.57rad), lift 0~50cm [cite: 440]
WAIST_TARGET: Optional[tuple[float, float]] = (WAIST_PITCH_DEG*np.pi/180, WAIST_LIFT_CM) 

# 底盘 move_wheel(linear, angular) —— PDF §7.2.1：线速度、角速度（与 §5.6 /mbc/wheel_command Twist 一致）
# linear：车体 x 方向线速度；angular：绕 z 轴角速度。置 0 表示不驱动平移/旋转（仍每周期刷新指令）
    
# ----------------

def main() -> None:
    # 初始化机器人连接 [cite: 927]
    r = RobotDds()
    
    # 根据文档建议，等待资源初始化 [cite: 928]
    print("正在初始化资源，请稍候...")
    time.sleep(1.0) 

    try:
        # 获取初始状态作为备份 [cite: 883, 884]
        h_feedback, _ = r.head_joint_states()
        w_feedback, _ = r.waist_joint_states()

        if not h_feedback or not w_feedback:
            print("错误：无法获取机器人反馈信息，请检查网络或电机状态。")
            return

        # 确定最终保持的目标位姿
        head = list(HEAD_TARGET) if HEAD_TARGET is not None else h_feedback
        waist = list(WAIST_TARGET) if WAIST_TARGET is not None else w_feedback

        print(f"开始保持姿态：")
        print(f" - 头部 (rad): {head}")
        print(f" - 腰部 (pitch_rad, lift_cm): {waist}")
        print(f" - 底盘 move_wheel(linear_x, angular_z): ({CHASSIS_LINEAR_X}, {CHASSIS_ANGULAR_Z})")
        print("按 Ctrl+C 停止并关闭连接。")

        dt = 1.0 / HZ
        while True:
            start_time = time.perf_counter()
            
            # 执行控制指令 [cite: 902]
            r.move_head(head)
            r.move_waist(waist)
            r.move_wheel(CHASSIS_LINEAR_X, CHASSIS_ANGULAR_Z)

            # 维持 30Hz 频率
            elapsed = time.perf_counter() - start_time
            time.sleep(max(0.0, dt - elapsed))

    except KeyboardInterrupt:
        print("\n检测到中断，正在安全关闭...")
    finally:
        # 必须调用 shutdown 释放资源 [cite: 920, 939]
        r.shutdown()
        print("已断开连接。")

if __name__ == "__main__":
    main()