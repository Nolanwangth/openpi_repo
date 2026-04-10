#!/usr/bin/env python3
"""
相机(Camera)接口使用演示程序
展示如何使用 agibot_gdk 或 gdk_env 进行相机图像获取和处理
"""

import time
import os

try:
    import agibot_gdk as gdk
except ImportError:
    try:
        import gdk_env as gdk
    except ImportError as e:
        raise ImportError(
            "未找到相机 Python 包：请在当前环境安装 agibot_gdk 或 gdk_env（通常随 Agibot GDK / 机载 SDK 的 wheel 提供）。"
        ) from e
import numpy as np
from typing import List, Dict, Any, Optional, Tuple

# 尝试导入OpenCV，如果失败则使用替代方案
try:
    import cv2
    HAS_OPENCV = True
except ImportError:
    HAS_OPENCV = False

class CameraDemo:
    def __init__(self):
        """初始化相机对象"""
        print("正在初始化相机对象...")
        self.camera = gdk.Camera()
        time.sleep(3)
        
        # 所有可用的相机类型
        self.camera_types = [
            # (gdk.CameraType.kHeadBackFisheye, "头部背部鱼眼相机"),
            # (gdk.CameraType.kHeadLeftFisheye, "头部左侧鱼眼相机"),
            # (gdk.CameraType.kHeadRightFisheye, "头部右侧鱼眼相机"),
            (gdk.CameraType.kHeadStereoLeft, "头部立体左相机"),
            (gdk.CameraType.kHeadStereoRight, "头部立体右相机"),
            (gdk.CameraType.kHandLeftColor, "左手相机"),
            (gdk.CameraType.kHandRightColor, "右手相机"),
            (gdk.CameraType.kHeadDepth, "深度相机"),
            (gdk.CameraType.kHeadColor, "头部彩色相机"),
        ]
        
        print("相机初始化完成！")

    def test_camera_type(self, camera_type, camera_name, test_count=3):
        """测试指定类型的相机"""
        print(f"\n{'='*60}")
        print(f"测试 {camera_name} ({camera_type})")
        print(f"{'='*60}")
        
        success_count = 0
        
        for i in range(test_count):
            print(f"\n--- {camera_name} 图像 #{i+1} ---")
            
            # 获取最新图像数据
            image = self.camera.get_latest_image(camera_type, 1000.0)
            
            if image is not None:
                success_count += 1
                self.print_image_info(image, camera_name, i+1)
                
                # 保存图像到文件
                os.makedirs("saved_images", exist_ok=True)
                filename = f"saved_images/{camera_name.replace(' ', '_')}_{i+1}_{image.timestamp_ns}.jpg"
                self.save_image_to_file(image, filename, camera_name)
                
                # # 测试 get_nearest_image 方法
                # print(f"--------------------------------")
                # print("测试 get_nearest_image 方法:")
                # image_nearest = self.camera.get_nearest_image(
                #     camera_type, image.timestamp_ns-1000000000, 1000.0)
                
                # if image_nearest is not None:
                #     print(f"✅ 最近图像数据: {image_nearest.timestamp_ns}")
                #     print(f"图像尺寸: {image_nearest.width} x {image_nearest.height}")
                # else:
                #     print(f"❌ 未找到最近的 {camera_name} 数据")
                    
            else:
                print(f"❌ 未收到 {camera_name} 图像 #{i+1}")
            
            time.sleep(1.0)
        
        print(f"\n{camera_name} 测试结果: {success_count}/{test_count} 成功")
        return success_count, test_count

    def print_image_info(self, image, camera_name, image_num):
        """打印图像信息"""
        print(f"✅ 时间戳: {image.timestamp_ns}")
        print(f"图像尺寸: {image.width} x {image.height}")
        print(f"编码格式: {image.encoding}")
        print(f"颜色格式: {image.color_format}")
        print(f"位深度: {image.bit_depth}")
        
        # 打印数据信息
        if hasattr(image, 'data') and image.data.any():
            data_size = len(image.data)
            print(f"数据大小: {data_size} 字节")
        else:
            print("数据视图: 无数据")

    def get_camera_fps(self, camera_type, camera_name):
        """获取相机帧率"""
        try:
            fps = self.camera.get_image_fps(camera_type)
            print(f"{camera_name} 帧率: {fps:.2f} FPS")
            return fps
        except Exception as e:
            print(f"获取 {camera_name} 帧率失败: {e}")
            return None

    def get_camera_latency(self, camera_type, camera_name, window_seconds=10.0):
        """获取相机延迟统计"""
        try:
            latency_stats = self.camera.get_image_latency(camera_type, window_seconds)
            print(f"{camera_name} 延迟统计 (窗口: {window_seconds}秒):")
            print(f"  最大延迟: {latency_stats.max_latency_ms:.2f} ms")
            print(f"  平均延迟: {latency_stats.avg_latency_ms:.2f} ms")
            print(f"  99%延迟: {latency_stats.p99_latency_ms:.2f} ms")
            print(f"  99.9%延迟: {latency_stats.p999_latency_ms:.2f} ms")
            print(f"  99.99%延迟: {latency_stats.p9999_latency_ms:.2f} ms")
            return latency_stats
        except Exception as e:
            print(f"获取 {camera_name} 延迟统计失败: {e}")
            return None

    def get_image_shape(self, camera_type, camera_name):
        """获取图像尺寸"""
        try:
            shape = self.camera.get_image_shape(camera_type)
            print(f"{camera_name} 图像尺寸: {shape[0]} x {shape[1]}")
            return shape
        except Exception as e:
            print(f"获取 {camera_name} 图像尺寸失败: {e}")
            return None

    def decode_image_data(self, image) -> Optional[np.ndarray]:
        """解码图像数据为numpy数组"""
        if not hasattr(image, 'data') or not image.data.any():
            print("图像数据为空")
            return None
        
        try:
            # 根据编码格式解码数据（参考camera_web_viewer.py的解码方式）
            if image.encoding == gdk.Encoding.JPEG:
                if HAS_OPENCV:
                    # JPEG编码，使用OpenCV解码（返回BGR格式，不转换）
                    nparr = np.frombuffer(image.data, np.uint8)
                    decoded_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                    return decoded_image
                else:
                    # 直接返回原始JPEG数据
                    return image.data
                    
            elif image.encoding == gdk.Encoding.PNG:
                if HAS_OPENCV:
                    # PNG编码，使用OpenCV解码（返回BGR格式，不转换）
                    nparr = np.frombuffer(image.data, np.uint8)
                    decoded_image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
                    return decoded_image
                else:
                    # 直接返回原始PNG数据
                    return image.data
                    
            elif image.encoding == gdk.Encoding.UNCOMPRESSED:
                # 未压缩数据，直接转换
                if image.color_format == gdk.ColorFormat.RGB:
                    decoded_image = np.frombuffer(image.data, dtype=np.uint8)
                    decoded_image = decoded_image.reshape((image.height, image.width, 3))
                    if HAS_OPENCV:
                        # RGB转BGR（参考camera_web_viewer.py）
                        decoded_image = cv2.cvtColor(decoded_image, cv2.COLOR_RGB2BGR)
                    return decoded_image
                elif image.color_format == gdk.ColorFormat.BGR:
                    # BGR格式，直接使用（参考camera_web_viewer.py）
                    decoded_image = np.frombuffer(image.data, dtype=np.uint8)
                    decoded_image = decoded_image.reshape((image.height, image.width, 3))
                    return decoded_image
                elif image.color_format == gdk.ColorFormat.GRAY8:
                    decoded_image = np.frombuffer(image.data, dtype=np.uint8)
                    decoded_image = decoded_image.reshape((image.height, image.width))
                    if HAS_OPENCV:
                        # 灰度转BGR（参考camera_web_viewer.py）
                        decoded_image = cv2.cvtColor(decoded_image, cv2.COLOR_GRAY2BGR)
                    return decoded_image
                elif image.color_format == gdk.ColorFormat.GRAY16:
                    # 16位灰度图（参考camera_web_viewer.py：转换为8位）
                    decoded_image = np.frombuffer(image.data, dtype=np.uint16)
                    decoded_image = decoded_image.reshape((image.height, image.width))
                    # 转换为8位
                    decoded_image = (decoded_image / 256).astype(np.uint8)
                    if HAS_OPENCV:
                        decoded_image = cv2.cvtColor(decoded_image, cv2.COLOR_GRAY2BGR)
                    return decoded_image
                elif image.color_format == gdk.ColorFormat.RS2_FORMAT_Z16:
                    # Intel RealSense 16位深度格式
                    decoded_image = np.frombuffer(image.data, dtype=np.uint16)
                    decoded_image = decoded_image.reshape((image.height, image.width))
                    return decoded_image
                else:
                    print(f"不支持的颜色格式: {image.color_format}")
                    return None
            else:
                print(f"不支持的编码格式: {image.encoding}")
                return None
                
        except Exception as e:
            print(f"解码图像数据失败: {e}")
            return None

    def analyze_image(self, image, camera_name):
        """分析图像数据"""
        print(f"\n--- {camera_name} 图像分析 ---")
        
        decoded_image = self.decode_image_data(image)
        if decoded_image is not None:
            print(f"解码后图像形状: {decoded_image.shape}")
            print(f"数据类型: {decoded_image.dtype}")
            
            if len(decoded_image.shape) == 3:  # 彩色图像
                print(f"通道数: {decoded_image.shape[2]}")
                print(f"像素值范围: [{decoded_image.min()}, {decoded_image.max()}]")
                print(f"平均像素值: {decoded_image.mean():.2f}")
                
                # 计算每个通道的统计信息
                for i in range(decoded_image.shape[2]):
                    channel = decoded_image[:, :, i]
                    print(f"  通道 {i}: 均值={channel.mean():.2f}, 标准差={channel.std():.2f}")
            else:  # 灰度图像
                print(f"像素值范围: [{decoded_image.min()}, {decoded_image.max()}]")
                print(f"平均像素值: {decoded_image.mean():.2f}")
                print(f"标准差: {decoded_image.std():.2f}")
            
            return decoded_image
        else:
            print("无法分析图像数据")
            return None

    def save_image_to_file(self, image, filename, camera_name):
        """保存图像数据到文件"""
        try:
            # 如果图像是压缩格式，直接保存原始数据
            if image.encoding in [gdk.Encoding.JPEG, gdk.Encoding.PNG]:
                with open(filename, "wb") as f:
                    f.write(image.data)
                print(f"✅ 图像已保存到: {filename}")
                return True
            
            # 对于未压缩格式，尝试解码后保存
            decoded_image = self.decode_image_data(image)
            if decoded_image is not None:
                # 检查是否是16位深度图像
                is_16bit_depth = (image.color_format == gdk.ColorFormat.RS2_FORMAT_Z16 or 
                                 image.color_format == gdk.ColorFormat.GRAY16)
                
                if HAS_OPENCV:
                    # 使用OpenCV保存图像（解码后的图像已经是BGR格式，直接保存）
                    if len(decoded_image.shape) == 3:
                        # 彩色图像（已经是BGR格式，直接保存）
                        cv2.imwrite(filename, decoded_image)
                    else:
                        # 灰度图像
                        if is_16bit_depth:
                            # 16位深度图像，保存为16位PNG
                            png_filename = filename.replace('.jpg', '.png')
                            cv2.imwrite(png_filename, decoded_image)
                            print(f"✅ 16位深度图像已保存到: {png_filename}")
                        else:
                            # 8位灰度图像
                            cv2.imwrite(filename, decoded_image)
                else:
                    # 没有OpenCV，保存为原始数据
                    if len(decoded_image.shape) == 3:
                        # 彩色图像，保存为PPM格式
                        ppm_filename = filename.replace('.jpg', '.ppm').replace('.png', '.ppm')
                        with open(ppm_filename, 'wb') as f:
                            f.write(f'P6\n{decoded_image.shape[1]} {decoded_image.shape[0]}\n255\n'.encode())
                            f.write(decoded_image.tobytes())
                        print(f"✅ 图像已保存到: {ppm_filename} (PPM格式)")
                    else:
                        # 灰度图像
                        if is_16bit_depth:
                            # 16位灰度图像，保存为16位PGM格式
                            pgm_filename = filename.replace('.jpg', '.pgm').replace('.png', '.pgm')
                            max_val = np.max(decoded_image)
                            if max_val > 65535:
                                max_val = 65535
                            with open(pgm_filename, 'wb') as f:
                                f.write(f'P5\n{decoded_image.shape[1]} {decoded_image.shape[0]}\n{max_val}\n'.encode())
                                f.write(decoded_image.tobytes())
                            print(f"✅ 16位深度图像已保存到: {pgm_filename} (16位PGM格式)")
                        else:
                            # 8位灰度图像，保存为PGM格式
                            pgm_filename = filename.replace('.jpg', '.pgm').replace('.png', '.pgm')
                            with open(pgm_filename, 'wb') as f:
                                f.write(f'P5\n{decoded_image.shape[1]} {decoded_image.shape[0]}\n255\n'.encode())
                                f.write(decoded_image.tobytes())
                            print(f"✅ 图像已保存到: {pgm_filename} (PGM格式)")
                
                return True
            else:
                print(f"❌ 无法保存图像数据")
                return False
        except Exception as e:
            print(f"❌ 保存图像失败: {e}")
            return False

    def continuous_monitoring(self, camera_type, camera_name, duration_seconds=30):
        """连续监控相机数据"""
        print(f"\n{'='*60}")
        print(f"连续监控 {camera_name} ({duration_seconds}秒)")
        print(f"{'='*60}")
        print("按Ctrl+C停止监控")
        
        start_time = time.time()
        count = 0
        fps_sum = 0
        fps_count = 0
        
        try:
            while time.time() - start_time < duration_seconds:
                image = self.camera.get_latest_image(camera_type, 1000.0)
                
                if image is not None:
                    count += 1
                    current_time = time.time()
                    elapsed = current_time - start_time
                    
                    if count > 1:
                        fps = 1.0 / (current_time - last_time)
                        fps_sum += fps
                        fps_count += 1
                    
                    last_time = current_time
                    
                    # 显示基本信息
                    print(f"\r{camera_name} 监控 #{count} - "
                          f"时间戳: {image.timestamp_ns} - "
                          f"尺寸: {image.width}x{image.height} - "
                          f"运行时间: {elapsed:.1f}s", end="")
                    
                    # 每10帧显示一次详细信息
                    if count % 10 == 0:
                        print(f"\n  第{count}帧详细信息:")
                        self.analyze_image(image, camera_name)
                else:
                    print(f"\r{camera_name} 监控 - 无数据", end="")
                
                time.sleep(0.1)
                
        except KeyboardInterrupt:
            print(f"\n\n监控被用户中断")
        
        # 显示统计信息
        if count > 0:
            avg_fps = fps_sum / fps_count if fps_count > 0 else 0
            print(f"\n\n监控统计:")
            print(f"  总帧数: {count}")
            print(f"  平均帧率: {avg_fps:.2f} FPS")
            print(f"  监控时长: {time.time() - start_time:.1f} 秒")

    def run_comprehensive_test(self):
        """运行综合测试"""
        print("📷 相机综合测试程序")
        print("=" * 50)
        
        total_success = 0
        total_tests = 0
        available_cameras = []
        
        # 1. 测试所有相机类型
        print("\n1. 测试所有相机类型")
        for camera_type, camera_name in self.camera_types:
            success, tests = self.test_camera_type(camera_type, camera_name)
            total_success += success
            total_tests += tests
            
            if success > 0:
                available_cameras.append((camera_type, camera_name))
        
        # 2. 显示总结
        print(f"\n{'='*60}")
        print("测试总结")
        print(f"{'='*60}")
        print(f"总测试次数: {total_tests}")
        print(f"成功次数: {total_success}")
        print(f"成功率: {total_success/total_tests*100:.1f}%")
        
        if available_cameras:
            print(f"\n可用的相机类型:")
            for camera_type, camera_name in available_cameras:
                print(f"  ✅ {camera_name}")
            
            # 3. 获取性能信息
            print(f"\n2. 获取性能信息")
            for camera_type, camera_name in available_cameras:
                self.get_image_shape(camera_type, camera_name)
                self.get_camera_fps(camera_type, camera_name)
                self.get_camera_latency(camera_type, camera_name)
            
            # 4. 连续监控演示
            if available_cameras:
                print(f"\n3. 连续监控演示")
                first_camera_type, first_camera_name = available_cameras[0]
                self.continuous_monitoring(first_camera_type, first_camera_name, 10)
        else:
            print(f"\n❌ 没有检测到可用的相机")

def main():
    """主函数"""
    demo = CameraDemo()
    
    print("选择运行模式:")
    print("1. 综合测试")
    print("2. 只测试特定相机")
    print("3. 连续监控模式")
    
    try:
        choice = input("请输入选择 (1, 2, 或 3): ").strip()
        
        if choice == "2":
            print("\n可用的相机类型:")
            for i, (camera_type, camera_name) in enumerate(demo.camera_types):
                print(f"{i}: {camera_name}")
            
            camera_choice = input("请选择相机 (输入数字): ").strip()
            try:
                camera_index = int(camera_choice)
                if 0 <= camera_index < len(demo.camera_types):
                    camera_type, camera_name = demo.camera_types[camera_index]
                    demo.test_camera_type(camera_type, camera_name, 5)
                else:
                    print("无效选择，运行综合测试")
                    demo.run_comprehensive_test()
            except ValueError:
                print("无效输入，运行综合测试")
                demo.run_comprehensive_test()
                
        elif choice == "3":
            print("\n可用的相机类型:")
            for i, (camera_type, camera_name) in enumerate(demo.camera_types):
                print(f"{i}: {camera_name}")
            
            camera_choice = input("请选择相机 (输入数字): ").strip()
            duration = input("监控时长(秒，默认30): ").strip()
            duration = int(duration) if duration else 30
            
            try:
                camera_index = int(camera_choice)
                if 0 <= camera_index < len(demo.camera_types):
                    camera_type, camera_name = demo.camera_types[camera_index]
                    demo.continuous_monitoring(camera_type, camera_name, duration)
                else:
                    print("无效选择")
            except ValueError:
                print("无效输入")
        else:
            # 默认运行综合测试
            demo.run_comprehensive_test()
            
    except KeyboardInterrupt:
        print("\n⚠️ 用户中断程序")
    except Exception as e:
        print(f"\n❌ 程序运行出错: {e}")
        print("运行综合测试...")
        demo.run_comprehensive_test()
    finally:
        # 关闭相机
        try:
            demo.camera.close_camera()
            print("相机已关闭")
        except:
            pass

if __name__ == "__main__":
    main()
