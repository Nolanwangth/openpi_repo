#!/usr/bin/env python3
"""
在本机运行：从机器人 /data/record/dlb.db 拉取录制到 ~/Desktop/datasets_raw/

未设置环境变量 ROBOT_SSH_PASS 时，默认使用密码 "1"（与当前 agi@101 一致）。
若已配置 SSH 公钥免密：export ROBOT_SSH_PASS=

只给任务名（与 templates.name 完全一致；不按备注筛选；先建 DEST/任务名/；episode 子目录为库里的 uuid；每条 rsync 后在 Video/ 里生成同名 `<uuid>.mp4`，需本机 ffmpeg）:
  ./pull_record_by_task.py "dig 0513"

任务名包含子串（多模板）:
  ./pull_record_by_task.py --name-contains dig

用法见 --help。
"""
from __future__ import annotations

import argparse
import base64
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from collections import OrderedDict, defaultdict


def sanitize(s: str) -> str:
    s = re.sub(r"[\s/\\:*?\"<>|#]+", "_", s)
    s = re.sub(r"_+", "_", s).strip("_")
    return s or "empty"


def task_root_folder_name(task_name: str) -> str:
    """顶层目录名：尽量保留任务名（含空格），仅替换路径非法字符。"""
    s = re.sub(r'[/\\:*?"<>|#\x00-\x1f]+', "_", task_name).strip()
    return s or "empty"


def ssh_cmd(host: str, user: str, password: str | None) -> list[str]:
    base = ["ssh", "-o", "StrictHostKeyChecking=no", f"{user}@{host}"]
    if password:
        return ["sshpass", "-e", *base]
    return base


def _run_remote_bash(host: str, user: str, password: str | None, payload_b64: str, remote_bash: str) -> subprocess.CompletedProcess[bytes]:
    env = os.environ.copy()
    if password:
        env["SSHPASS"] = password
    return subprocess.run(
        ssh_cmd(host, user, password) + ["bash", "-s", payload_b64],
        input=remote_bash.encode("utf-8"),
        capture_output=True,
        text=False,
        env=env,
    )


def remote_query_recordings_by_template_name(
    host: str, user: str, password: str | None, template_name: str
) -> list[dict[str, str | int]]:
    """按 templates.name 精确匹配（不筛备注）；每条录制一行 JSON：uuid, start_ts, task_id, name, description。"""
    payload_b64 = base64.b64encode(template_name.encode("utf-8")).decode("ascii")
    remote_bash = r"""set -euo pipefail
export PAYLOAD_B64="$1"
python3 - <<'PY'
import base64, json, os, sqlite3, sys
raw = base64.b64decode(os.environ["PAYLOAD_B64"])
name = raw.decode("utf-8")
con = sqlite3.connect("/data/record/dlb.db")
con.row_factory = sqlite3.Row
cur = con.execute(
    "SELECT t.uuid, t.start_ts, t.task_id, m.name, IFNULL(m.description, '') AS description "
    "FROM tasks t JOIN templates m ON t.task_id = m.id "
    "WHERE trim(m.name) = trim(?) ORDER BY t.task_id, t.start_ts ASC",
    (name,),
)
rows = cur.fetchall()
if not rows:
    print("NO_MATCH", file=sys.stderr)
    sys.exit(2)
for r in rows:
    print(json.dumps({
        "uuid": r["uuid"],
        "start_ts": r["start_ts"],
        "task_id": r["task_id"],
        "name": r["name"],
        "description": r["description"],
    }, ensure_ascii=False))
PY
"""
    r = _run_remote_bash(host, user, password, payload_b64, remote_bash)
    out_b = r.stdout.decode("utf-8", errors="replace")
    err_b = r.stderr.decode("utf-8", errors="replace") if r.stderr else ""
    if r.returncode != 0 or "NO_MATCH" in err_b:
        sys.stderr.write(err_b)
        sys.stderr.write(out_b)
        sys.exit(2)
    rows_out: list[dict[str, str | int]] = []
    for line in out_b.splitlines():
        line = line.strip("\r")
        if not line.strip():
            continue
        try:
            rows_out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    if not rows_out:
        sys.stderr.write("未解析到录制行:\n" + out_b + "\n" + err_b)
        sys.exit(3)
    return rows_out


def remote_query_tasks_name_contains(
    host: str, user: str, password: str | None, substr: str
) -> list[dict[str, str | int]]:
    """返回每条 task 一行：task_id, name, description, uuid, start_ts（JSON Lines）。"""
    payload_b64 = base64.b64encode(substr.encode("utf-8")).decode("ascii")
    remote_bash = r"""set -euo pipefail
export PAYLOAD_B64="$1"
python3 - <<'PY'
import base64, json, os, sqlite3, sys
raw = base64.b64decode(os.environ["PAYLOAD_B64"])
substr = raw.decode("utf-8")
con = sqlite3.connect("/data/record/dlb.db")
con.row_factory = sqlite3.Row
cur = con.execute(
    "SELECT t.task_id, m.name, IFNULL(m.description, '') AS description, "
    "t.uuid, t.start_ts FROM tasks t "
    "JOIN templates m ON t.task_id = m.id "
    "WHERE INSTR(LOWER(m.name), LOWER(?)) > 0 "
    "ORDER BY m.name, m.description, t.start_ts ASC",
    (substr,),
)
rows = cur.fetchall()
if not rows:
    print("NO_MATCH", file=sys.stderr)
    sys.exit(2)
for r in rows:
    print(json.dumps({
        "task_id": r["task_id"],
        "name": r["name"],
        "description": r["description"],
        "uuid": r["uuid"],
        "start_ts": r["start_ts"],
    }, ensure_ascii=False))
PY
"""
    r = _run_remote_bash(host, user, password, payload_b64, remote_bash)
    out_b = r.stdout.decode("utf-8", errors="replace")
    err_b = r.stderr.decode("utf-8", errors="replace") if r.stderr else ""
    if r.returncode != 0 or "NO_MATCH" in err_b:
        sys.stderr.write(err_b)
        sys.stderr.write(out_b)
        sys.exit(2)
    rows: list[dict[str, str | int]] = []
    for line in out_b.splitlines():
        line = line.strip("\r")
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    if not rows:
        sys.stderr.write("未解析到任务行:\n" + out_b + "\n" + err_b)
        sys.exit(3)
    return rows


_warned_no_ffmpeg = False


def _ffconcat_quoted_path(path: str) -> str:
    ap = os.path.abspath(path).replace("\\", "/")
    return "'" + ap.replace("'", "'\\''") + "'"


def maybe_encode_head_color_mp4(episode_dir: str, out_mp4: str, fps: float, *, dry_run: bool) -> None:
    """从 episode 下 camera/head/color 的 jpg/jpeg 编码为 out_mp4（通常为 任务大文件夹/Video/<uuid>.mp4）。"""
    global _warned_no_ffmpeg
    if dry_run:
        return
    if not shutil.which("ffmpeg"):
        if not _warned_no_ffmpeg:
            print(
                "  [mp4] 未找到 ffmpeg，跳过 head 预览视频。安装：sudo apt install ffmpeg",
                file=sys.stderr,
            )
            _warned_no_ffmpeg = True
        return

    color_dir = os.path.join(episode_dir, "camera", "head", "color")
    if not os.path.isdir(color_dir):
        return

    paths: list[str] = []
    for name in sorted(os.listdir(color_dir)):
        lower = name.lower()
        if lower.endswith(".jpg") or lower.endswith(".jpeg"):
            paths.append(os.path.join(color_dir, name))
    if not paths:
        print(f"  [mp4] {color_dir} 无 jpg，跳过 {os.path.basename(out_mp4)}", file=sys.stderr)
        return

    os.makedirs(os.path.dirname(out_mp4) or ".", exist_ok=True)
    dur = 1.0 / max(fps, 1e-6)
    fd, list_path = tempfile.mkstemp(prefix="ffconcat_", suffix=".txt", text=True)
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            f.write("ffconcat version 1.0\n")
            for p in paths:
                f.write(f"file {_ffconcat_quoted_path(p)}\n")
                f.write(f"duration {dur:.6f}\n")
            f.write(f"file {_ffconcat_quoted_path(paths[-1])}\n")

        r = subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-hide_banner",
                "-loglevel",
                "error",
                "-f",
                "concat",
                "-safe",
                "0",
                "-i",
                list_path,
                "-c:v",
                "libx264",
                "-pix_fmt",
                "yuv420p",
                "-movflags",
                "+faststart",
                out_mp4,
            ],
            capture_output=True,
            text=True,
        )
        if r.returncode != 0:
            print(f"  [mp4] ffmpeg 失败 ({r.returncode}): {r.stderr or r.stdout}", file=sys.stderr)
            return
        print(f"  [mp4] 已写入 {out_mp4}（{len(paths)} 帧, {fps:g} fps）")
    finally:
        try:
            os.unlink(list_path)
        except OSError:
            pass


def _folder_for_task(name: str, desc: str, task_id: int, used: set[str]) -> str:
    """每个 task 一个顶层文件夹，优先用任务名；重名则加 _tid{id} 或备注后缀。"""
    base = sanitize(name)
    if base not in used:
        used.add(base)
        return base
    base2 = sanitize(f"{name}_{desc}") if desc else f"{base}_tid{task_id}"
    if base2 not in used:
        used.add(base2)
        return base2
    key = f"{base}_tid{task_id}"
    used.add(key)
    return key


def main() -> None:
    p = argparse.ArgumentParser(description="从机器人按任务拉取 /data/record 到本机")
    p.add_argument(
        "task_name",
        nargs="?",
        default=None,
        help="与 templates.name 完全一致；不按备注匹配（与 --name-contains 二选一）",
    )
    p.add_argument(
        "--name-contains",
        metavar="SUBSTR",
        default=None,
        help="拉取所有任务名包含该子串的模板（如 dig）；每个任务一个子目录，目录名为任务名",
    )
    p.add_argument("--dry-run", action="store_true", help="只打印将要 rsync 的路径")
    p.add_argument("--no-mp4", action="store_true", help="传输完成后不根据 camera/head/color 生成 Video/*.mp4")
    p.add_argument(
        "--mp4-fps",
        type=float,
        default=float(os.environ.get("RECORD_PULL_MP4_FPS", "30")),
        metavar="N",
        help="预览视频帧率（默认 30；输出在任务目录 Video/<uuid>.mp4，环境变量 RECORD_PULL_MP4_FPS）",
    )
    p.add_argument("--host", default=os.environ.get("ROBOT_HOST", "10.42.0.101"))
    p.add_argument("--user", default=os.environ.get("ROBOT_USER", "agi"))
    p.add_argument("--dest", default=os.environ.get("DEST_DIR", os.path.expanduser("~/Desktop/datasets_raw")))
    args = p.parse_args()

    if "ROBOT_SSH_PASS" in os.environ:
        password = os.environ["ROBOT_SSH_PASS"] or None
    else:
        password = "1"
    if password and not shutil.which("sshpass"):
        print("需要 sshpass：sudo apt install sshpass；或配置 SSH 公钥后执行 export ROBOT_SSH_PASS= 走免密。", file=sys.stderr)
        sys.exit(1)

    if args.name_contains is not None:
        if args.task_name is not None:
            p.error("使用 --name-contains 时不要写位置参数任务名")
        substr = args.name_contains
        all_rows = remote_query_tasks_name_contains(args.host, args.user, password, substr)
    else:
        if not args.task_name:
            p.error("请提供任务名，或使用 --name-contains")
        all_rows = None

    rsync_e = "sshpass -e ssh -o StrictHostKeyChecking=no" if password else "ssh -o StrictHostKeyChecking=no"
    env = os.environ.copy()
    if password:
        env["SSHPASS"] = password

    os.makedirs(args.dest, exist_ok=True)

    if all_rows is not None:
        # 按 task_id 分组，保证每个「任务模板」一个文件夹
        by_task: "OrderedDict[int, list[dict[str, str | int]]]" = OrderedDict()
        for row in all_rows:
            tid = int(row["task_id"])
            by_task.setdefault(tid, []).append(row)

        used_names: set[str] = set()
        task_folders: dict[int, str] = {}
        for tid, sessions in by_task.items():
            name = str(sessions[0]["name"])
            desc = str(sessions[0]["description"])
            task_folders[tid] = _folder_for_task(name, desc, tid, used_names)

        total = sum(len(s) for s in by_task.values())
        print(f"匹配 {len(by_task)} 个任务模板、共 {total} 条录制 -> {args.dest}")
        for tid, sessions in by_task.items():
            top = os.path.join(args.dest, task_folders[tid])
            video_dir = os.path.join(top, "Video")
            sessions_sorted = sorted(sessions, key=lambda r: int(r["start_ts"]))
            print(f"\n=== 任务 [{sessions_sorted[0]['name']}] -> 目录 {task_folders[tid]}/ ===")
            for row in sessions_sorted:
                uuid = str(row["uuid"]).strip()
                dest = os.path.join(top, uuid)
                src = f"{args.user}@{args.host}:/data/record/{uuid}/"
                print(f"  >>> {uuid} -> {task_folders[tid]}/{uuid}")
                if args.dry_run:
                    print(f"  [dry-run] rsync {src} -> {dest}/")
                    continue
                os.makedirs(dest, exist_ok=True)
                subprocess.run(
                    ["rsync", "-aP", "--partial", "-e", rsync_e, src, dest + "/"],
                    check=True,
                    env=env,
                )
                if not args.no_mp4:
                    out_mp4 = os.path.join(video_dir, f"{uuid}.mp4")
                    maybe_encode_head_color_mp4(dest, out_mp4, args.mp4_fps, dry_run=False)
        print("\n完成。机器人上的源目录未被删除。")
        return

    rows = remote_query_recordings_by_template_name(args.host, args.user, password, args.task_name)
    by_tid: dict[int, list[dict[str, str | int]]] = defaultdict(list)
    for row in rows:
        by_tid[int(row["task_id"])].append(row)

    top_name = task_root_folder_name(args.task_name)
    task_top = os.path.join(args.dest, top_name)
    video_dir = os.path.join(task_top, "Video")
    print(f"匹配到 {len(rows)} 条录制 -> {task_top}")
    for tid in sorted(by_tid.keys(), key=lambda t: min(int(r["start_ts"]) for r in by_tid[t])):
        sess = sorted(by_tid[tid], key=lambda r: int(r["start_ts"]))
        for row in sess:
            uuid = str(row["uuid"]).strip()
            dest = os.path.join(task_top, uuid)
            src = f"{args.user}@{args.host}:/data/record/{uuid}/"
            rel = os.path.join(top_name, uuid)
            print(f"\n>>> {uuid}  ->  {rel}")
            if args.dry_run:
                print(f"[dry-run] rsync {src} -> {dest}/")
                continue
            os.makedirs(dest, exist_ok=True)
            subprocess.run(
                ["rsync", "-aP", "--partial", "-e", rsync_e, src, dest + "/"],
                check=True,
                env=env,
            )
            if not args.no_mp4:
                out_mp4 = os.path.join(video_dir, f"{uuid}.mp4")
                maybe_encode_head_color_mp4(dest, out_mp4, args.mp4_fps, dry_run=False)
    print("\n完成。机器人上的源目录未被删除。")


if __name__ == "__main__":
    main()
