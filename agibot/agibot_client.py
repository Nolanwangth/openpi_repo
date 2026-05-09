#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import io
import json
import socket
import sys
import threading
import time
from pathlib import Path

import numpy as np
from PIL import Image

THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

def encode_jpeg_base64(img_rgb: np.ndarray, quality: int = 85) -> dict:
    pil = Image.fromarray(np.ascontiguousarray(img_rgb), mode="RGB")
    buff = io.BytesIO()
    pil.save(buff, format="JPEG", quality=quality)
    return {"encoding": "jpeg_base64", "data": base64.b64encode(buff.getvalue()).decode("ascii")}


class GdkClient30Hz:
    def __init__(
        self,
        host: str,
        port: int,
        hz: float,
        task: str,
        request_horizon: int = 10,
        execution_horizon: int = 10,
    ):
        self.host = host
        self.port = port
        self.hz = hz
        self.dt = 1.0 / hz
        self.task = task
        self.request_horizon = request_horizon
        self.execution_horizon = execution_horizon

        self.sock = None
        self.read_file = None
        self.bot = None
        self.camera = None
        self.arm_dof = None
        self.hand_dof = None
        self.last_imgs = {"head": None, "left_wrist": None, "right_wrist": None}
        self._lock = threading.Lock()
        self.current_chunk = None
        self.current_chunk_idx = 0
        self.current_chunk_id = -1
        self.exec_counter = 0
        self.last_action = None

        self.request_inflight = False
        self.request_start_exec_counter = 0
        self.request_start_chunk_idx = 0

    def start(self):
        from a2d_sdk.robot import CosineCamera as Camera
        from arm_hand_policy_interface import ARM_DOF, HAND_DOF, MAX_ARM_STEP_RAD, ArmHand30Hz

        self.arm_dof = ARM_DOF
        self.hand_dof = HAND_DOF
        self.sock = socket.create_connection((self.host, self.port), timeout=5.0)
        self.sock.settimeout(None)
        self.read_file = self.sock.makefile("rb")
        # 与手臂一致的单步限幅：chunk 目标跳变时手指也会平滑跟上（仍经 HAND_LO/HI 绝对夹紧）
        self.bot = ArmHand30Hz(max_hand_step_rad=MAX_ARM_STEP_RAD)
        self.camera = Camera(["head", "hand_left", "hand_right"])
        time.sleep(1.0)
        print(f"[client] connected to server {self.host}:{self.port}")
        self._bootstrap_first_chunk_blocking()

    def stop(self):
        if self.camera is not None:
            try:
                self.camera.close()
            except Exception:
                pass
        if self.bot is not None:
            try:
                self.bot.shutdown()
            except Exception:
                pass
        if self.read_file is not None:
            try:
                self.read_file.close()
            except Exception:
                pass
        if self.sock is not None:
            try:
                self.sock.close()
            except Exception:
                pass

    def _get_camera_image(self, cam_key: str, sdk_name: str) -> np.ndarray:
        out = self.camera.get_latest_image(sdk_name)
        if out is not None and out[0] is not None:
            img = out[0]
            if img.ndim == 3 and img.shape[2] == 3:
                self.last_imgs[cam_key] = img
        if self.last_imgs[cam_key] is None:
            self.last_imgs[cam_key] = np.zeros((224, 224, 3), dtype=np.uint8)
        return self.last_imgs[cam_key]

    def _bootstrap_first_chunk_blocking(self) -> None:
        """首包推理完成前主循环会反复下发全零，实机常表现为「完全不动」；启动时同步拉一段 chunk。"""
        payload, _ = self._build_obs_payload()
        req = {
            **payload,
            "type": "chunk_request",
            "inference_delay": 0,
            "execution_horizon": self.execution_horizon,
            "prev_chunk_left_over": None,
        }
        print("[client] waiting for first action_chunk (first infer may take a while)...", flush=True)
        self.sock.sendall((json.dumps(req) + "\n").encode("utf-8"))
        line = self.read_file.readline()
        if not line:
            raise RuntimeError("server closed connection before first chunk")
        resp = json.loads(line.decode("utf-8"))
        if resp.get("type") != "action_chunk":
            raise RuntimeError(f"unexpected first response: {resp.get('type')!r}")
        chunk = np.asarray(resp["actions"], dtype=np.float64)
        if chunk.size == 0 or chunk.shape[0] == 0:
            raise RuntimeError("server returned empty actions")
        self.current_chunk = chunk
        self.current_chunk_idx = 0
        self.current_chunk_id = int(resp.get("chunk_id", -1))
        a0 = chunk[0]
        print(
            f"[client] first chunk ready id={self.current_chunk_id} steps={chunk.shape[0]} "
            f"|arm‖={float(np.linalg.norm(a0[: self.arm_dof])):.3f} "
            f"|hand‖={float(np.linalg.norm(a0[self.arm_dof : self.arm_dof + self.hand_dof])):.3f}",
            flush=True,
        )

    def _build_obs_payload(self):
        st = self.bot.read_state()
        joints = np.asarray(st.arm_rad + st.hand_rad, dtype=np.float32)
        if joints.shape[0] != self.arm_dof + self.hand_dof:
            raise RuntimeError(f"unexpected joint dim {joints.shape[0]}")

        head = self._get_camera_image("head", "head")
        left = self._get_camera_image("left_wrist", "hand_left")
        right = self._get_camera_image("right_wrist", "hand_right")

        return {
            "type": "observation",
            "timestamp": time.time(),
            "task": self.task,
            "joints": joints.tolist(),
            "images": {
                "head": encode_jpeg_base64(head),
                "left_wrist": encode_jpeg_base64(left),
                "right_wrist": encode_jpeg_base64(right),
            },
        }, st

    def run(self):
        tick = 0
        next_t = time.perf_counter()
        while True:
            tic = time.perf_counter()
            payload, st = self._build_obs_payload()

            self._maybe_request_chunk(payload)
            action, chunk_id, progress = self._next_action()
            if action.shape[0] < self.arm_dof + self.hand_dof:
                raise RuntimeError(f"action dim < {self.arm_dof + self.hand_dof}: {action.shape[0]}")

            arm_cmd = action[: self.arm_dof].tolist()
            hand_cmd = action[self.arm_dof : self.arm_dof + self.hand_dof].tolist()
            self.bot.command(arm_cmd, hand_cmd, state=st)

            tick += 1
            if tick % 30 == 0:
                one_cycle_ms = (time.perf_counter() - tic) * 1000.0
                print(
                    f"[client] tick#{tick} loop={one_cycle_ms:.1f}ms "
                    f"chunk={chunk_id} progress={progress} rtc=True inflight={self.request_inflight}"
                )

            next_t += self.dt
            now = time.perf_counter()
            if now < next_t:
                time.sleep(next_t - now)
            else:
                next_t = now

    def _next_action(self):
        with self._lock:
            if self.current_chunk is None or self.current_chunk_idx >= self.current_chunk.shape[0]:
                if self.last_action is None:
                    action = np.zeros((self.arm_dof + self.hand_dof,), dtype=np.float64)
                else:
                    action = self.last_action.copy()
                return action, -1, "none"

            action = self.current_chunk[self.current_chunk_idx].reshape(-1)
            self.current_chunk_idx += 1
            self.exec_counter += 1
            self.last_action = action.copy()
            chunk_id = int(getattr(self, "current_chunk_id", -1))
            progress = f"{self.current_chunk_idx}/{self.current_chunk.shape[0]}"
            return action, chunk_id, progress

    def _need_new_chunk(self):
        if self.current_chunk is None:
            return True
        if self.current_chunk_idx >= self.current_chunk.shape[0]:
            return True
        return self.current_chunk_idx >= self.request_horizon

    def _maybe_request_chunk(self, payload):
        with self._lock:
            if self.request_inflight or not self._need_new_chunk():
                return

            prev_left_over = None
            inference_delay = 0
            if self.current_chunk is not None and self.current_chunk_idx < self.current_chunk.shape[0]:
                prev_left_over = self.current_chunk[self.current_chunk_idx :].tolist()
                inference_delay = int(self.current_chunk_idx)

            req = {
                **payload,
                "type": "chunk_request",
                "inference_delay": inference_delay,
                "execution_horizon": self.execution_horizon,
                "prev_chunk_left_over": prev_left_over,
            }
            self.request_inflight = True
            self.request_start_exec_counter = self.exec_counter
            self.request_start_chunk_idx = self.current_chunk_idx

        t = threading.Thread(target=self._request_chunk_blocking, args=(req,), daemon=True)
        t.start()

    def _request_chunk_blocking(self, req: dict):
        try:
            self.sock.sendall((json.dumps(req) + "\n").encode("utf-8"))
            line = self.read_file.readline()
            if not line:
                raise RuntimeError("server closed connection")
            resp = json.loads(line.decode("utf-8"))
            new_chunk = np.asarray(resp["actions"], dtype=np.float64)
            with self._lock:
                real_delay = max(0, self.exec_counter - self.request_start_exec_counter)
                # RTC：跳过推理期间已执行过的前缀；若整段被跳过则至少保留最后一步，避免 queued=0 卡死
                real_delay = min(real_delay, max(0, new_chunk.shape[0] - 1))
                queued = new_chunk[real_delay:]
                if queued.shape[0] == 0 and new_chunk.shape[0] > 0:
                    queued = new_chunk[-1:]
                    real_delay = new_chunk.shape[0] - 1
                self.current_chunk = queued
                self.current_chunk_idx = 0
                self.current_chunk_id = int(resp.get("chunk_id", -1))
                self.request_inflight = False
                print(
                    f"[client] new chunk={self.current_chunk_id} "
                    f"size={new_chunk.shape[0]} real_delay={real_delay} queued={self.current_chunk.shape[0]}",
                    flush=True,
                )
        except Exception as e:
            with self._lock:
                self.request_inflight = False
            print(f"[client] chunk request failed: {e}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--host", type=str, default="127.0.0.1")
    parser.add_argument("--port", type=int, default=9000)
    parser.add_argument("--hz", type=float, default=30.0)
    parser.add_argument("--task", type=str, default="pick up the torque gun")
    parser.add_argument("--request-horizon", type=int, default=10)
    parser.add_argument("--execution-horizon", type=int, default=10)
    args = parser.parse_args()

    cli = GdkClient30Hz(
        host=args.host,
        port=args.port,
        hz=args.hz,
        task=args.task,
        request_horizon=args.request_horizon,
        execution_horizon=args.execution_horizon,
    )
    cli.start()
    try:
        cli.run()
    except KeyboardInterrupt:
        pass
    finally:
        cli.stop()
        print("[done] gdk client stopped")


if __name__ == "__main__":
    main()
