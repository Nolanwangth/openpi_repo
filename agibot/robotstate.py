import time
import sys
from a2d_sdk.robot import RobotDds as Robot

# 1. 初始化机器人
robot = Robot()
print("\n" + "="*40)
print("  智元 G01 全机状态监控 (含完整单位说明)")
print("      按 Ctrl + C 退出读取")
print("="*40 + "\n")
time.sleep(1.0) 

try:
    while True:
        # 2. 获取状态数据
        arm_all, _ = robot.arm_joint_states()    
        hand_all, ts = robot.hand_joint_states() 
        head_pos, _ = robot.head_joint_states()  
        waist_pos, _ = robot.waist_joint_states() 

        # 3. 格式化输出
        print(f"--- 时间戳: {ts} ns ---")

        # 头部部分：SDK 内部通常已转为 Degree
        print(f"【头部 (Yaw/Pitch)】: {head_pos} (Degree)\n")

        # 腰部部分
        if waist_pos and len(waist_pos) == 2:
            print(f"【腰部状态】: 俯仰(Pitch)={waist_pos[0]:.4f} rad, 升降(Lift)={waist_pos[1]:.4f} m\n")
        else:
            print("【腰部数据】: 获取失败\n")

        # 手臂部分：7轴关节弧度
        if arm_all and len(arm_all) == 14:
            print(f"【左臂状态 (7轴)】: {arm_all[:7]} (rad)\n")
            print(f"【右臂状态 (7轴)】: {arm_all[7:]} (rad)\n")
        else:
            print("【手臂数据】: 获取失败\n")

        # 灵巧手部分
        if hand_all and any(h is not None for h in hand_all):
            print(f"【左手灵巧手】: {hand_all[:6]} (Pos/Deg)\n")
            print(f"【右手灵巧手】: {hand_all[6:]} (Pos/Deg)\n")
        else:
            gripper_all, _ = robot.gripper_states()
            print(f"【末端夹爪】: {gripper_all} (Pos)\n")

        print("-" * 50 + "\n")

        # 4. 设置更新频率
        time.sleep(1.0)

except KeyboardInterrupt:
    print("\n[通知] 用户中断，正在关闭连接...")
finally:
    # 5. 安全关闭
    robot.shutdown()
    sys.exit(0)