#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import io
import json
import socket
import threading
import time
from dataclasses import dataclass
from pathlib import Path

import numpy as np
import torch
from PIL import Image

from lerobot.configs.types import FeatureType, PolicyFeature
from lerobot.policies.factory import make_pre_post_processors
from lerobot.policies.pi05.configuration_pi05 import PI05Config
from lerobot.policies.pi05.modeling_pi05 import PI05Policy
from lerobot.policies.rtc.configuration_rtc import RTCConfig
from lerobot.processor.normalize_processor import NormalizerProcessorStep
from lerobot.utils.constants import ACTION, OBS_STATE


def choose_device() -> str:
    if torch.cuda.is_available():
        return "cuda"
    return "cpu"

'''
定义Observation类,用于存储观察到的状态和任务
joints_26: np.ndarray,26维关节角度
head_rgb: np.ndarray,头部RGB图像
left_wrist_rgb: np.ndarray,左手腕RGB图像
right_wrist_rgb: np.ndarray,右手腕RGB图像
timestamp: float,时间戳
task: str,任务名称
'''
@dataclass
class Observation:
    joints_26: np.ndarray
    head_rgb: np.ndarray
    left_wrist_rgb: np.ndarray
    right_wrist_rgb: np.ndarray
    timestamp: float
    task: str

# 解码图像数据为numpy数组
def decode_image_payload(payload) -> np.ndarray: 
    # 如果 payload 是列表，假定其已为 HxWx3 的 np.uint8 数组
    if isinstance(payload, list):   
        img = np.asarray(payload, dtype=np.uint8) 
        if img.ndim != 3 or img.shape[2] != 3:
            raise ValueError("image list payload must be HxWx3")
        return img

    # 如果 payload 不是 dict，则报错
    if not isinstance(payload, dict):
        raise ValueError("image payload must be dict or HxWx3 list")

    # 获取编码方式
    encoding = payload.get("encoding")
    if encoding == "jpeg_base64":
        # jpeg_base64: base64 解码后，用 PIL 读取成 RGB 格式
        raw = base64.b64decode(payload["data"])
        img = Image.open(io.BytesIO(raw)).convert("RGB")
        return np.asarray(img, dtype=np.uint8)

    if encoding == "raw_uint8_hwc":
        # raw_uint8_hwc: data 已经是 np.uint8 的扁平数组，再 reshape 成原有尺寸
        arr = np.asarray(payload["data"], dtype=np.uint8)
        shape = payload["shape"]
        return arr.reshape(shape)

    # 不支持的编码类型
    raise ValueError(f"unsupported image encoding: {encoding}")




def load_policy(model_path: Path, device: str, execution_horizon: int) -> tuple[PI05Policy, any, any]:
    """
    加载 PI05 策略模型及其预处理、后处理器。

    参数:
        model_path (Path): 模型权重目录路径，内部需包含 config.json。
        device (str): 推理设备（如 'cpu', 'cuda', 'mps'）。
        execution_horizon (int): RTC 策略最大前瞻步数。

    返回:
        (policy, preprocessor, postprocessor)
        policy: PI05Policy 模型实例
        preprocessor: 适用于该模型的预处理器（包含标准化、图像转化等步骤）
        postprocessor: 适用于该模型的后处理器（包含去标准化等步骤）
    """

    # 读取模型配置文件 config.json
    config_path = model_path / "config.json"
    config_data = json.loads(config_path.read_text())
    # 去除 config.json 中类型字段, 防止与类参数冲突
    config_data.pop("type", None)

    # 内部函数：将 input_features/output_features 字典从原始 JSON 格式转为 PolicyFeature 配置
    def _convert_features(raw_features: dict) -> dict[str, PolicyFeature]:
        converted = {}
        for key, feat in raw_features.items():
            # type: FeatureType (如 VISUAL/STATE/ACTION)，shape: 元组格式
            converted[key] = PolicyFeature(
                type=FeatureType(feat["type"]),
                shape=tuple(feat["shape"]),
            )
        return converted

    # 配置输入、输出特征
    config_data["input_features"] = _convert_features(config_data["input_features"])
    config_data["output_features"] = _convert_features(config_data["output_features"])

    # 组装 PI05Config
    cfg = PI05Config(**config_data)
    # 推理用设备赋值（如 cpu/cuda/mps）
    cfg.device = device
    # RTC 配置，控制策略的实时纠偏、最大引导步数等信息
    cfg.rtc_config = RTCConfig(
        enabled=True,                     # 启用 RTC
        execution_horizon=execution_horizon,  # 最大执行步数
        max_guidance_weight=10.0,         # 最大引导权重
        debug=False,                      # 关闭 debug
    )

    # 加载模型及权重，设置为 eval 模式（推理，非训练）
    policy = PI05Policy.from_pretrained(
        str(model_path),      # 权重目录
        config=cfg,           # 已填充的配置
        local_files_only=True,# 不从远端下载（本地加载）
        strict=False,         # 配置和权重部分兼容即可
    )
    policy.eval()

    # 根据模型配置动态创建预处理器和后处理器（如归一化、设备切换等）
    preprocessor, postprocessor = make_pre_post_processors(
        policy.config,
        pretrained_path=str(model_path),
        preprocessor_overrides={"device_processor": {"device": device}},    # 预处理器 device 设为目标推理设备
        postprocessor_overrides={"device_processor": {"device": "cpu"}},    # 后处理器 device 固定在 cpu
    )

    # 返回模型、预处理器、后处理器
    return policy, preprocessor, postprocessor


class Pi05Session:
    def __init__(self, policy: PI05Policy, preprocessor, postprocessor, default_task: str):
        self.policy = policy
        self.preprocessor = preprocessor
        self.postprocessor = postprocessor
        self.default_task = default_task

        self._latest_chunk_id = 0
        self._action_normalizer_step: NormalizerProcessorStep | None = None
        for step in preprocessor.steps:
            if isinstance(step, NormalizerProcessorStep):
                self._action_normalizer_step = step
                break
        if self._action_normalizer_step is None:
            raise RuntimeError("NormalizerProcessorStep missing from PI05 preprocessor")

    def _prev_chunk_left_over_to_model_space(self, prev_left_over: list) -> torch.Tensor:
        """Client sends executed-but-skipped actions in robot (denormalized) space; RTC needs [-1,1] quantile space."""
        t = torch.tensor(prev_left_over, dtype=torch.float32)
        if t.ndim == 1:
            t = t.unsqueeze(0)
        t_steps, d_in = t.shape
        action_dim = self.policy.config.output_features[ACTION].shape[0]
        if d_in < action_dim:
            t = torch.cat([t, torch.zeros(t_steps, action_dim - d_in, dtype=t.dtype)], dim=-1)
        elif d_in > action_dim:
            t = t[:, :action_dim]
        device = next(self.policy.parameters()).device
        rows = []
        for i in range(t_steps):
            row = t[i : i + 1].to(device)
            rows.append(self._action_normalizer_step._normalize_action(row, inverse=False))
        return torch.cat(rows, dim=0).unsqueeze(0)

    def _build_batch(self, obs: Observation):
        state_dim = int(self.policy.config.input_features[OBS_STATE].shape[0])
        state_vec = np.zeros((state_dim,), dtype=np.float32)
        j = np.asarray(obs.joints_26, dtype=np.float32).reshape(-1)
        n = min(j.shape[0], state_dim)
        state_vec[:n] = j[:n]

        def img_to_tensor(img: np.ndarray) -> torch.Tensor:
            arr = np.ascontiguousarray(img, dtype=np.uint8)
            return torch.from_numpy(arr.copy()).permute(2, 0, 1).float() / 255.0

        task = obs.task if obs.task else self.default_task
        batch = {
            "observation.state": torch.from_numpy(state_vec),
            "observation.images.base_0_rgb": img_to_tensor(obs.head_rgb),
            "observation.images.left_wrist_0_rgb": img_to_tensor(obs.left_wrist_rgb),
            "observation.images.right_wrist_0_rgb": img_to_tensor(obs.right_wrist_rgb),
            "task": task,
        }
        return self.preprocessor(batch)

    def infer_chunk(
        self,
        obs: Observation,
        inference_delay: int = 0,
        prev_chunk_left_over: torch.Tensor | None = None,
        execution_horizon: int | None = None,
    ) -> tuple[np.ndarray, int, float]:
        tic = time.perf_counter()
        batch = self._build_batch(obs)
        with torch.no_grad():
            action_chunk = self.policy.predict_action_chunk(
                batch,
                inference_delay=inference_delay,
                prev_chunk_left_over=prev_chunk_left_over,
                execution_horizon=(
                    execution_horizon
                    if execution_horizon is not None
                    else self.policy.config.rtc_config.execution_horizon
                ),
            )
        # Model outputs actions in training-normalized space; must unnormalize before robot cmds.
        _, chunk_size, _ = action_chunk.shape
        processed_actions = []
        for i in range(chunk_size):
            single = action_chunk[:, i, :]
            processed_actions.append(self.postprocessor(single))
        action_tensor = torch.stack(processed_actions, dim=1).squeeze(0)
        action_dim = int(self.policy.config.output_features[ACTION].shape[0])
        chunk = action_tensor[:, :action_dim].detach().float().cpu().numpy().astype(np.float32)
        infer_ms = (time.perf_counter() - tic) * 1000.0
        self._latest_chunk_id += 1
        return chunk, self._latest_chunk_id, infer_ms


def parse_observation_msg(msg: dict, default_task: str) -> Observation:
    joints = np.asarray(msg["joints"], dtype=np.float32).reshape(-1)
    if joints.shape[0] < 26:
        raise ValueError(f"joints dims must be >=26, got {joints.shape[0]}")
    images = msg["images"]
    return Observation(
        joints_26=joints[:26],
        head_rgb=decode_image_payload(images["head"]),
        left_wrist_rgb=decode_image_payload(images["left_wrist"]),
        right_wrist_rgb=decode_image_payload(images["right_wrist"]),
        timestamp=float(msg.get("timestamp", time.time())),
        task=str(msg.get("task", default_task)),
    )


def handle_client(conn: socket.socket, addr, session: Pi05Session):
    print(f"[tcp] client connected: {addr}")
    read_file = conn.makefile("rb")
    msg_count = 0
    try:
        while True:
            line = read_file.readline()
            if not line:
                break
            msg = json.loads(line.decode("utf-8"))
            if msg.get("type", "chunk_request") != "chunk_request":
                continue

            obs = parse_observation_msg(msg, default_task=session.default_task)

            inference_delay = int(msg.get("inference_delay", 0))
            execution_horizon = msg.get("execution_horizon")
            prev_left_over = msg.get("prev_chunk_left_over")
            prev_left_over_t = None
            if prev_left_over is not None:
                prev_left_over_t = session._prev_chunk_left_over_to_model_space(prev_left_over)

            chunk, chunk_id, infer_ms = session.infer_chunk(
                obs=obs,
                inference_delay=inference_delay,
                prev_chunk_left_over=prev_left_over_t,
                execution_horizon=execution_horizon,
            )
            print(
                f"[infer] chunk#{chunk_id} ready len={chunk.shape[0]} "
                f"infer={infer_ms:.1f}ms rtc=on subtask=None"
            )

            resp = {
                "type": "action_chunk",
                "timestamp": time.time(),
                "actions": chunk.tolist(),
                "rtc_enabled": True,
                "chunk_id": chunk_id,
                "chunk_size": int(chunk.shape[0]),
            }
            conn.sendall((json.dumps(resp) + "\n").encode("utf-8"))
            msg_count += 1
            if msg_count % 30 == 0:
                print(f"[tcp] served requests={msg_count} last_chunk={chunk_id}")
    except Exception as e:
        print(f"[tcp] client error {addr}: {e}")
    finally:
        try:
            read_file.close()
        except Exception:
            pass
        try:
            conn.close()
        except Exception:
            pass
        print(f"[tcp] client disconnected: {addr}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default="0.0.0.0")
    parser.add_argument("--port", type=int, default=9000)
    parser.add_argument("--model-path", type=str, default="lerobot/pi05_base")
    parser.add_argument("--task", type=str, default="pick up the torque gun")
    parser.add_argument("--execution-horizon", type=int, default=50)
    parser.add_argument("--blend-steps", type=int, default=40)
    args = parser.parse_args()

    model_path = Path(args.model_path).resolve()
    device = choose_device()
    print(f"[init] model={model_path}, device={device}, task={args.task}")

    policy, preprocessor, postprocessor = load_policy(
        model_path=model_path, device=device, execution_horizon=args.execution_horizon
    )
    session = Pi05Session(
        policy=policy,
        preprocessor=preprocessor,
        postprocessor=postprocessor,
        default_task=args.task,
    )

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((args.host, args.port))
    server.listen(1)
    print(f"[serve] pi05 tcp server listening on {args.host}:{args.port}")
    try:
        while True:
            conn, addr = server.accept()
            handle_client(conn, addr, session)
    except KeyboardInterrupt:
        pass
    finally:
        server.close()
        print("[done] server stopped")


if __name__ == "__main__":
    main()
