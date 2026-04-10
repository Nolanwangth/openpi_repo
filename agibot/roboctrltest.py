import time
import sys
from a2d_sdk.robot import RobotController, RobotDds

def run_arm_and_hand_test():
    # 1. 初始化接口
    rc = RobotController()
    rd = RobotDds()
    
    print("正在初始化硬件链路（手臂 + 灵巧手）...")
    time.sleep(2.0)

    try:
        # 2. 获取初始位姿作为基准
        res_arm = rd.arm_joint_states()
        res_hand = rd.hand_joint_states()
        
        if not res_arm or not res_hand:
            print("错误：无法获取关节状态。请检查机器及 env.sh 环境。")
            return
        
        start_arm = list(res_arm[0])
        start_hand = list(res_hand[0])
        
        print("成功获取初始位姿，开始构建联动轨迹 (14臂 + 12手指)...")

        # 3. 构建 50 步平滑序列 (模拟 Pi0.5 Action Chunking)
        mock_actions = []
        target_offset = 0.2 # 约 11.4 度，确保在安全限制内

        for i in range(50):
            progress = i / 50.0
            offset = target_offset * progress 
            
            # --- 左手臂动作 (7关节) ---
            left_arm_action = list(start_arm[:7])
            for j in range(7):
                # 联动：奇数关节正向，偶数关节负向，增加动感
                left_arm_action[j] += offset if j % 2 == 1 else -offset
            
            # --- 左手灵巧手动作 (6关节) ---
            # 索引 0-5 对应左手
            left_hand_action = list(start_hand[:6])
            for k in range(6):
                left_hand_action[k] -= offset*5  # 模拟握拳动作
            
            # 封装单步 Action
            action_step = {
                "left_arm": {
                    "action_data": left_arm_action,
                    "control_type": "ABS_JOINT"
                },
                "right_arm": {
                    "action_data": start_arm[7:14], # 右臂保持不动
                    "control_type": "ABS_JOINT"
                },
                "left_tool": {
                    "action_data": left_hand_action, # 控制左手手指
                    "control_type": "ABS_JOINT"
                },
                "right_tool": {
                    "action_data": start_hand[6:12], # 右手保持不动
                    "control_type": "ABS_JOINT"
                }
            }
            mock_actions.append(action_step)

        # 4. 下发轨迹
        print(">>> 下发轨迹：左臂整体移动 + 左手同步握拳...")
        ts_ns = int(time.time() * 1e9)
        rc.trajectory_tracking_control(
            infer_timestamp=ts_ns,
            robot_states={"arm": start_arm, "hand": start_hand}, 
            robot_actions=mock_actions,
            robot_link="base_link",
            trajectory_reference_time=2.0
        )

        # 5. 等待执行并获取最终状态计算差值
        time.sleep(4.5) 
        res_arm_end = rd.arm_joint_states()
        res_hand_end = rd.hand_joint_states()
        
        if res_arm_end and res_hand_end:
            end_arm = list(res_arm_end[0])
            end_hand = list(res_hand_end[0])
            
            print("\n" + "="*75)
            print(f"{'位置分类':<10} | {'索引':<4} | {'初始(rad)':<10} | {'最终(rad)':<10} | {'变化量(deg)'}")
            print("-" * 75)
            
            # 打印手臂 14 关节 (0-6左, 7-13右)
            for a in range(14):
                delta = end_arm[a] - start_arm[a]
                label = "左臂" if a < 7 else "右臂"
                print(f"{label:<10} | {a:<4} | {start_arm[a]:>10.4f} | {end_arm[a]:>10.4f} | {delta*57.3:>8.2f}°")
            
            print("-" * 75)
            
            # 打印手指 12 关节 (0-5左, 6-11右)
            for h in range(12):
                delta = end_hand[h] - start_hand[h]
                label = "左手指" if h < 6 else "右手指"
                print(f"{label:<10} | {h:<4} | {start_hand[h]:>10.4f} | {end_hand[h]:>10.4f} | {delta*57.3:>8.2f}°")
            print("="*75)

    except Exception as e:
        print(f"运行出错: {e}")
    finally:
        print("清理资源...")
        try:
            # 尝试将控制模式切回 STOP
            rc.set_control_mode(control_mode=0)
        except:
            pass
        rd.shutdown()

if __name__ == "__main__":
    run_arm_and_hand_test()