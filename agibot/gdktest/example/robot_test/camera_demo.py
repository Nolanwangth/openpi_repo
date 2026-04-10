from a2d_sdk.robot import CosineCamera as Camera
# 初始化相机
import time
cameras = ["head", "hand_left","hand_right"]
camera = Camera(cameras)
# 获取实时图像
while True:
    image, time_stamp = camera.get_latest_image("head")
    # print(image)
    # 获取指定时间戳的图像
    # timestamp_ns = int(time.time() * 1e9) # 当前时间戳(纳秒)
    # image = camera.get_image_nearest("head", timestamp_ns)
    # 监控相机状态
    fps = camera.get_fps("head")
    print(f"head相机帧率: {fps}")
    time.sleep(0.03)
# latency = camera.get_latency_stats("head", window_seconds=5.0)
# 使用完毕后关闭相机