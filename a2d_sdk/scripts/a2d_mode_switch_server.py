import zmq
import os
import sys
import subprocess
from enum import Enum
import subprocess
import logging
import time
import datetime
from google.protobuf import text_format
import json

current_dir = os.path.dirname(os.path.abspath(__file__))
workspace_dir = os.path.realpath(os.path.join(current_dir, "../"))
print(f"workspace_dir: {workspace_dir}")
sys.path.append(workspace_dir)
sys.path.append(os.path.join(workspace_dir, "proto"))

from proto.mode_switch_pb2 import ModeSwitchRequest, Mode, ModeSwitchResponse
from proto.image_preprocess_pb2 import ImagePreprocessParam

mode_switch_request_path = os.path.join("/data/logs/", "mode_switch_request.txt")
sdk_wrapper_path = os.path.join(workspace_dir, "scripts/sdk_wrapper.sh")
cosine_sdk_type = ""

def setup_logger(logger_name):
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)
    # integrate with other projects, write log to parent directory
    log_dir = os.path.join("/data/", "logs")
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    file_handler = logging.FileHandler(f"{log_dir}/{logger_name}.txt")
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.ERROR)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger

server_logger = setup_logger("a2d_mode_switch")

def clear_archive_log():
    log_dir = os.path.join("/data/", "logs")
    clear_cmd = f"mkdir -p {log_dir} && rm -rf {log_dir}/*.tar.gz"
    try:
        subprocess.run(clear_cmd, shell=True, check=True)
    except Exception as e:
        server_logger.error(f"Failed to clear log: {e}")

def archieve_log():
    log_dir = os.path.join("/data/", "logs")
    timestamp = datetime.datetime.now().strftime("%Y%m%d.%H%M%S")
    log_file_name = f"log_{timestamp}.tar.gz"
    log_file_path = os.path.join(log_dir, log_file_name)
    cmd = f"cd /data/ && tar --warning=no-file-changed --exclude='*.tar.gz' -zcvf {log_file_name} logs/ && mv {log_file_name} logs/"
    clear_cmd_txt = f"cd /data/logs/ && ls *.txt | grep -v a2d_mode_switch | xargs rm -rf"
    clear_cmd_log = f"cd /data/logs/ && ls *INFO* | grep -v a2d_mode_switch | xargs rm -rf"
    try:
        subprocess.run(cmd, shell=True, check=True)
        subprocess.run(clear_cmd_txt, shell=True, check=True)
        subprocess.run(clear_cmd_log, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Warning: Command failed with error {e}")

def start_http_server():
    # check if http server is already running by checking process name
    ps_command = f"ps aux | grep http.server | grep -v grep"
    try:
        result = subprocess.check_output(ps_command, shell=True, text=True)
        if "http.server" in result:
            server_logger.info("http server is already running.")
            return True
    except subprocess.CalledProcessError:
        pass

    server_logger.info("Starting http server...")
    subprocess.Popen(f"nohup bash {workspace_dir}/scripts/start_http_server.sh > /data/logs//http_server.txt 2>&1 &", shell=True)
    server_logger.info("http server started successfully.")
    return True

# 增加enum映射
MountPos = {
    0: "head",
    1: "hand_left",
    2: "hand_right",
    3: "back_left_fisheye",
    4: "hand_left_fisheye",
    5: "hand_right_fisheye",
    6: "back_right_fisheye",
    7: "head_center_fisheye",
    8: "head_left_fisheye",
    9: "head_right_fisheye"
}

# 添加相机配置相关的常量
CAMERA_NAME_TO_ID = {
    "head": {"camera_id": "d455_1", "width": 1280, "height": 720},
    "hand_left": {"camera_id": "d405_1", "width": 848, "height": 480},
    "hand_right": {"camera_id": "d405_2", "width": 848, "height": 480},
    "back_left_fisheye": {"camera_id": "cam0", "width": 1920, "height": 1536, "calibFile": "/data/parameters/back_left_fisheye_intrinsic_params.json"},
    "hand_left_fisheye": {"camera_id": "cam1", "width": 1920, "height": 1536, "calibFile": "/data/parameters/hand_left_fisheye_intrinsic_params.json"},
    "hand_right_fisheye": {"camera_id": "cam2", "width": 1920, "height": 1536, "calibFile": "/data/parameters/hand_right_fisheye_intrinsic_params.json"},
    "back_right_fisheye": {"camera_id": "cam3", "width": 1920, "height": 1536, "calibFile": "/data/parameters/back_right_fisheye_intrinsic_params.json"},
    "head_center_fisheye": {"camera_id": "cam4", "width": 1920, "height": 1536, "calibFile": "/data/parameters/head_center_fisheye_intrinsic_params.json"},
    "head_left_fisheye": {"camera_id": "cam5", "width": 1920, "height": 1536, "calibFile": "/data/parameters/head_left_fisheye_intrinsic_params.json"},
    "head_right_fisheye": {"camera_id": "cam6", "width": 1920, "height": 1536, "calibFile": "/data/parameters/head_right_fisheye_intrinsic_params.json"}
}

def analyze_camera_config(config: ModeSwitchRequest):
    if len(config.img_preproc) == 0:
        server_logger.error("No camera config found.Will use default config.")
        # 检查文件是否存在，存在则删除
        fisheye_conf = os.path.join(workspace_dir, "/home/agi/app/conf/deploy/develop/fisheye_camera_conf.json")
        rs_conf = os.path.join(workspace_dir, "/home/agi/app/conf/deploy/develop/rs_camera_conf.json")
        
        if os.path.exists(fisheye_conf):
            os.remove(fisheye_conf)
        if os.path.exists(rs_conf):
            os.remove(rs_conf)
        return True
    
    rs_camera_config = {}
    fisheye_camera_config = {}
    for img_preproc in config.img_preproc:
        camera_pos = img_preproc.pos
        camera_name = MountPos[camera_pos]
        if camera_name in CAMERA_NAME_TO_ID:
            camera_id = CAMERA_NAME_TO_ID[camera_name]["camera_id"]
            width = CAMERA_NAME_TO_ID[camera_name]["width"]
            height = CAMERA_NAME_TO_ID[camera_name]["height"]
            if 'fisheye' in camera_name:
                fisheye_camera_config[camera_id] = {}
                fisheye_camera_config[camera_id]["name"]    = camera_name
                fisheye_camera_config[camera_id]["width"]   = str(width)
                fisheye_camera_config[camera_id]["height"]  = str(height)
                fisheye_camera_config[camera_id]["publish"] = True
                # 检查是否存在FrameRate
                if hasattr(img_preproc, "FrameRate"):
                    if img_preproc.FrameRate == 5 or img_preproc.FrameRate == 10 or img_preproc.FrameRate == 15 or img_preproc.FrameRate == 20 or img_preproc.FrameRate == 25 or img_preproc.FrameRate == 30:
                        fisheye_camera_config[camera_id]["fps"] = str(img_preproc.FrameRate)
                    else:
                        fisheye_camera_config[camera_id]["fps"] = str(30)
                else:
                    fisheye_camera_config[camera_id]["fps"] = str(30)
                fisheye_camera_config[camera_id]["img_process"] = {}
                fisheye_camera_config[camera_id]["img_process"]["enabled"] = False
                fisheye_camera_config[camera_id]["img_process"]["calibFile"] = CAMERA_NAME_TO_ID[camera_name]["calibFile"]
                if hasattr(img_preproc, "crop") and img_preproc.crop.enable:
                    fisheye_camera_config[camera_id]["img_process"]["enabled"] = True
                    fisheye_camera_config[camera_id]["img_process"]["crop_resize"] = {}
                    fisheye_camera_config[camera_id]["img_process"]["crop_resize"]["left"]   = str(img_preproc.crop.l)
                    fisheye_camera_config[camera_id]["img_process"]["crop_resize"]["top"]    = str(img_preproc.crop.t)
                    fisheye_camera_config[camera_id]["img_process"]["crop_resize"]["right"]  = str(img_preproc.crop.r)
                    fisheye_camera_config[camera_id]["img_process"]["crop_resize"]["bottom"] = str(img_preproc.crop.b)
                if hasattr(img_preproc, "resize") and img_preproc.resize.enable:
                    if "crop_resize" not in fisheye_camera_config[camera_id]["img_process"]:
                        fisheye_camera_config[camera_id]["img_process"]["crop_resize"] = {}
                    fisheye_camera_config[camera_id]["img_process"]["enabled"] = True
                    fisheye_camera_config[camera_id]["img_process"]["crop_resize"]["resizewidth"]  = str(img_preproc.resize.w)
                    fisheye_camera_config[camera_id]["img_process"]["crop_resize"]["resizeheight"] = str(img_preproc.resize.h)
                elif hasattr(img_preproc, "crop") and img_preproc.crop.enable:
                    if "crop_resize" not in fisheye_camera_config[camera_id]["img_process"]:
                        fisheye_camera_config[camera_id]["img_process"]["crop_resize"] = {}
                    # 如果crop没有设置，则根据width和height计算crop
                    width_re = (int(img_preproc.crop.r) - int(img_preproc.crop.l))
                    height_re = (int(img_preproc.crop.b) - int(img_preproc.crop.t))
                    fisheye_camera_config[camera_id]["img_process"]["crop_resize"]["resizewidth"]  = str(width_re)
                    fisheye_camera_config[camera_id]["img_process"]["crop_resize"]["resizeheight"] = str(height_re)
                if hasattr(img_preproc, "undistort") and img_preproc.undistort.enable:
                    fisheye_camera_config[camera_id]["img_process"]["enabled"] = True
                    fisheye_camera_config[camera_id]["img_process"]["balance"] = str(img_preproc.undistort.bal)
                else:
                    fisheye_camera_config[camera_id]["img_process"]["balance"] = "1.0"
                if hasattr(img_preproc, "permute") and img_preproc.permute.enable:
                    fisheye_camera_config[camera_id]["img_process"]["enabled"] = True
                    list_order = [img_preproc.permute.order1, img_preproc.permute.order2, img_preproc.permute.order3]
                    fisheye_camera_config[camera_id]["img_process"]["permuteOrder"] = list_order
                else:
                    fisheye_camera_config[camera_id]["img_process"]["permuteOrder"] = [0, 1, 2]
            else:
                rs_camera_config[camera_id] = {}
                rs_camera_config[camera_id]["name"]    = camera_name
                rs_camera_config[camera_id]["width"]   = str(width)
                rs_camera_config[camera_id]["height"]  = str(height)
                rs_camera_config[camera_id]["publish"] = True
                # 检查是否存在FrameRate
                if hasattr(img_preproc, "FrameRate"):
                    if img_preproc.FrameRate == 5 or img_preproc.FrameRate == 10 or img_preproc.FrameRate == 15 or img_preproc.FrameRate == 20 or img_preproc.FrameRate == 25 or img_preproc.FrameRate == 30:
                        rs_camera_config[camera_id]["fps"] = str(img_preproc.FrameRate)
                    else:
                        rs_camera_config[camera_id]["fps"] = str(30)
                else:
                    rs_camera_config[camera_id]["fps"] = str(30)
                if hasattr(img_preproc, "depth_enable"):
                    rs_camera_config[camera_id]["depthEnable"] = img_preproc.depth_enable
                else:
                    rs_camera_config[camera_id]["depthEnable"] = False
                rs_camera_config[camera_id]["img_process"] = {}
                rs_camera_config[camera_id]["img_process"]["enabled"] = False
                if hasattr(img_preproc, "crop") and img_preproc.crop.enable:
                    rs_camera_config[camera_id]["img_process"]["crop_resize"] = {}
                    rs_camera_config[camera_id]["img_process"]["enabled"] = True
                    rs_camera_config[camera_id]["img_process"]["crop_resize"]["left"]   = str(img_preproc.crop.l)
                    rs_camera_config[camera_id]["img_process"]["crop_resize"]["top"]    = str(img_preproc.crop.t)
                    rs_camera_config[camera_id]["img_process"]["crop_resize"]["right"]  = str(img_preproc.crop.r)
                    rs_camera_config[camera_id]["img_process"]["crop_resize"]["bottom"] = str(img_preproc.crop.b)
                if hasattr(img_preproc, "resize") and img_preproc.resize.enable:
                    if "crop_resize" not in rs_camera_config[camera_id]["img_process"]:
                        rs_camera_config[camera_id]["img_process"]["crop_resize"] = {}
                    rs_camera_config[camera_id]["img_process"]["enabled"] = True
                    rs_camera_config[camera_id]["img_process"]["crop_resize"]["resizewidth"]  = str(img_preproc.resize.w)
                    rs_camera_config[camera_id]["img_process"]["crop_resize"]["resizeheight"] = str(img_preproc.resize.h)
                elif hasattr(img_preproc, "crop") and img_preproc.crop.enable:
                    if "crop_resize" not in rs_camera_config[camera_id]["img_process"]:
                        rs_camera_config[camera_id]["img_process"]["crop_resize"] = {}
                    # 如果crop没有设置，则根据width和height计算crop
                    width_re = (int(img_preproc.crop.r) - int(img_preproc.crop.l))
                    height_re = (int(img_preproc.crop.b) - int(img_preproc.crop.t))
                    rs_camera_config[camera_id]["img_process"]["crop_resize"]["resizewidth"]  = str(width_re)
                    rs_camera_config[camera_id]["img_process"]["crop_resize"]["resizeheight"] = str(height_re)
                if hasattr(img_preproc, "permute") and img_preproc.permute.enable:
                    rs_camera_config[camera_id]["img_process"]["enabled"] = True
                    list_order = [img_preproc.permute.order1, img_preproc.permute.order2, img_preproc.permute.order3]
                    rs_camera_config[camera_id]["img_process"]["permuteOrder"] = list_order 
                else:
                    rs_camera_config[camera_id]["img_process"]["permuteOrder"] = [0, 1, 2]
        else:
            server_logger.error(f"Unknown camera position: {camera_pos}")
            return False
    
    # 将配置写入文件
    # 检查配置不为空则写入
    if len(fisheye_camera_config) > 0:
        with open(os.path.join(workspace_dir, "/home/agi/app/conf/deploy/develop/fisheye_camera_conf.json"), "w") as f:
            json.dump(fisheye_camera_config, f)
    if len(rs_camera_config) > 0:
        with open(os.path.join(workspace_dir, "/home/agi/app/conf/deploy/develop/rs_camera_conf.json"), "w") as f:
            json.dump(rs_camera_config, f)
    return True
    
def save_mode_witch_request(config: ModeSwitchRequest):
    with open(mode_switch_request_path, "w") as f:
        f.write(text_format.MessageToString(config))

def start_copilot_system(config: ModeSwitchRequest):
    is_use_cosine_sdk = config.hybrid_deploy_config.use_cosine_sdk
    camera_model = config.hybrid_deploy_config.camera_model
    if is_use_cosine_sdk:
        if camera_model == "copilot":
            cmd = f"{sdk_wrapper_path} start copilot"
            cosine_sdk_type = "copilot"
        elif camera_model == "develop":
            analyze_camera_config(config)
            cmd = f"{sdk_wrapper_path} start develop"
            cosine_sdk_type = "develop"
        elif camera_model == "compressed_image":
            cmd = f"{sdk_wrapper_path} start compressed_image"
            cosine_sdk_type = "compressed_image"
        elif camera_model == "vr":
            cmd = f"{sdk_wrapper_path} start vr"
            cosine_sdk_type = "vr"
        else:
            server_logger.error(f"Unknown camera model: {camera_model}")
            return False
        server_logger.info(f"Starting sdk_wrapper.sh in the background: {cmd}")
        subprocess.Popen(
            f"nohup bash -c '{cmd}' > /data/logs//sdk_wrapper.txt 2>&1 &", shell=True
        )
        server_logger.info("sdk_wrapper.sh started successfully.")
    else:
        server_logger.info("Not using cosine sdk, skip starting sdk_wrapper.sh")
        return False
    
    server_logger.info("copilot started successfully.")
    return True

def stop_copilot_system():
    cmd = f"{sdk_wrapper_path} stop"
    server_logger.info(f"Stopping sdk with {cmd} in the background...")
    subprocess.Popen(f"nohup {cmd} > /data/logs//launcher.txt 2>&1 &", shell=True)
    server_logger.info("sdk stopped successfully.")
    return True

class FunctionMode(Enum):
    ERROR = 0
    IDLE= 1
    COPILOT = 2

class ModeSwitchServer:
    def __init__(self):
        self.function_mode = FunctionMode.COPILOT

    def set_function_mode(self, function_mode):
        self.function_mode = function_mode

    def get_function_mode(self):
        return self.function_mode
    
    def switch_to_idle(self):
        server_logger.info(f"Switching to idle mode, current function mode: {self.function_mode}")
        if self.function_mode == FunctionMode.IDLE:
            return True
        ret = stop_copilot_system()
        if ret:
            self.function_mode = FunctionMode.IDLE
        else:
            self.function_mode = FunctionMode.ERROR
        return ret

    def switch_to_copilot(self, config: ModeSwitchRequest):
        """
        使用launcher启动copilot模式
        """
        server_logger.info(f"Switching to copilot mode, current function mode: {self.function_mode}")
        if self.function_mode == FunctionMode.ERROR:
            return False

        try:
            if start_copilot_system(config):
                self.function_mode = FunctionMode.COPILOT
                return True
            else:
                self.function_mode = FunctionMode.ERROR
                return False
        except subprocess.CalledProcessError as e:
            self.function_mode = FunctionMode.ERROR
            server_logger.error(f"Error: {e}")
            return False

def server():
    clear_archive_log()

    os.makedirs(os.path.join("/data/logs/"), exist_ok=True)
    start_http_server()

    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://10.42.0.101:8848")

    mode_switch_server = ModeSwitchServer()

    server_logger.info("Server is running and waiting for requests...")

    while True:
        message = socket.recv_string()
        archieve_log()

        config = ModeSwitchRequest()
        text_format.Merge(message, config)
        save_mode_witch_request(config)

        if config.mode == Mode.COPILOT:
            if mode_switch_server.switch_to_copilot(config):
                response = ModeSwitchResponse()
                response.success = True
                socket.send_string(text_format.MessageToString(response))
            else:
                response = ModeSwitchResponse()
                response.success = False
                response.error_info = "Switch to 'copilot' failed."
                socket.send_string(text_format.MessageToString(response))
        elif config.mode == Mode.IDLE:
            if mode_switch_server.switch_to_idle():
                response = ModeSwitchResponse()
                response.success = True
                socket.send_string(text_format.MessageToString(response))
            else:
                response = ModeSwitchResponse()
                response.success = False
                response.error_info = "Switch to 'idle' failed."
                socket.send_string(text_format.MessageToString(response))
        else:
            response = ModeSwitchResponse()
            response.success = False
            response.error_info = "Unknown mode request.Now only support copilot and idle mode."
            socket.send_string(text_format.MessageToString(response))

if __name__ == "__main__":
    server()
