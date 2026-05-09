import time
import cv2
import threading
import numpy as np
from a2d_sdk.robot import CosineCamera as Camera

class AgibotCameraPro:
    def __init__(self, cam_name="hand_right"):
        self.cam_name = cam_name
        # 初始化相机组 [cite: 1282]
        self.camera = Camera([self.cam_name])
        self.latest_frame = None
        self.running = True
        self.lock = threading.Lock()
        
        # 官方建议：等待资源初始化 
        print(f"正在预热相机服务: {cam_name}...")
        time.sleep(2.0) 
        
        # 启动后台采集线程，确保 30Hz 不受主线程阻塞影响
        self.thread = threading.Thread(target=self._update_loop, daemon=True)
        self.thread.start()

    def _update_loop(self):
        """独立采集线程"""
        while self.running:
            # 实时图像获取 [cite: 1298]
            result = self.camera.get_latest_image(self.cam_name)
            
            if result is not None:
                # 图像数据为 numpy 数组 
                img, ts = result 
                with self.lock:
                    self.latest_frame = img
            
            # 官方默认帧率通常为 30Hz ，此处微调休眠确保稳定性
            time.sleep(0.01)

    def get_frame(self):
        with self.lock:
            return self.latest_frame

    def stop(self):
        self.running = False
        self.thread.join()
        self.camera.close() # 必须调用释放资源 

def run_optimized_test():
    cam_name = "hand_left"
    streamer = AgibotCameraPro(cam_name)
    
    cv2.namedWindow(f"Agibot G01 [{cam_name}]", cv2.WINDOW_NORMAL)
    
    last_log_time = time.time()
    frame_count = 0

    try:
        while True:
            start_time = time.time()
            
            img = streamer.get_frame()
            if img is None:
                continue

            frame_count += 1

            # ---------------- 极简预览逻辑 ----------------
            # 仅在需要预览时进行 copy 或处理，不干扰采集
            show_img = img.copy()
            
            # 每秒统计
            if time.time() - last_log_time >= 1.0:
                fps = frame_count / (time.time() - last_log_time)
                # 监控相机性能统计信息 [cite: 1309]
                sdk_fps = streamer.camera.get_fps(cam_name)
                print(f"[统计] 显示FPS: {fps:.1f} | SDK内部FPS: {sdk_fps}")
                frame_count = 0
                last_log_time = time.time()

            cv2.imshow(f"Agibot G01 [{cam_name}]", show_img)
            
            # 按 Q 退出
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

    finally:
        streamer.stop()
        cv2.destroyAllWindows()
        print("测试结束，资源已释放")

if __name__ == "__main__":
    run_optimized_test()