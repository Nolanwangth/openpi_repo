#!/usr/bin/env python3
"""
Convert AgiBot GDK `record/<uuid>/` bags to LeRobot v3 dataset for PI05 training.

**运行示例**（默认已含 prompt，重导同一路径需 `--overwrite`）::

    python agi2lerobot_dataset.py --overwrite
    python agi2lerobot_dataset.py --prompt "other task" --out-root path/to/other

**本脚本流程（与你的预期一致）**  
1. 扫描 `--record-root` 下每个 UUID 子目录，**统计**含 `record/raw_joints.h5` 的 episode 条数（可选 `--stats-only` 只打印清单后退出）。  
2. 对每条 episode **全部**写入同一个 LeRobot 数据集（PI05 训练：`observation.state` / `action` 26 维 + 三路图像键名与 `Pi05Policy` 一致）。  
3. 图像：**按时间戳就近**取该条下的原始文件并 **copy** 到数据集——头部来自 `camera/<head>/…/*.jpg`，手腕来自 `camera/hand_left/color/*.jpg` 与 `camera/hand_right/color/*.jpg`（与 `agibot_client` 三路相机一致；亦接受同目录下的 `.jpeg`/`.png`）。  
4. 语言任务：默认 `--prompt` 为 ``pick up the torque gun``（与 `agibot_pi05_server.py` 常见 `--task` 一致），写入全部帧；传 ``--prompt ""`` 则改按各条 ``meta_info.json`` 的 ``text`` → ``task_id`` → ``--task-default``。

**必须与部署代码一致（验收标准）**  
实现细节以源码为准；下方摘要与文件中「部署约定」注释块，与 `agibot/agibot_client.py`、`agibot/agibot_pi05_server.py` 逐项对齐。

1. **26 维 `joints` / `observation.state` / `action`**  
   与客户端 `GdkClient30Hz._build_obs_payload()` 相同：`arm_rad(14) + hand_rad(12)`，手指顺序见
   `agibot/arm_hand_policy_interface.py` / `agibot/readme.md`（先左后右，每只手 6 维）。

2. **三路图像 → LeRobot 键名（与 `Pi05Session._build_batch()` 一致）**  
   - 消息里 `images["head"]` / SDK `CosineCamera("head")` → `observation.images.base_0_rgb`  
   - `images["left_wrist"]` / `"hand_left"` → `observation.images.left_wrist_0_rgb`  
   - `images["right_wrist"]` / `"hand_right"` → `observation.images.right_wrist_0_rgb`  
   部署链路上 **解码后仍是「原始 H×W」**：`parse_observation_msg()` → `decode_image_payload()` 得到与 JPEG 一致的 `uint8` HWC；`img_to_tensor` 只做 `/255` 与维度变换，**不在 `agibot_pi05_server.py` 里改分辨率**。  
   缩放到 `pi05_base` 的 224 发生在 **LeRobot PI05 的 `preprocessor` / 模型 `resize_with_pad`**（与线上一致）。

3. **本脚本：原样拷贝 record 里的 JPEG/PNG（不缩放、不重编码）**  
   与线上一致：部署侧解码后为相机原始 H×W；PI05 在训练/推理时由 `resize_with_pad` 等到 `config.image_resolution`（如 224）。  
   数据集落盘路径扩展名与源文件一致（多为 `.jpg`）；**缺图时** 写入与 metadata 一致的纯色 JPEG 占位（仅该情况会编码）。

4. **30 Hz**  
   与 `GdkClient30Hz` 控制周期一致；时间轴由 `raw_joints.h5` 重采样到 30Hz。

5. **磁盘格式**  
   对 record 帧 **字节级 copy**；占位为 JPEG。训练读 Parquet 内嵌图即可。默认 **保留** ``images/`` 下各集文件（``--no-keep-images-on-disk`` 可改为与 LeRobot 原生一致、每集 save 后删掉以省空间）。

GDK `record` 下：`head_center_fisheye` 常为 H.265，无逐帧 JPEG；头部 RGB 序列一般在 `camera/head/color/`。
"""
from __future__ import annotations

import argparse
import json
import os
import shutil
import sys
from pathlib import Path

import numpy as np
from PIL import Image

# LeRobot lives under ./lerobot in this repo
_REPO_ROOT = Path(__file__).resolve().parent
_LEROBOT_SRC = _REPO_ROOT / "lerobot" / "src"
if _LEROBOT_SRC.is_dir() and str(_LEROBOT_SRC) not in sys.path:
    sys.path.insert(0, str(_LEROBOT_SRC))

from lerobot.datasets.lerobot_dataset import LeRobotDataset  # noqa: E402
from lerobot.utils.constants import ACTION, OBS_STR  # noqa: E402


class NativeCopyLeRobotDataset(LeRobotDataset):
    """Write image features by copying source files when `frame[key]` is a PIL image with `filename`.

    Paths use the source suffix (``.jpg`` / ``.png`` / …). NumPy / 无 filename 的 PIL 走父类编码（占位黑图 → JPEG）。

    LeRobot 默认在每个 ``save_episode`` 后 **删除** 本集 ``images/`` 下的文件（像素已嵌进 Parquet）。
    设置 ``keep_images_on_disk=True`` 可保留磁盘上的 jpg/png（约与 Parquet 内嵌重复占盘）。
    """

    keep_images_on_disk: bool = True

    def clear_episode_buffer(self, delete_images: bool = True) -> None:
        if getattr(self, "keep_images_on_disk", False):
            delete_images = False
        super().clear_episode_buffer(delete_images=delete_images)

    def add_frame(self, frame: dict) -> None:
        self._native_ext: dict[str, str] = {}
        for key in frame:
            if key in self.features and self.features[key]["dtype"] == "image":
                v = frame[key]
                if isinstance(v, Image.Image):
                    fn = getattr(v, "filename", None)
                    if fn and Path(fn).is_file():
                        self._native_ext[key] = Path(fn).suffix.lower() or ".jpg"
        try:
            super().add_frame(frame)
        finally:
            self._native_ext = {}

    def _get_image_file_path(self, episode_index: int, image_key: str, frame_index: int) -> Path:
        p = super()._get_image_file_path(episode_index, image_key, frame_index)
        ext = getattr(self, "_native_ext", {}).get(image_key)
        if ext:
            return p.with_suffix(ext)
        return p.with_suffix(".jpg")

    def _save_image(self, image, fpath: Path, compress_level: int = 1) -> None:
        if isinstance(image, Image.Image):
            fp = getattr(image, "filename", None)
            if fp:
                src = Path(fp)
                try:
                    if src.is_file():
                        dst = fpath.resolve()
                        if src.resolve() != dst:
                            shutil.copy2(src, fpath)
                            return
                except OSError:
                    pass
        super()._save_image(image, fpath, compress_level=compress_level)


# ---------------------------------------------------------------------------
# 部署约定 — 以下两条为唯一权威，本脚本字段/语义必须与之一致（改前先对读源码）
#
# agibot/agibot_client.py
#   • 关节：GdkClient30Hz._build_obs_payload — joints = np.asarray(st.arm_rad + st.hand_rad)
#     长度 ARM_DOF+HAND_DOF (=26)，dtype float32，经 JSON 发往服务端。
#   • 相机：start() 里 CosineCamera(["head", "hand_left", "hand_right"])；
#     _get_camera_image("head","head") / ("left_wrist","hand_left") / ("right_wrist","hand_right")。
#   • 消息 images 键名："head"、"left_wrist"、"right_wrist"（encode_jpeg_base64，线上 JPEG）。
#   • 频率：默认 --hz 30.0，dt = 1/hz（与数据集 fps=30 对齐）。
#   • 执行：run() 里 action[:arm_dof] 臂、action[arm_dof:arm_dof+hand_dof] 手，与 joints 维序一致。
#
# agibot/agibot_pi05_server.py
#   • 解析：parse_observation_msg — joints_26 = joints[:26]；
#     head_rgb/left_wrist_rgb/right_wrist_rgb = decode_image_payload(images["head"|...])。
#   • 推理批：Pi05Session._build_batch — state_32[:26] = obs.joints_26（模型用 32 维，前 26 为实机语义）；
#     img_to_tensor：HWC uint8 → CHW float /255，不改 H/W。
#   • LeRobot 键名（与 pi05 训练一致）：observation.images.base_0_rgb ← head_rgb；
#     left_wrist_0_rgb ← left_wrist_rgb；right_wrist_0_rgb ← right_wrist_rgb。
#   • 输出：infer_chunk 里 postprocessor 后对 action 取 [:26] 回传客户端（与 bot.command 维序一致）。
#
# 本脚本：observation.state / action 为 26 维（与 payload joints / 回传 chunk 一致）；图像为 record 原始文件 copy；
# record→三路目录映射见 _resolve_head_rgb_dir / wrist 路径。
# ---------------------------------------------------------------------------

# === Tensor keys: Pi05Session._build_batch（agibot_pi05_server.py）===
OBS_STATE = f"{OBS_STR}.state"
IMG_HEAD = f"{OBS_STR}.images.base_0_rgb"
IMG_LEFT = f"{OBS_STR}.images.left_wrist_0_rgb"
IMG_RIGHT = f"{OBS_STR}.images.right_wrist_0_rgb"

STATE_ACTION_DIM = 26  # agibot_client: ARM_DOF + HAND_DOF
# 某路相机在全部 episode 中都无图时，用该分辨率做黑图占位与 metadata（与 client 缺图占位一致）
_FALLBACK_IMAGE_HW = (224, 224)
FPS = 30  # agibot_client GdkClient30Hz default hz (int for LeRobot metadata)
# 默认语言标签（可被 --prompt 覆盖；传空字符串则走 meta_info）
DEFAULT_TASK_PROMPT = "pick up the torque gun"

_JOINT_NAMES = [f"arm_{i}" for i in range(14)]
_FINGER = ["thumb_rot", "index", "mid", "ring", "pinky", "thumb_bend"]
_HAND_L = [f"left_{n}" for n in _FINGER]
_HAND_R = [f"right_{n}" for n in _FINGER]
FEATURE_NAMES = _JOINT_NAMES + _HAND_L + _HAND_R


def _load_h5(path: Path):
    import h5py

    return h5py.File(path, "r")


def _sort_by_time(t: np.ndarray, y: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    t = np.asarray(t, dtype=np.int64).reshape(-1)
    y = np.asarray(y, dtype=np.float64)
    if y.ndim == 1:
        y = y.reshape(-1, 1)
    order = np.argsort(t)
    return t[order], y[order]


def _interp_multi(t_src: np.ndarray, y_src: np.ndarray, t_q: np.ndarray) -> np.ndarray:
    """Linear interpolate each column of y_src onto t_q (nanoseconds)."""
    t_src, y_src = _sort_by_time(t_src, y_src)
    t_src_f = t_src.astype(np.float64)
    t_q_f = np.asarray(t_q, dtype=np.float64)
    out = np.zeros((len(t_q), y_src.shape[1]), dtype=np.float64)
    for d in range(y_src.shape[1]):
        out[:, d] = np.interp(t_q_f, t_src_f, y_src[:, d], left=np.nan, right=np.nan)
    return out


def _effector_deg_to_rad(pos: np.ndarray) -> np.ndarray:
    pos = np.asarray(pos, dtype=np.float64)
    if pos.size == 0:
        return pos
    flat = np.abs(pos.reshape(-1))
    if flat.size and np.nanmax(flat) > 20.0:
        return np.radians(pos)
    return pos


def _build_state_action_vectors(f) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Returns (t_ns, state_26, action_26) at state/joint timestamps."""
    t_joint = np.asarray(f["state/joint/timestamp"][:], dtype=np.int64)
    arm = np.asarray(f["state/joint/position"][:], dtype=np.float64)
    if arm.shape[0] != len(t_joint) or arm.shape[1] != 14:
        raise ValueError(f"unexpected state/joint shape {arm.shape}")

    tl = np.asarray(f["state/left_effector/timestamp"][:], dtype=np.int64)
    hl = np.asarray(f["state/left_effector/position"][:], dtype=np.float64)
    tr = np.asarray(f["state/right_effector/timestamp"][:], dtype=np.int64)
    hr = np.asarray(f["state/right_effector/position"][:], dtype=np.float64)

    hl = _effector_deg_to_rad(hl)
    hr = _effector_deg_to_rad(hr)
    hl_i = _interp_multi(tl, hl, t_joint)
    hr_i = _interp_multi(tr, hr, t_joint)

    state = np.concatenate([arm, hl_i, hr_i], axis=1)
    if state.shape[1] != STATE_ACTION_DIM:
        raise ValueError(state.shape)

    # Action streams (command), already radians in typical logs
    aj_t = np.asarray(f["action/joint/timestamp"][:], dtype=np.int64)
    aj = np.asarray(f["action/joint/position"][:], dtype=np.float64)
    al_t = np.asarray(f["action/left_effector/timestamp"][:], dtype=np.int64)
    al = np.asarray(f["action/left_effector/position"][:], dtype=np.float64)
    ar_t = np.asarray(f["action/right_effector/timestamp"][:], dtype=np.int64)
    ar = np.asarray(f["action/right_effector/position"][:], dtype=np.float64)

    aj_i = _interp_multi(aj_t, aj, t_joint)
    al_i = _interp_multi(al_t, al, t_joint)
    ar_i = _interp_multi(ar_t, ar, t_joint)
    action = np.concatenate([aj_i, al_i, ar_i], axis=1)

    valid = np.isfinite(state).all(axis=1) & np.isfinite(action).all(axis=1)
    t_joint = t_joint[valid]
    state = state[valid]
    action = action[valid]
    return t_joint, state.astype(np.float32), action.astype(np.float32)


def _resample_30hz(t_ns: np.ndarray, state: np.ndarray, action: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    if len(t_ns) < 2:
        return t_ns[:0], state[:0], action[:0]
    t0, t1 = float(t_ns[0]), float(t_ns[-1])
    dt = 1e9 / float(FPS)
    grid = np.arange(t0, t1, dt, dtype=np.float64)
    if grid.size == 0:
        return t_ns[:0], state[:0], action[:0]
    t_ns_f = t_ns.astype(np.float64)
    st = np.stack(
        [np.interp(grid, t_ns_f, state[:, j]) for j in range(STATE_ACTION_DIM)],
        axis=1,
    ).astype(np.float32)
    ac = np.stack(
        [np.interp(grid, t_ns_f, action[:, j]) for j in range(STATE_ACTION_DIM)],
        axis=1,
    ).astype(np.float32)
    return grid.astype(np.int64), st, ac


def _stem_ns(p: Path) -> int:
    return int(p.stem)


def _collect_rgb_frames(folder: Path) -> tuple[np.ndarray, list[Path]]:
    """Timestamped RGB frames: *.jpg / *.jpeg / *.png in folder (ns timestamp in filename stem)."""
    if not folder.is_dir():
        return np.zeros(0, dtype=np.int64), []
    paths: list[Path] = []
    for pat in ("*.jpg", "*.jpeg", "*.png", "*.JPG", "*.JPEG", "*.PNG"):
        paths.extend(folder.glob(pat))
    paths = sorted({p.resolve(): p for p in paths}.values(), key=_stem_ns)
    if not paths:
        return np.zeros(0, dtype=np.int64), []
    ts = np.array([_stem_ns(p) for p in paths], dtype=np.int64)
    return ts, paths


def _resolve_head_rgb_dir(cam_root: Path, primary: str) -> Path:
    """
    Maps SDK camera name ``head`` (agibot_client: CosineCamera / get_latest_image("head")) to record JPEGs.
    GDK `head_center_fisheye/` is often H.265 only; RGB jpgs are usually under `head/color/`.
    """
    candidates = [primary, "head/color", "head_center_fisheye"]
    seen: set[str] = set()
    ordered: list[str] = []
    for c in candidates:
        if c and c not in seen:
            seen.add(c)
            ordered.append(c)
    for rel in ordered:
        d = cam_root / rel
        ts, _ = _collect_rgb_frames(d)
        if ts.size > 0:
            return d
    return cam_root / primary


def _nearest_image(
    ts: np.ndarray,
    paths: list[Path],
    t_q: int,
    *,
    expected_hw: tuple[int, int],
) -> Image.Image | np.ndarray:
    """Nearest frame by timestamp; PIL with ``filename`` set for native copy, or uint8 HWC black placeholder."""
    h, w = expected_hw
    if ts.size == 0 or not paths:
        return np.zeros((h, w, 3), dtype=np.uint8)
    i = int(np.searchsorted(ts, t_q, side="left"))
    candidates: list[int] = []
    if i < len(ts):
        candidates.append(i)
    if i > 0:
        candidates.append(i - 1)
    best = min(candidates, key=lambda k: abs(int(ts[k]) - t_q))
    path = paths[best]
    with Image.open(path) as im:
        if im.size != (w, h):
            raise ValueError(
                f"image {path} size {im.size[0]}x{im.size[1]} != dataset metadata {w}x{h} (W×H); "
                "all episodes must match the reference resolution probed at convert start."
            )
    carrier = Image.new("RGB", (1, 1), color=(0, 0, 0))
    carrier.filename = os.fspath(path)
    return carrier


def _probe_reference_hw(
    episodes: list[Path],
    head_subdir: str,
) -> tuple[tuple[int, int], tuple[int, int], tuple[int, int]]:
    """(H,W) per camera from the first existing frame found while scanning episodes."""
    found: list[tuple[int, int] | None] = [None, None, None]

    def try_dir(d: Path, idx: int) -> None:
        if found[idx] is not None:
            return
        _, paths = _collect_rgb_frames(d)
        if not paths:
            return
        with Image.open(paths[0]) as im:
            found[idx] = (im.height, im.width)

    for ep in episodes:
        cam_root = ep / "camera"
        head_dir = _resolve_head_rgb_dir(cam_root, head_subdir)
        left_dir = cam_root / "hand_left" / "color"
        right_dir = cam_root / "hand_right" / "color"
        try_dir(head_dir, 0)
        try_dir(left_dir, 1)
        try_dir(right_dir, 2)
        if all(x is not None for x in found):
            break

    def _fb(x: tuple[int, int] | None) -> tuple[int, int]:
        return x if x is not None else _FALLBACK_IMAGE_HW

    return _fb(found[0]), _fb(found[1]), _fb(found[2])


def _episode_task(
    meta_path: Path,
    default_task: str,
    *,
    task_prompt: str | None = None,
) -> str:
    """LeRobot 每帧 ``task`` 字符串。若给定 ``task_prompt``（非空），优先于 bag 内 meta。"""
    if task_prompt is not None and str(task_prompt).strip():
        return str(task_prompt).strip()
    if not meta_path.is_file():
        return default_task
    try:
        meta = json.loads(meta_path.read_text())
    except json.JSONDecodeError:
        return default_task
    text = str(meta.get("text") or "").strip()
    if text:
        return text
    tid = meta.get("task_id")
    if tid is not None:
        return f"task_id_{tid}"
    return default_task


def _discover_episodes(record_root: Path) -> list[Path]:
    out: list[Path] = []
    for child in sorted(record_root.iterdir()):
        if not child.is_dir():
            continue
        h5 = child / "record" / "raw_joints.h5"
        if h5.is_file():
            out.append(child)
    return out


def _count_dirs_without_h5(record_root: Path) -> int:
    """UUID 文件夹存在但没有 record/raw_joints.h5 的数量（仅统计、不转换）。"""
    if not record_root.is_dir():
        return 0
    n = 0
    for child in record_root.iterdir():
        if child.is_dir() and not (child / "record" / "raw_joints.h5").is_file():
            n += 1
    return n


def _episode_rgb_frame_counts(episode_dir: Path, head_subdir: str) -> tuple[int, int, int]:
    """每路目录下已收集的 RGB 帧数量（jpg/jpeg/png），用于统计。"""
    cam_root = episode_dir / "camera"
    head_dir = _resolve_head_rgb_dir(cam_root, head_subdir)
    left_dir = cam_root / "hand_left" / "color"
    right_dir = cam_root / "hand_right" / "color"
    _, ph = _collect_rgb_frames(head_dir)
    _, pl = _collect_rgb_frames(left_dir)
    _, pr = _collect_rgb_frames(right_dir)
    return len(ph), len(pl), len(pr)


def print_record_inventory(
    record_root: Path,
    episodes: list[Path],
    *,
    head_subdir: str,
) -> None:
    """转换前打印：episode 条数、各路 jpg/图像帧数；无 h5 的子目录数。"""
    skip = _count_dirs_without_h5(record_root)
    print(f"[inventory] record-root = {record_root.resolve()}")
    print(f"[inventory] 可转换 episode 数（含 record/raw_joints.h5）: {len(episodes)}")
    if skip:
        print(f"[inventory] 跳过子目录数（无 raw_joints.h5，不进入数据集）: {skip}")
    print("[inventory] 各路 RGB 帧数（文件名时间戳 ns，含 .jpg/.jpeg/.png）:")
    for ep in episodes:
        nh, nl, nr = _episode_rgb_frame_counts(ep, head_subdir)
        hd = _resolve_head_rgb_dir(ep / "camera", head_subdir)
        try:
            head_rel = hd.resolve().relative_to(ep.resolve())
        except ValueError:
            head_rel = hd
        print(f"  - {ep.name}")
        print(f"      head   -> {head_rel}  count={nh}")
        print(f"      left   -> camera/hand_left/color   count={nl}")
        print(f"      right  -> camera/hand_right/color  count={nr}")


def _make_features(hw_head: tuple[int, int], hw_left: tuple[int, int], hw_right: tuple[int, int]) -> dict:
    h0, w0 = hw_head
    h1, w1 = hw_left
    h2, w2 = hw_right
    return {
        ACTION: {"dtype": "float32", "shape": (STATE_ACTION_DIM,), "names": FEATURE_NAMES},
        OBS_STATE: {"dtype": "float32", "shape": (STATE_ACTION_DIM,), "names": FEATURE_NAMES},
        IMG_HEAD: {"dtype": "image", "shape": (h0, w0, 3), "names": ["height", "width", "channel"]},
        IMG_LEFT: {"dtype": "image", "shape": (h1, w1, 3), "names": ["height", "width", "channel"]},
        IMG_RIGHT: {"dtype": "image", "shape": (h2, w2, 3), "names": ["height", "width", "channel"]},
    }


def convert_episode(
    episode_dir: Path,
    dataset: LeRobotDataset,
    *,
    head_subdir: str,
    default_task: str,
    task_prompt: str | None,
    min_frames: int,
    hw_head: tuple[int, int],
    hw_left: tuple[int, int],
    hw_right: tuple[int, int],
) -> int:
    h5_path = episode_dir / "record" / "raw_joints.h5"
    meta_path = episode_dir / "meta_info.json"
    cam_root = episode_dir / "camera"

    with _load_h5(h5_path) as f:
        t_ns, state, action = _build_state_action_vectors(f)
    t_ns, state, action = _resample_30hz(t_ns, state, action)
    n = len(t_ns)
    if n < min_frames:
        return 0

    head_dir = _resolve_head_rgb_dir(cam_root, head_subdir)
    # wrist: same streams as agibot_client CosineCamera("hand_left"|"hand_right")
    left_dir = cam_root / "hand_left" / "color"
    right_dir = cam_root / "hand_right" / "color"
    ts_h, ph = _collect_rgb_frames(head_dir)
    ts_l, pl = _collect_rgb_frames(left_dir)
    ts_r, pr = _collect_rgb_frames(right_dir)
    ep_name = episode_dir.name
    if ts_h.size == 0:
        print(f"[warn] {ep_name}: no head RGB frames under {head_dir} (need JPEG/PNG; fisheye is often H.265 only).")
    if ts_l.size == 0:
        print(f"[warn] {ep_name}: no left wrist images under {left_dir}")
    if ts_r.size == 0:
        print(f"[warn] {ep_name}: no right wrist images under {right_dir}")

    task = _episode_task(meta_path, default_task, task_prompt=task_prompt)
    for i in range(n):
        t = int(t_ns[i])
        frame = {
            OBS_STATE: state[i],
            ACTION: action[i],
            IMG_HEAD: _nearest_image(ts_h, ph, t, expected_hw=hw_head),
            IMG_LEFT: _nearest_image(ts_l, pl, t, expected_hw=hw_left),
            IMG_RIGHT: _nearest_image(ts_r, pr, t, expected_hw=hw_right),
            "task": task,
        }
        dataset.add_frame(frame)
    dataset.save_episode(parallel_encoding=False)
    return n


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--record-root", type=Path, default=_REPO_ROOT / "record", help="Parent folder of UUID episodes")
    p.add_argument("--out-root", type=Path, default=_REPO_ROOT / "lerobot_datasets" / "agibot_record_pi05")
    p.add_argument("--repo-id", type=str, default="agibot_record_pi05", help="LeRobot repo_id metadata")
    p.add_argument(
        "--head-camera",
        type=str,
        default="head/color",
        help="Preferred subdir under camera/ for head RGB (jpg/png). Default head/color matches GDK JPEG; "
        "head_center_fisheye is often H.265-only — script auto-falls back to head/color if preferred is empty.",
    )
    p.add_argument(
        "--task-default",
        type=str,
        default="agibot manipulation",
        help="仅当 --prompt 为空（关闭固定句）且 meta_info 无可用 text/task_id 时的回退任务字符串。",
    )
    p.add_argument(
        "--task-prompt",
        "--prompt",
        dest="task_prompt",
        type=str,
        default=DEFAULT_TASK_PROMPT,
        metavar="TEXT",
        help="本次转换中**所有** episode 的 LeRobot 语言任务（默认：%(default)r）。"
        "传空字符串可关闭覆盖，改为按 meta_info 的 text / task_id。",
    )
    p.add_argument("--min-frames", type=int, default=30, help="Skip episodes shorter than this at 30 Hz")
    p.add_argument("--episodes", type=int, default=None, help="Max number of episodes to convert")
    p.add_argument(
        "--overwrite",
        action="store_true",
        help="Delete --out-root if it already exists (LeRobot.create requires a new empty directory).",
    )
    p.add_argument(
        "--stats-only",
        action="store_true",
        help="Only scan --record-root: print episode count and per-episode RGB frame counts, then exit.",
    )
    p.add_argument(
        "--keep-images-on-disk",
        action=argparse.BooleanOptionalAction,
        default=True,
        help="每个 episode 写入 Parquet 后是否保留 images/ 下文件。默认保留（便于直接浏览 jpg）；"
        "加 --no-keep-images-on-disk 则与 LeRobot 原生一致、写完即删目录以省磁盘（训练仍读 Parquet 内嵌 bytes）。",
    )
    args = p.parse_args()

    episodes = _discover_episodes(args.record_root)
    if args.episodes is not None:
        episodes = episodes[: args.episodes]
    if not episodes:
        raise SystemExit(f"No episodes with record/raw_joints.h5 under {args.record_root}")

    print_record_inventory(args.record_root, episodes, head_subdir=args.head_camera)
    if args.stats_only:
        print("[inventory] --stats-only: 不写入数据集，退出。")
        return

    if args.out_root.exists():
        if args.overwrite:
            shutil.rmtree(args.out_root)
        else:
            raise SystemExit(
                f"Output directory already exists: {args.out_root}\n"
                "Remove it or pass --overwrite (LeRobotDataset.create needs an empty path)."
            )

    hw_head, hw_left, hw_right = _probe_reference_hw(episodes, args.head_camera)
    print(
        f"[probe] image HW (H×W) metadata: head={hw_head} left_wrist={hw_left} right_wrist={hw_right} "
        f"(missing-camera fallback={_FALLBACK_IMAGE_HW})"
    )
    if args.task_prompt and str(args.task_prompt).strip():
        print(f"[task] 固定 prompt（全部 episode）: {args.task_prompt.strip()!r}")
    print(f"[convert] 开始写入 LeRobot 数据集（共 {len(episodes)} 条 episode，PI05 三路图 + 26 维 state/action）…")

    features = _make_features(hw_head, hw_left, hw_right)
    dataset = NativeCopyLeRobotDataset.create(
        repo_id=args.repo_id,
        fps=FPS,
        root=args.out_root,
        robot_type="agibot_a2d",
        features=features,
        use_videos=False,
    )
    dataset.keep_images_on_disk = args.keep_images_on_disk
    print(f"[images] keep on disk after each episode: {args.keep_images_on_disk}")

    total_frames = 0
    used = 0
    for ep in episodes:
        n = convert_episode(
            ep,
            dataset,
            head_subdir=args.head_camera,
            default_task=args.task_default,
            task_prompt=args.task_prompt,
            min_frames=args.min_frames,
            hw_head=hw_head,
            hw_left=hw_left,
            hw_right=hw_right,
        )
        if n:
            used += 1
            total_frames += n
            print(f"[ok] {ep.name}: {n} frames @ {FPS}Hz")
        else:
            print(f"[skip] {ep.name}: too short or empty")

    dataset.finalize()
    print(f"Done. episodes={used} total_frames={total_frames} root={args.out_root}")


if __name__ == "__main__":
    main()
