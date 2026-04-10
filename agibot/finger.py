import time
import numpy as np
from a2d_sdk.robot import Pose, RobotDds

def finger_recoil_test():
    rd = RobotDds()
    print(">>> 正在连接灵巧手，请确保 robot-service 已重启并显示绿灯...")
    time.sleep(2.0)

    # 你提供的完全张开状态基准
    OPEN_HAND_BASE = np.array([36, 200, 200, 200, 200, 1, 36, 200, 200, 200, 200, 1])/180*np.pi

    # 1. 获取当前位置
    res_init = rd.hand_joint_states()
    if not res_init or not res_init[0]:
        print("错误：无法读取手部状态。请检查机器端指示灯是否为绿色。")
        return
    
    start_hand = list(res_init[0])
    print(f"当前实时位姿: {start_hand}")

    try:
        # --- 阶段 0：强制复位到你提供的“完全张开”状态 ---
        # 这一步是为了冲刷掉之前可能存在的限位报错
        print("\n>>> 阶段 0：正在尝试强制复位到【完全张开】状态...")
        rd.move_hand(OPEN_HAND_BASE)
        time.sleep(3.0)

        # --- 阶段 1：收拢 (握拳) ---
        # 目标：四指(1-4)从 170+ 减小到 50，大拇指弯曲(5)从 0.99 增加到 40
        close_pose = np.array([30, 0, 0, 0, 0, 90, 30, 0, 0, 0, 0, 90]) /180*np.pi
        print(">>> 阶段 1：正在下发【收拢】指令 (大幅度动作)...")
        rd.move_hand(close_pose)
        
        # 等待动作完成
        time.sleep(4.0)
        res_closed = rd.hand_joint_states()
        mid_hand = list(res_closed[0]) if res_closed else start_hand

        # --- 阶段 2：再次张开 (回到你提供的基准) ---
        print(">>> 阶段 2：正在下发【张开】指令 (返回基准位)...")
        rd.move_hand(OPEN_HAND_BASE)
        
        time.sleep(3.0)
        res_final = rd.hand_joint_states()
        end_hand = list(res_final[0]) if res_final else mid_hand

        # --- 结果对比分析 ---
        print("\n" + "="*70)
        print(f"{'关节索引':<10} | {'初始':<7} | {'收拢位':<7} | {'最终回归':<7} | {'结论'}")
        print("-" * 70)
        
        labels = ["拇指旋", "食指弯", "中指弯", "无名弯", "小指弯", "拇指弯"]
        for i in range(6):
            # 以阶段1的收拢偏移量作为判断依据
            actual_move = abs(mid_hand[i] - start_hand[i])
            # 如果变动超过 5度，说明电机执行了指令
            status = "【OK】" if actual_move > 5.0 else "【静止】"
            
            print(f"{labels[i]:<8} ({i}) | {start_hand[i]:>6.1f} | {mid_hand[i]:>6.1f} | {end_hand[i]:>6.1f} | {status}")
        print("="*70)

    except Exception as e:
        print(f"运行出错: {e}")
    finally:
        print("\n测试结束。")
        rd.shutdown()

if __name__ == "__main__":
    finger_recoil_test()