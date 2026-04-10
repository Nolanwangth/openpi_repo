import time
import sys
from a2d_sdk.robot import CosineCamera as Camera

def run_data_stress_test():
    cam_name = "head"
    cam_manager = None
    
    try:
        print(f"正在初始化相机服务: {cam_name} (30Hz 模式测试)...")
        cam_manager = Camera([cam_name])
        
        # 预热链路
        time.sleep(3) 

        print("-" * 50)
        print("开始纯数据流提取测试（不生成预览窗，减少干扰）")
        print("如果 FPS 稳定在 25-30 之间，说明对接 Pi0.5 的链路是完美的。")
        print("按 Ctrl+C 停止测试")
        print("-" * 50)

        frame_count = 0
        start_test_time = time.time()
        last_log_time = time.time()

        while True:
            # 1. 核心操作：尝试抓取当前最新的一帧
            result = cam_manager.get_latest_image(cam_name)
            
            if result is not None:
                img, ts = result
                if img is not None:
                    # 计数：成功拿到了一帧可以给模型用的 ndarray
                    frame_count += 1
                


                    
            # 2. 每隔 1 秒打印一次当前的实际接收效率
            current_time = time.time()
            if current_time - last_log_time >= 1.0:
                actual_fps = frame_count / (current_time - last_log_time)
                print(f"当前接收状态: 成功抓取帧数={frame_count}, 实时有效频率={actual_fps:.2f} Hz")

                print(f"数据类型: {type(img)}")
                print(f"图像维度 (Shape): {img.shape}") 
                print(f"数据总数 (Size): {img.size}")
                print(f"每个像素的数据类型: {img.dtype}")
                
                # 重置计数器
                frame_count = 0
                last_log_time = current_time

            # 3. 频率控制：30Hz 对应每帧间隔约 33ms
            # 我们稍微快一点点 (比如 30ms) 确保能把数据“抽干”
            time.sleep(0.03)

    except KeyboardInterrupt:
        print("\n测试由用户停止。")
    except Exception as e:
        print(f"运行出错: {e}")
    finally:
        if cam_manager is not None:
            cam_manager.close()
        print("资源已释放，测试结束。")

if __name__ == "__main__":
    run_data_stress_test()