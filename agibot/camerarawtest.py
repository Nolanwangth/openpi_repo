import time
import cv2
import threading
import numpy as np
from a2d_sdk.robot import CosineCamera as Camera

# head：头部 RGB；head_center_fisheye：头部中央鱼眼（广角），见 GDK v1.5 PDF 5.5.1 /camera/head_center_fisheye
CAM_NAMES = ("head", "head_center_fisheye")
# 拉取 get_latest_image 与主循环刷新上限（Hz）
CAM_POLL_HZ = 30.0


def rgb_to_bgr_for_imshow(img: np.ndarray) -> np.ndarray:
    """CosineCamera 返回多为 RGB；cv2.imshow 按 BGR 显示，不转换则红蓝会颠倒。"""
    if img is None or img.ndim != 3:
        return img
    c = img.shape[2]
    if c == 3:
        return cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    if c == 4:
        return cv2.cvtColor(img, cv2.COLOR_RGBA2BGR)
    return img


class AgibotMultiCameraPro:
    def __init__(self, cam_names=CAM_NAMES):
        self.cam_names = list(cam_names)
        self.camera = Camera(self.cam_names)
        self.latest_frames = {n: None for n in self.cam_names}
        self.running = True
        self.lock = threading.Lock()

        print(f"正在预热相机服务: {', '.join(self.cam_names)}...")
        time.sleep(2.0)

        self.thread = threading.Thread(target=self._update_loop, daemon=True)
        self.thread.start()

    def _update_loop(self):
        period = 1.0 / CAM_POLL_HZ
        next_tick = time.perf_counter()
        while self.running:
            for name in self.cam_names:
                result = self.camera.get_latest_image(name)
                if result is not None:
                    img, _ts = result
                    with self.lock:
                        self.latest_frames[name] = img
            next_tick += period
            sleep_s = next_tick - time.perf_counter()
            if sleep_s > 0:
                time.sleep(sleep_s)
            else:
                next_tick = time.perf_counter()

    def get_frame(self, cam_name: str):
        with self.lock:
            return self.latest_frames.get(cam_name)

    def stop(self):
        self.running = False
        self.thread.join()
        self.camera.close()

    def window_title(self, cam_name: str) -> str:
        return f"Agibot G01 [{cam_name}]"


def run_optimized_test():
    streamer = AgibotMultiCameraPro(CAM_NAMES)

    for name in CAM_NAMES:
        cv2.namedWindow(streamer.window_title(name), cv2.WINDOW_NORMAL)

    last_log_time = time.time()
    frame_count = 0
    period = 1.0 / CAM_POLL_HZ
    next_tick = time.perf_counter()

    try:
        while True:
            frame_count += 1
            for name in CAM_NAMES:
                img = streamer.get_frame(name)
                if img is None:
                    continue
                show_img = rgb_to_bgr_for_imshow(img.copy())
                cv2.imshow(streamer.window_title(name), show_img)

            if time.time() - last_log_time >= 1.0:
                elapsed = time.time() - last_log_time
                fps = frame_count / elapsed
                sdk_parts = [
                    f"{n}={streamer.camera.get_fps(n):.1f}" for n in CAM_NAMES
                ]
                print(f"[统计] 主循环≈{fps:.1f} Hz | SDK FPS: " + ", ".join(sdk_parts))
                frame_count = 0
                last_log_time = time.time()

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

            next_tick += period
            sleep_s = next_tick - time.perf_counter()
            if sleep_s > 0:
                time.sleep(sleep_s)
            else:
                next_tick = time.perf_counter()

    finally:
        streamer.stop()
        cv2.destroyAllWindows()
        print("测试结束，资源已释放")


if __name__ == "__main__":
    run_optimized_test()
