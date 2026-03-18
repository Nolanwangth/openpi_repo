import json
import argparse
from typing import Dict, List

# 相机名称到ID的映射
CAMERA_NAME_TO_ID = {
    "back_left_fisheye": "cam0",
    "hand_left_fisheye": "cam1",
    "hand_right_fisheye": "cam2",
    "back_right_fisheye": "cam3",
    "head_center_fisheye": "cam4",
    "head_left_fisheye": "cam5",
    "head_right_fisheye": "cam6"
}

# 添加RS相机映射
RS_CAMERA_MAP = {
    "d455_1": {
        "name": "head",
        "default_width": 1280,
        "default_height": 720
    },
    "d405_1": {
        "name": "hand_left",
        "default_width": 848,
        "default_height": 480
    },
    "d405_2": {
        "name": "hand_right",
        "default_width": 848,
        "default_height": 480
    }
}

def create_fisheye_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='生成相机配置文件')
    
    # 相机选择
    parser.add_argument('--cameras', type=str, nargs='+', 
                       default=['hand_left_fisheye', 'hand_right_fisheye', 'head_center_fisheye'],
                       help='要配置的相机名称列表')
    
    # 基础参数
    parser.add_argument('--fps', type=int, default=30,
                       help='出图帧率 (5-30之间且能被30整除)')
    
    # 图像预处理参数
    parser.add_argument('--balance', type=float, default=1.0,
                       help='去畸变视野调整 (默认1.0)')
    
    # 裁剪参数
    parser.add_argument('--crop', type=int, nargs=4, default=[0, 0, 1920, 1536],
                       help='裁剪参数 left top right bottom')
    parser.add_argument('--resize', type=int, nargs=2, default=[1920, 1536],
                       help='调整大小 width height')
    
    # 通道置换
    parser.add_argument('--channel_order', type=int, nargs=3, default=[0, 1, 2],
                       help='通道顺序 (例如: RGB=[0,1,2], BGR=[2,1,0])')
    
    return parser

def validate_fisheye_params(args) -> bool:
    # 验证相机名称
    for cam_name in args.cameras:
        if cam_name not in CAMERA_NAME_TO_ID:
            print(f"错误: 无效的相机名称: {cam_name}")
            print("可用的相机名称:")
            for name, id in CAMERA_NAME_TO_ID.items():
                print(f"  {name} ({id})")
            return False
    
    # 验证FPS
    if not (5 <= args.fps <= 30 and 30 % args.fps == 0):
        print(f"错误: FPS必须在5-30之间且能被30整除，当前值: {args.fps}")
        return False
        
    # 验证裁剪参数
    left, top, right, bottom = args.crop
    if not (0 <= left < right <= 1920 and 0 <= top < bottom <= 1536):
        print(f"错误: 裁剪参数无效: {args.crop}")
        return False
        
    # 验证resize参数
    width, height = args.resize
    if not (0 < width <= 1920 and 0 < height <= 1536):
        print(f"错误: resize参数无效: {args.resize}")
        return False
        
    # 验证通道顺序
    if not all(0 <= x <= 2 for x in args.channel_order) or len(set(args.channel_order)) != 3:
        print(f"错误: 通道顺序参数无效: {args.channel_order}")
        return False
        
    return True

def generate_fisheye_config(args) -> Dict:
    config = {}
    left, top, right, bottom = args.crop
    width, height = args.resize
    
    for cam_name in args.cameras:
        cam_id = CAMERA_NAME_TO_ID[cam_name]
        config[cam_id] = {
            "width": "1920",
            "height": "1536",
            "fps": str(args.fps),
            "name": cam_name,
            "img_process": {
                "calibFile": f"/data/parameters/{cam_name}_intrinsic_params.json",
                "balance": str(args.balance),
                "crop_resize": {
                    "left": str(left),
                    "top": str(top),
                    "right": str(right),
                    "bottom": str(bottom),
                    "resizedwidth": str(width),
                    "resizedHeight": str(height)
                },
                "permuteOrder": args.channel_order
            }
        }
    
    return config

def create_rs_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='生成RS相机配置文件')
    
    # 相机选择
    parser.add_argument('--cameras', type=str, nargs='+',
                       default=['d455_1', 'd405_1', 'd405_2'],
                       help='要配置的相机ID列表')
    
    # 基础参数
    parser.add_argument('--fps', type=int, default=30,
                       help='出图帧率 (5-30之间且能被30整除)')
    
    # D455分辨率
    parser.add_argument('--d455_resolution', type=int, nargs=2, default=[1280, 720],
                       help='D455相机分辨率 width height')
    
    # D405分辨率
    parser.add_argument('--d405_resolution', type=int, nargs=2, default=[848, 480],
                       help='D405相机分辨率 width height')
    
    # 裁剪和调整大小参数
    parser.add_argument('--crop', action='store_true',
                       help='是否启用裁剪')
    parser.add_argument('--crop_params', type=int, nargs=4,
                       help='裁剪参数 left top right bottom')
    parser.add_argument('--resize', type=int, nargs=2,
                       help='调整大小 width height')
    
    # 通道置换
    parser.add_argument('--channel_order', type=int, nargs=3, default=[0, 1, 2],
                       help='通道顺序 (例如: RGB=[0,1,2], BGR=[2,1,0])')
    
    return parser

def validate_rs_params(args) -> bool:
    # 验证相机ID
    for cam_id in args.cameras:
        if cam_id not in RS_CAMERA_MAP:
            print(f"错误: 无效的相机ID: {cam_id}")
            print("可用的相机ID:")
            for id, info in RS_CAMERA_MAP.items():
                print(f"  {id} ({info['name']})")
            return False
    
    # 验证FPS
    if not (5 <= args.fps <= 30 and 30 % args.fps == 0):
        print(f"错误: FPS必须在5-30之间且能被30整除，当前值: {args.fps}")
        return False
    
    # 如果启用裁剪，验证裁剪参数
    if args.crop and args.crop_params:
        left, top, right, bottom = args.crop_params
        for cam_id in args.cameras:
            width = args.d455_resolution[0] if 'd455' in cam_id else args.d405_resolution[0]
            height = args.d455_resolution[1] if 'd455' in cam_id else args.d405_resolution[1]
            if not (0 <= left < right <= width and 0 <= top < bottom <= height):
                print(f"错误: {cam_id}的裁剪参数无效: {args.crop_params}")
                return False
    
    # 验证通道顺序
    if not all(0 <= x <= 2 for x in args.channel_order) or len(set(args.channel_order)) != 3:
        print(f"错误: 通道顺序参数无效: {args.channel_order}")
        return False
    
    return True

def generate_rs_config(args) -> Dict:
    config = {}
    
    for cam_id in args.cameras:
        # 确定分辨率
        if 'd455' in cam_id:
            width, height = args.d455_resolution
        else:
            width, height = args.d405_resolution
        
        config[cam_id] = {
            "name": RS_CAMERA_MAP[cam_id]["name"],
            "fps": str(args.fps),
            "width": str(width),
            "height": str(height),
            "img_process": {
                "crop_resize": {
                    "left": str(args.crop_params[0] if args.crop and args.crop_params else 0),
                    "top": str(args.crop_params[1] if args.crop and args.crop_params else 0),
                    "right": str(args.crop_params[2] if args.crop and args.crop_params else width),
                    "bottom": str(args.crop_params[3] if args.crop and args.crop_params else height),
                    "resizedwidth": str(args.resize[0] if args.resize else width),
                    "resizedHeight": str(args.resize[1] if args.resize else height)
                },
                "permuteOrder": args.channel_order
            }
        }
    
    return config

def generate_fisheye_config_api(cameras=None, fps=30, balance=1.0, crop=None, resize=None, channel_order=None, output_file=None):
    """API函数：生成鱼眼相机配置文件
    
    Args:
        cameras: 相机名称列表，默认为 ['hand_left_fisheye', 'hand_right_fisheye', 'head_center_fisheye']
        fps: 帧率，默认为30
        balance: 去畸变视野调整，默认为1.0
        crop: 裁剪参数 [left, top, right, bottom]，默认为 [0, 0, 1920, 1536]
        resize: 调整大小 [width, height]，默认为 [1920, 1536]
        channel_order: 通道顺序，默认为 [0, 1, 2]
        output_file: 输出文件路径，默认为 "fisheye_camera_conf.json"
        
    Returns:
        Dict: 生成的配置字典
    """
    # 设置默认值
    if cameras is None:
        cameras = ['hand_left_fisheye', 'hand_right_fisheye', 'head_center_fisheye']
    if crop is None:
        crop = [0, 0, 1920, 1536]
    if resize is None:
        resize = [1920, 1536]
    if channel_order is None:
        channel_order = [0, 1, 2]
    if output_file is None:
        output_file = "fisheye_camera_conf.json"
    
    # 创建类似命令行参数的对象
    class Args:
        pass
    
    args = Args()
    args.cameras = cameras
    args.fps = fps
    args.balance = balance
    args.crop = crop
    args.resize = resize
    args.channel_order = channel_order
    
    # 验证参数
    if not validate_fisheye_params(args):
        return None
    
    # 生成配置
    config = generate_fisheye_config(args)
    
    # 保存配置
    if output_file:
        with open(output_file, 'w') as f:
            json.dump(config, f, indent=4)
    
    return config

def generate_rs_config_api(cameras=None, fps=30, d455_resolution=None, d405_resolution=None, 
                           crop=False, crop_params=None, resize=None, channel_order=None, output_file=None):
    """API函数：生成RS相机配置文件
    
    Args:
        cameras: 相机ID列表，默认为 ['d455_1', 'd405_1', 'd405_2']
        fps: 帧率，默认为30
        d455_resolution: D455相机分辨率 [width, height]，默认为 [1280, 720]
        d405_resolution: D405相机分辨率 [width, height]，默认为 [848, 480]
        crop: 是否启用裁剪，默认为False
        crop_params: 裁剪参数 [left, top, right, bottom]
        resize: 调整大小 [width, height]
        channel_order: 通道顺序，默认为 [0, 1, 2]
        output_file: 输出文件路径，默认为 "rs_camera_conf.json"
        
    Returns:
        Dict: 生成的配置字典
    """
    # 设置默认值
    if cameras is None:
        cameras = ['d455_1', 'd405_1', 'd405_2']
    if d455_resolution is None:
        d455_resolution = [1280, 720]
    if d405_resolution is None:
        d405_resolution = [848, 480]
    if channel_order is None:
        channel_order = [0, 1, 2]
    if output_file is None:
        output_file = "rs_camera_conf.json"
    
    # 创建类似命令行参数的对象
    class Args:
        pass
    
    args = Args()
    args.cameras = cameras
    args.fps = fps
    args.d455_resolution = d455_resolution
    args.d405_resolution = d405_resolution
    args.crop = crop
    args.crop_params = crop_params
    args.resize = resize
    args.channel_order = channel_order
    
    # 验证参数
    if not validate_rs_params(args):
        return None
    
    # 生成配置
    config = generate_rs_config(args)
    
    # 保存配置
    if output_file:
        with open(output_file, 'w') as f:
            json.dump(config, f, indent=4)
    
    return config

def main():
    # 创建主解析器
    parser = argparse.ArgumentParser(description='相机配置生成工具')
    subparsers = parser.add_subparsers(dest='type', help='选择要生成的相机配置类型')
    
    # 添加鱼眼相机子命令
    fisheye_parser = subparsers.add_parser('fisheye', help='生成鱼眼相机配置')
    fisheye_parser.add_argument('--cameras', type=str, nargs='+', 
                               default=['hand_left_fisheye', 'hand_right_fisheye', 'head_center_fisheye'],
                               help='要配置的相机名称列表')
    fisheye_parser.add_argument('--fps', type=int, default=30,
                               help='出图帧率 (5-30之间且能被30整除)')
    fisheye_parser.add_argument('--balance', type=float, default=1.0,
                               help='去畸变视野调整 (默认1.0)')
    fisheye_parser.add_argument('--crop', type=int, nargs=4, default=[0, 0, 1920, 1536],
                               help='裁剪参数 left top right bottom')
    fisheye_parser.add_argument('--resize', type=int, nargs=2, default=[1920, 1536],
                               help='调整大小 width height')
    fisheye_parser.add_argument('--channel_order', type=int, nargs=3, default=[0, 1, 2],
                               help='通道顺序 (例如: RGB=[0,1,2], BGR=[2,1,0])')
    
    # 添加RS相机子命令
    rs_parser = subparsers.add_parser('rs', help='生成RS相机配置')
    rs_parser.add_argument('--cameras', type=str, nargs='+',
                          default=['d455_1', 'd405_1', 'd405_2'],
                          help='要配置的相机ID列表')
    rs_parser.add_argument('--fps', type=int, default=30,
                          help='出图帧率 (5-30之间且能被30整除)')
    rs_parser.add_argument('--d455_resolution', type=int, nargs=2, default=[1280, 720],
                          help='D455相机分辨率 width height')
    rs_parser.add_argument('--d405_resolution', type=int, nargs=2, default=[848, 480],
                          help='D405相机分辨率 width height')
    rs_parser.add_argument('--crop', action='store_true',
                          help='是否启用裁剪')
    rs_parser.add_argument('--crop_params', type=int, nargs=4,
                          help='裁剪参数 left top right bottom')
    rs_parser.add_argument('--resize', type=int, nargs=2,
                          help='调整大小 width height')
    rs_parser.add_argument('--channel_order', type=int, nargs=3, default=[0, 1, 2],
                          help='通道顺序 (例如: RGB=[0,1,2], BGR=[2,1,0])')
    
    args = parser.parse_args()
    
    if args.type == 'fisheye':
        if validate_fisheye_params(args):
            config = generate_fisheye_config(args)
            output_file = "fisheye_camera_conf.json"
            with open(output_file, 'w') as f:
                json.dump(config, f, indent=4)
            
            print(f"配置文件已生成：{output_file}")
            print("\n当前配置参数:")
            print(f"选择的相机: {args.cameras}")
            print(f"对应的camID: {[CAMERA_NAME_TO_ID[name] for name in args.cameras]}")
            print(f"FPS: {args.fps}")
            print(f"去畸变balance: {args.balance}")
            print(f"裁剪区域: left={args.crop[0]}, top={args.crop[1]}, right={args.crop[2]}, bottom={args.crop[3]}")
            print(f"调整大小: width={args.resize[0]}, height={args.resize[1]}")
            print(f"通道顺序: {args.channel_order}")
    
    elif args.type == 'rs':
        if validate_rs_params(args):
            config = generate_rs_config(args)
            output_file = "rs_camera_conf.json"
            with open(output_file, 'w') as f:
                json.dump(config, f, indent=4)
            
            print(f"配置文件已生成：{output_file}")
            print("\n当前配置参数:")
            print(f"选择的相机: {args.cameras}")
            print(f"FPS: {args.fps}")
            print(f"D455分辨率: {args.d455_resolution}")
            print(f"D405分辨率: {args.d405_resolution}")
            if args.crop and args.crop_params:
                print(f"裁剪区域: left={args.crop_params[0]}, top={args.crop_params[1]}, "
                      f"right={args.crop_params[2]}, bottom={args.crop_params[3]}")
            if args.resize:
                print(f"调整大小: width={args.resize[0]}, height={args.resize[1]}")
            print(f"通道顺序: {args.channel_order}")
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
