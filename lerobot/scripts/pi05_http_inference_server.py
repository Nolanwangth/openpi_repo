#!/usr/bin/env python3
# Copyright 2025 — minimal helper script for local deployment (not part of upstream HF tests).
"""
在 **conda pi05**（已安装 lerobot[pi]、能加载 pi05）里运行，把本地 `pi05_base` 暴露成 HTTP，供 **gdk_env** 用 `requests` 调。

不依赖 FastAPI：仅标准库 http.server。

用法:
  conda activate pi05
  cd /path/to/openpi_repo/lerobot
  export PI05_CHECKPOINT="$PWD/pi05_base"   # 或你的绝对路径
  # tokenizer 离线时（与 policy_preprocessor.json 一致）:
  # export LEROBOT_PI05_TOKENIZER_PATH="$HF_HOME/hub/models--google--paligemma-3b-pt-224/snapshots/<hash>"
  python scripts/pi05_http_inference_server.py --host 0.0.0.0 --port 8765

GDK 侧 POST JSON 见仓库内说明或 print 本文件末尾注释。

请求体 JSON 示例:
{
  "task": "pick up the red block",
  "observation": {
    "state": [32 floats],
    "images": {
      "base_0_rgb": [[[...]]],
      "left_wrist_0_rgb": [[[...]]],
      "right_wrist_0_rgb": [[[...]]]
    }
  },
  "actions_per_chunk": 50
}

图像: 任意 HxWx3 uint8，服务端会按 policy 缩放到 224（与 lerobot async 一致）。
"""
from __future__ import annotations

import argparse
import json
import logging
import os
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

import numpy as np
import torch

from lerobot.async_inference.helpers import raw_observation_to_observation
from lerobot.configs.types import FeatureType
from lerobot.datasets.feature_utils import hw_to_dataset_features
from lerobot.policies.factory import make_pre_post_processors
from lerobot.policies.pi05.modeling_pi05 import PI05Policy
from lerobot.utils.constants import OBS_STR

logger = logging.getLogger("pi05_http")


def _lerobot_features_pi05_base() -> dict:
    """与 pi05_base/config.json 中 32 维 state + 三路相机名一致。"""
    hw: dict = {f"s{i}": float for i in range(32)}
    hw["base_0_rgb"] = (224, 224, 3)
    hw["left_wrist_0_rgb"] = (224, 224, 3)
    hw["right_wrist_0_rgb"] = (224, 224, 3)
    return hw_to_dataset_features(hw, OBS_STR, use_video=False)


def _pick_device() -> str:
    if torch.cuda.is_available():
        return "cuda"
    if getattr(torch.backends, "mps", None) and torch.backends.mps.is_available():
        return "mps"
    return "cpu"


class Pi05HttpState:
    policy: PI05Policy
    preprocessor: object
    postprocessor: object
    lerobot_features: dict
    device: str
    actions_per_chunk: int


STATE = Pi05HttpState()


def _load(ckpt: Path, actions_per_chunk: int) -> None:
    device = _pick_device()
    logger.info("Loading PI05 from %s on %s", ckpt, device)
    policy = PI05Policy.from_pretrained(str(ckpt), local_files_only=True)
    policy.to(device)
    policy.eval()

    pre, post = make_pre_post_processors(
        policy.config,
        pretrained_path=str(ckpt),
        preprocessor_overrides={"device_processor": {"device": device}},
        postprocessor_overrides={"device_processor": {"device": device}},
    )

    STATE.policy = policy
    STATE.preprocessor = pre
    STATE.postprocessor = post
    STATE.lerobot_features = _lerobot_features_pi05_base()
    STATE.device = device
    STATE.actions_per_chunk = actions_per_chunk


def _run_inference(body: dict) -> list[list[float]]:
    task = body.get("task", "")
    obs = body.get("observation") or {}
    state = np.asarray(obs.get("state"), dtype=np.float32).reshape(-1)
    if state.size < 32:
        pad = np.zeros(32, dtype=np.float32)
        pad[: state.size] = state
        state = pad
    else:
        state = state[:32]

    images_in = obs.get("images") or {}
    robot_obs: dict = {f"s{i}": float(state[i]) for i in range(32)}
    robot_obs["task"] = task
    for cam in ("base_0_rgb", "left_wrist_0_rgb", "right_wrist_0_rgb"):
        if cam not in images_in:
            raise ValueError(f"Missing image key: {cam}")
        arr = np.asarray(images_in[cam], dtype=np.uint8)
        if arr.ndim != 3 or arr.shape[-1] != 3:
            raise ValueError(f"{cam} must be HxWx3 uint8, got {arr.shape}")
        robot_obs[cam] = arr

    image_ft = {
        k: v
        for k, v in STATE.policy.config.input_features.items()
        if v.type is FeatureType.VISUAL
    }
    observation = raw_observation_to_observation(robot_obs, STATE.lerobot_features, image_ft)
    observation = STATE.preprocessor(observation)

    n_chunk = int(body.get("actions_per_chunk", STATE.actions_per_chunk))
    n_chunk = max(1, min(n_chunk, STATE.policy.config.chunk_size))

    with torch.inference_mode():
        chunk = STATE.policy.predict_action_chunk(observation)
        if chunk.ndim != 3:
            chunk = chunk.unsqueeze(0)
        chunk = chunk[:, :n_chunk, :]

    _, T, D = chunk.shape
    out: list[list[float]] = []
    for i in range(T):
        row = STATE.postprocessor(chunk[:, i, :])
        out.append(row.detach().float().cpu().numpy().reshape(-1).tolist())
    return out


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt: str, *args) -> None:
        logger.info("%s - %s", self.address_string(), fmt % args)

    def do_GET(self) -> None:  # noqa: N802
        if self.path in ("/", "/health"):
            self.send_response(200)
            self.send_header("Content-Type", "text/plain; charset=utf-8")
            self.end_headers()
            self.wfile.write(b"pi05_http_inference_server OK\nPOST /infer with JSON body.\n")
        else:
            self.send_error(404)

    def do_POST(self) -> None:  # noqa: N802
        if self.path != "/infer":
            self.send_error(404)
            return
        ln = int(self.headers.get("Content-Length", "0"))
        raw = self.rfile.read(ln)
        try:
            body = json.loads(raw.decode("utf-8"))
            actions = _run_inference(body)
            payload = json.dumps({"ok": True, "action_chunk": actions}).encode("utf-8")
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(payload)))
            self.end_headers()
            self.wfile.write(payload)
        except Exception as e:  # noqa: BLE001
            err = json.dumps({"ok": False, "error": str(e)}).encode("utf-8")
            self.send_response(500)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(err)))
            self.end_headers()
            self.wfile.write(err)


def main() -> None:
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")
    p = argparse.ArgumentParser()
    p.add_argument(
        "--checkpoint",
        default=os.environ.get("PI05_CHECKPOINT", str(Path(__file__).resolve().parent.parent / "pi05_base")),
        help="含 config.json / model.safetensors / policy_*processor.json 的目录",
    )
    p.add_argument("--host", default="0.0.0.0")
    p.add_argument("--port", type=int, default=8765)
    p.add_argument("--actions-per-chunk", type=int, default=50)
    args = p.parse_args()

    ckpt = Path(args.checkpoint).resolve()
    if not ckpt.is_dir():
        raise SystemExit(f"Checkpoint 目录不存在: {ckpt}")

    _load(ckpt, args.actions_per_chunk)
    httpd = HTTPServer((args.host, args.port), Handler)
    logger.info("Listening http://%s:%s  POST /infer", args.host, args.port)
    httpd.serve_forever()


if __name__ == "__main__":
    main()
   