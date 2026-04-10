import time
import sys
import numpy as np
from a2d_sdk.robot import RobotDds as Robot

def arm_movement_test():
    # 1. 初始化机器人
    robot = Robot()
    time.sleep(0.5)  # 等待资源初始化
    
    # 2. 获取初始状态并记录
    initial_pos, start_ts = robot.arm_joint_states()
    if not initial_pos or len(initial_pos) != 14:
        print("错误：无法获取初始手臂状态或关节数不匹配")
        return
    
    print(f"测试开始 - 初始位置: {[round(p, 4) for p in initial_pos]}")
    
    # 3. 规划 50 个 Timestep 的平滑轨迹
    # 设定一个微小的增量目标，确保每步不超过 0.2618 rad 的限位
    timesteps = 50
    step_increment = 0.005  # 每步增加 0.005 弧度 (约 0.28°)，远低于 15° 的安全阈值
    
    history = []
    current_target = np.array(initial_pos)
    
    try:
        for i in range(timesteps):
            # 计算下一个控制指令
            current_target = current_target + step_increment
            
            # 执行控制指令
            robot.move_arm(current_target.tolist())
            
            # 等待机器人响应（建议周期 10ms）
            time.sleep(0.05) 
            
            # 实时读取当前反馈状态用于后续标准对比
            feedback_pos, _ = robot.arm_joint_states()
            history.append({
                "step": i + 1,
                "command": current_target.tolist(),
                "feedback": feedback_pos
            })
            
        # 4. 对比前后控制是否标准
        print("\n" + "="*50)
        print("控制标准对比分析：")
        final_pos, end_ts = robot.arm_joint_states()
        
        # 计算指令与反馈的均方误差 (MSE)
        commands = np.array([h["command"] for h in history])
        feedbacks = np.array([h["feedback"] for h in history])
        mse = np.mean((commands - feedbacks)**2)
        
        print(f"1. 轨迹完整性: 完成 {len(history)}/{timesteps} 个时间步")
        print(f"2. 最终位置偏差 (Error): {np.linalg.norm(np.array(final_pos) - current_target):.6f} rad")
        print(f"3. 平均跟踪精度 (MSE): {mse:.6f}")
        
        if mse < 0.001:
            print("结论：控制表现【标准】。反馈高度贴合指令轨迹。")
        else:
            print("结论：控制存在偏离。请检查是否存在奇异点或负载过重。")
            
    except Exception as e:
        print(f"测试异常中断: {e}")
    finally:
        # 5. 释放资源
        robot.shutdown()
        print("机器人连接已关闭。")

if __name__ == "__main__":
    arm_movement_test()