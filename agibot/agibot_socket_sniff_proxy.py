#!/usr/bin/env python3
"""
在 client 与 agibot_pi05_* 服务之间插入 TCP 代理，按行记录 JSON 协议并做维度/字段摘要。

协议（与 agibot_client / agibot_pi05_mock_trajectory_server 一致）：
  - 每条消息一行 UTF-8 JSON，以 \\n 结尾。
  - client → server: type == \"chunk_request\"
  - server → client: type == \"action_chunk\"

用法示例::

  # 终端 A：mock 服务仍监听 9000
  python agibot/agibot_pi05_mock_trajectory_server.py --host 127.0.0.1 --port 9000

  # 终端 B（本脚本）：监听 9100，转发到 9000
  python agibot/agibot_socket_sniff_proxy.py --listen-port 9100 --upstream-port 9000

  # 终端 C：client 指向代理端口
  python agibot/agibot_client.py --host 127.0.0.1 --port 9100 ...

若不想改 client 端口，也可把 mock 服务改到 9001，代理占 9000 并转发到 9001。
"""

from __future__ import annotations

import argparse
import base64
import json
import socket
import sys
import threading
import time
from pathlib import Path
from typing import Any

THIS_DIR = Path(__file__).resolve().parent
if str(THIS_DIR) not in sys.path:
    sys.path.insert(0, str(THIS_DIR))

try:
    from arm_hand_policy_interface import ARM_DOF, HAND_DOF

    _EXPECTED_JOINTS = int(ARM_DOF + HAND_DOF)
except Exception:
    _EXPECTED_JOINTS = 26


def _summarize_array_list(name: str, data: Any, *, expect_row: int | None) -> list[str]:
    lines: list[str] = []
    if not isinstance(data, list):
        lines.append(f"  {name}: (not a list) type={type(data).__name__}")
        return lines
    if len(data) == 0:
        lines.append(f"  {name}: [] (empty)")
        return lines
    if isinstance(data[0], list):
        n_rows = len(data)
        n_cols = len(data[0]) if data[0] is not None else 0
        lines.append(f"  {name}: shape≈({n_rows}, {n_cols}) (list-of-lists)")
        if expect_row is not None and n_cols != expect_row:
            lines.append(f"    ⚠ row width {n_cols} != expected {expect_row}")
        if n_rows > 0 and isinstance(data[0], list) and len(data[0]) > 0:
            r0 = data[0]
            try:
                xs = [float(x) for x in r0[: min(8, len(r0))]]
                lines.append(f"    first_row[:8]={xs}")
            except (TypeError, ValueError):
                lines.append(f"    first_row (non-numeric preview)={r0[:3]!r}...")
    else:
        lines.append(f"  {name}: 1D len={len(data)}")
        if expect_row is not None and len(data) != expect_row:
            lines.append(f"    ⚠ len {len(data)} != expected {expect_row}")
        try:
            head = [float(x) for x in data[:8]]
            lines.append(f"    head[:8]={head}")
        except (TypeError, ValueError):
            pass
    return lines


def _jpeg_magic_from_b64_prefix(raw: str, *, prefix_chars: int = 128) -> bool | None:
    """仅解码 base64 前缀，避免每帧对整图 decode（30Hz×三路相机很重）。"""
    chunk = raw[:prefix_chars]
    if not chunk:
        return None
    pad = "=" * ((4 - len(chunk) % 4) % 4)
    try:
        blob = base64.b64decode(chunk + pad, validate=True)
    except Exception:
        return None
    return len(blob) >= 3 and blob[:3] == b"\xff\xd8\xff"


def _summarize_images(images: Any, *, max_b64_preview: int) -> list[str]:
    lines: list[str] = []
    if not isinstance(images, dict):
        lines.append(f"  images: (not dict) {type(images).__name__}")
        return lines
    for k, v in images.items():
        if not isinstance(v, dict):
            lines.append(f"  images[{k!r}]: not dict")
            continue
        enc = v.get("encoding")
        raw = v.get("data")
        if not isinstance(raw, str):
            lines.append(f"  images[{k!r}]: encoding={enc!r} data_type={type(raw).__name__}")
            continue
        n = len(raw)
        jpeg_hint = _jpeg_magic_from_b64_prefix(raw)
        tip = raw[:max_b64_preview] + ("…" if n > max_b64_preview else "")
        jmsg = "unknown" if jpeg_hint is None else str(jpeg_hint)
        lines.append(
            f"  images[{k!r}]: encoding={enc!r} b64_len={n} "
            f"jpeg_prefix_magic_ok={jmsg} b64_head={tip!r}"
        )
    return lines


def _log_chunk_request(seq: int, msg: dict, *, expected_joints: int) -> None:
    ts = time.strftime("%H:%M:%S")
    print(f"\n[{ts}] >>> C→S #{seq} chunk_request", flush=True)
    print(f"  task={msg.get('task')!r}", flush=True)
    print(f"  timestamp={msg.get('timestamp')}", flush=True)
    print(f"  inference_delay={msg.get('inference_delay')!r} execution_horizon={msg.get('execution_horizon')!r}", flush=True)
    pco = msg.get("prev_chunk_left_over")
    if pco is None:
        print("  prev_chunk_left_over=None", flush=True)
    elif isinstance(pco, list):
        if len(pco) == 0:
            print("  prev_chunk_left_over=[]", flush=True)
        elif isinstance(pco[0], list):
            print(f"  prev_chunk_left_over: {len(pco)} rows x {len(pco[0])} cols", flush=True)
        else:
            print(f"  prev_chunk_left_over: flat len={len(pco)}", flush=True)
    else:
        print(f"  prev_chunk_left_over: unexpected type {type(pco).__name__}", flush=True)

    joints = msg.get("joints")
    for line in _summarize_array_list("joints", joints, expect_row=expected_joints):
        print(line, flush=True)

    for line in _summarize_images(msg.get("images"), max_b64_preview=48):
        print(line, flush=True)

    extra = set(msg.keys()) - {
        "type",
        "task",
        "timestamp",
        "joints",
        "images",
        "inference_delay",
        "execution_horizon",
        "prev_chunk_left_over",
    }
    if extra:
        print(f"  (extra keys) {sorted(extra)}", flush=True)


def _log_action_chunk(seq: int, msg: dict, *, expected_action_width: int) -> None:
    ts = time.strftime("%H:%M:%S")
    print(f"\n[{ts}] <<< S→C #{seq} action_chunk", flush=True)
    print(
        f"  chunk_id={msg.get('chunk_id')!r} chunk_size(field)={msg.get('chunk_size')!r} "
        f"rtc_enabled={msg.get('rtc_enabled')!r}",
        flush=True,
    )
    print(f"  timestamp={msg.get('timestamp')}", flush=True)
    actions = msg.get("actions")
    for line in _summarize_array_list("actions", actions, expect_row=expected_action_width):
        print(line, flush=True)
    if isinstance(actions, list) and actions and isinstance(actions[0], list):
        n_rows = len(actions)
        n_cols = len(actions[0])
        cs = msg.get("chunk_size")
        if cs is not None and int(cs) != n_rows:
            print(f"  ⚠ chunk_size field {cs!r} != inferred rows {n_rows}", flush=True)
    extra = set(msg.keys()) - {"type", "timestamp", "actions", "rtc_enabled", "chunk_id", "chunk_size"}
    if extra:
        print(f"  (extra keys) {sorted(extra)}", flush=True)


def _relay_lines(
    label: str,
    src: socket.socket,
    dst: socket.socket,
    *,
    direction: str,
    counter: dict[str, int],
    expected_joints: int,
    log_raw_on_error: bool,
    raw_cap: int,
) -> None:
    """direction: 'c2s' or 's2c' — 按行读取并转发。"""
    f = src.makefile("rb")

    try:
        while True:
            line = f.readline()
            if not line:
                break
            dst.sendall(line)
            text = line.decode("utf-8", errors="replace")
            if not text.endswith("\n"):
                print(f"[{label}] incomplete line (no newline), len={len(line)}", flush=True)
            try:
                msg = json.loads(text)
            except json.JSONDecodeError as e:
                print(f"[{label}] JSON decode error ({direction}): {e}", flush=True)
                if log_raw_on_error:
                    preview = text[:raw_cap].replace("\n", "\\n")
                    print(f"  raw_head={preview!r}", flush=True)
                continue

            counter[direction] += 1
            seq = counter[direction]
            mtype = msg.get("type")
            if direction == "c2s" and mtype == "chunk_request":
                _log_chunk_request(seq, msg, expected_joints=expected_joints)
            elif direction == "s2c" and mtype == "action_chunk":
                _log_action_chunk(seq, msg, expected_action_width=expected_joints)
            else:
                print(f"\n[{label}] {direction} #{seq} type={mtype!r} (unexpected for this direction)", flush=True)
    finally:
        try:
            f.close()
        except Exception:
            pass
        try:
            dst.shutdown(socket.SHUT_WR)
        except Exception:
            pass


def _handle_pair(
    client_sock: socket.socket,
    client_addr,
    *,
    upstream_host: str,
    upstream_port: int,
    expected_joints: int,
    log_raw_on_error: bool,
    raw_cap: int,
) -> None:
    label = f"{client_addr[0]}:{client_addr[1]}"
    print(f"[proxy] client connected {label} -> {upstream_host}:{upstream_port}", flush=True)
    up: socket.socket | None = None
    try:
        up = socket.create_connection((upstream_host, upstream_port), timeout=10.0)
    except OSError as e:
        print(f"[proxy] upstream connect failed: {e}", flush=True)
        client_sock.close()
        return

    counter: dict[str, int] = {"c2s": 0, "s2c": 0}

    t1 = threading.Thread(
        target=_relay_lines,
        args=(label, client_sock, up,),
        kwargs={
            "direction": "c2s",
            "counter": counter,
            "expected_joints": expected_joints,
            "log_raw_on_error": log_raw_on_error,
            "raw_cap": raw_cap,
        },
        daemon=True,
    )
    t2 = threading.Thread(
        target=_relay_lines,
        args=(label, up, client_sock,),
        kwargs={
            "direction": "s2c",
            "counter": counter,
            "expected_joints": expected_joints,
            "log_raw_on_error": log_raw_on_error,
            "raw_cap": raw_cap,
        },
        daemon=True,
    )
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    try:
        client_sock.close()
    except Exception:
        pass
    try:
        up.close()
    except Exception:
        pass
    print(f"[proxy] session end {label}", flush=True)


def main() -> None:
    p = argparse.ArgumentParser(description="TCP 行协议嗅探代理（chunk_request / action_chunk）")
    p.add_argument("--listen-host", type=str, default="0.0.0.0")
    p.add_argument("--listen-port", type=int, default=9100)
    p.add_argument("--upstream-host", type=str, default="127.0.0.1")
    p.add_argument("--upstream-port", type=int, default=9000)
    p.add_argument(
        "--expected-joint-dim",
        type=int,
        default=_EXPECTED_JOINTS,
        help=f"关节/动作向量期望维度（默认 {_EXPECTED_JOINTS}，来自 arm_hand_policy_interface 若可导入）",
    )
    p.add_argument("--log-raw-on-json-error", action="store_true", help="JSON 解析失败时打印原始行前缀")
    p.add_argument("--raw-cap", type=int, default=400, help="原始行前缀最大字符数")
    args = p.parse_args()

    srv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    srv.bind((args.listen_host, args.listen_port))
    srv.listen(8)
    print(
        f"[proxy] listening {args.listen_host}:{args.listen_port} -> "
        f"{args.upstream_host}:{args.upstream_port} | expected_joint_dim={args.expected_joint_dim}",
        flush=True,
    )
    try:
        while True:
            conn, addr = srv.accept()
            threading.Thread(
                target=_handle_pair,
                args=(conn, addr),
                kwargs={
                    "upstream_host": args.upstream_host,
                    "upstream_port": args.upstream_port,
                    "expected_joints": args.expected_joint_dim,
                    "log_raw_on_error": args.log_raw_on_json_error,
                    "raw_cap": args.raw_cap,
                },
                daemon=True,
            ).start()
    except KeyboardInterrupt:
        pass
    finally:
        srv.close()
        print("[proxy] stopped", flush=True)


if __name__ == "__main__":
    main()
