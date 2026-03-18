#!/usr/bin/env python3
"""
将智元机器人（Agibot）采集的原始数据转换为 LeRobot 训练 Pi0 模型所需的标准格式。

主要功能：
1. 读取 H5 格式的关节数据和相机数据
2. 以 Head Camera 为 Master Clock，进行 30Hz 时间戳对齐
3. 构建 26 维 State 向量（Left_Arm(7) + Left_Hand(6) + Right_Arm(7) + Right_Hand(6)）
4. 生成 Action（Action_t = State_{t+1}）
5. 处理图像（Resize 到 320x240 或 256x256）
6. 输出 LeRobot 标准格式（Parquet + 图片）
"""

import argparse
import json
import os
import shutil
from pathlib import Path
from typing import Dict, List, Optional, Tuple

import cv2
import h5py
import numpy as np
import pandas as pd
from tqdm import tqdm


class AgibotParser:
    """解析智元机器人原始数据格式"""

    def __init__(self, episode_dir: Path):
        self.episode_dir = Path(episode_dir)
        self.meta_info = self._load_meta_info()
        self.joints_data = self._load_joints()
        self.camera_timestamps = self._load_camera_timestamps()

    def _load_meta_info(self) -> dict:
        """加载 meta_info.json"""
        meta_path = self.episode_dir / "meta_info.json"
        if not meta_path.exists():
            raise FileNotFoundError(f"meta_info.json not found in {self.episode_dir}")
        with open(meta_path, "r") as f:
            return json.load(f)

    def _load_joints(self) -> dict:
        """加载关节数据（H5格式）"""
        h5_path = self.episode_dir / "record" / "raw_joints.h5"
        if not h5_path.exists():
            raise FileNotFoundError(f"raw_joints.h5 not found in {h5_path}")

        with h5py.File(h5_path, "r") as f:
            data = {
                "joint": {
                    "position": f["state/joint/position"][:],
                    "timestamp": f["state/joint/timestamp"][:],
                },
                "left_effector": {
                    "position": f["state/left_effector/position"][:],
                    "timestamp": f["state/left_effector/timestamp"][:],
                },
                "right_effector": {
                    "position": f["state/right_effector/position"][:],
                    "timestamp": f["state/right_effector/timestamp"][:],
                },
            }
        return data

    def _load_camera_timestamps(self) -> dict:
        """加载相机时间戳"""
        timestamps = {}

        # Head Camera (优先使用 head/color 目录下的文件名)
        head_color_dir = self.episode_dir / "camera" / "head" / "color"
        if head_color_dir.exists():
            # 从文件名提取时间戳
            jpg_files = sorted(head_color_dir.glob("*.jpg"))
            if jpg_files:
                head_ts = []
                for f in jpg_files:
                    try:
                        head_ts.append(int(f.stem))
                    except ValueError:
                        continue
                if head_ts:
                    timestamps["head"] = np.array(head_ts)
        
        # 如果上面没有找到，尝试从 head_color.txt 读取
        if "head" not in timestamps:
            head_txt = self.episode_dir / "camera" / "head_color" / "head_color.txt"
            if head_txt.exists():
                head_ts = []
                with open(head_txt, "r") as f:
                    for line in f:
                        parts = line.strip().split()
                        if parts:
                            try:
                                head_ts.append(int(parts[0]))
                            except ValueError:
                                continue
                if head_ts:
                    timestamps["head"] = np.array(head_ts)

        # Left Wrist Camera
        left_wrist_dir = self.episode_dir / "camera" / "hand_left" / "color"
        if left_wrist_dir.exists():
            jpg_files = sorted(left_wrist_dir.glob("*.jpg"))
            if jpg_files:
                left_ts = []
                for f in jpg_files:
                    try:
                        left_ts.append(int(f.stem))
                    except ValueError:
                        continue
                if left_ts:
                    timestamps["wrist_left"] = np.array(left_ts)
        
        # 如果上面没有找到，尝试从 txt 文件读取
        if "wrist_left" not in timestamps:
            left_txt = self.episode_dir / "camera" / "hand_left" / "d405_1_jpg.txt"
            if left_txt.exists():
                left_ts = []
                with open(left_txt, "r") as f:
                    for line in f:
                        parts = line.strip().split()
                        if len(parts) >= 3:
                            try:
                                # 格式：frame_id timestamp_ns timestamp_ms ...
                                # timestamp_ms 是毫秒，需要转换为纳秒
                                left_ts.append(int(float(parts[2]) * 1e6))
                            except (ValueError, IndexError):
                                continue
                if left_ts:
                    timestamps["wrist_left"] = np.array(left_ts)

        # Right Wrist Camera
        right_wrist_dir = self.episode_dir / "camera" / "hand_right" / "color"
        if right_wrist_dir.exists():
            jpg_files = sorted(right_wrist_dir.glob("*.jpg"))
            if jpg_files:
                right_ts = []
                for f in jpg_files:
                    try:
                        right_ts.append(int(f.stem))
                    except ValueError:
                        continue
                if right_ts:
                    timestamps["wrist_right"] = np.array(right_ts)
        
        # 如果上面没有找到，尝试从 txt 文件读取
        if "wrist_right" not in timestamps:
            right_txt = self.episode_dir / "camera" / "hand_right" / "d405_2_jpg.txt"
            if right_txt.exists():
                right_ts = []
                with open(right_txt, "r") as f:
                    for line in f:
                        parts = line.strip().split()
                        if len(parts) >= 3:
                            try:
                                right_ts.append(int(float(parts[2]) * 1e6))
                            except (ValueError, IndexError):
                                continue
                if right_ts:
                    timestamps["wrist_right"] = np.array(right_ts)

        return timestamps

    def get_camera_image_path(self, camera_name: str, timestamp: int) -> Optional[Path]:
        """根据时间戳获取相机图片路径"""
        if camera_name == "head":
            img_dir = self.episode_dir / "camera" / "head" / "color"
            if img_dir.exists():
                img_path = img_dir / f"{timestamp}.jpg"
                if img_path.exists():
                    return img_path
        elif camera_name == "wrist_left":
            img_dir = self.episode_dir / "camera" / "hand_left" / "color"
            if img_dir.exists():
                img_path = img_dir / f"{timestamp}.jpg"
                if img_path.exists():
                    return img_path
        elif camera_name == "wrist_right":
            img_dir = self.episode_dir / "camera" / "hand_right" / "color"
            if img_dir.exists():
                img_path = img_dir / f"{timestamp}.jpg"
                if img_path.exists():
                    return img_path
        return None


def align_timestamps(
    head_timestamps: np.ndarray,
    left_wrist_timestamps: np.ndarray,
    right_wrist_timestamps: np.ndarray,
    joint_timestamps: np.ndarray,
    target_fps: float = 30.0,
    max_time_diff_ms: float = 50.0,
) -> Tuple[np.ndarray, List[int], List[int], List[int], List[int]]:
    """
    以 Head Camera 为 Master Clock，对齐所有传感器的时间戳

    Args:
        head_timestamps: Head Camera 时间戳（纳秒）
        left_wrist_timestamps: Left Wrist Camera 时间戳（纳秒）
        right_wrist_timestamps: Right Wrist Camera 时间戳（纳秒）
        joint_timestamps: Joint 时间戳（纳秒）
        target_fps: 目标帧率（Hz）
        max_time_diff_ms: 最大允许时间差（毫秒）

    Returns:
        aligned_timestamps: 对齐后的时间戳数组
        head_indices: Head Camera 对应的索引
        left_wrist_indices: Left Wrist Camera 对应的索引
        right_wrist_indices: Right Wrist Camera 对应的索引
        joint_indices: Joint 对应的索引
    """
    if len(head_timestamps) == 0:
        raise ValueError("Head camera timestamps are empty")

    # 计算目标时间间隔（纳秒）
    target_interval_ns = int(1e9 / target_fps)

    # 生成均匀的时间戳序列（基于 Head Camera 的时间范围）
    start_time = head_timestamps[0]
    end_time = head_timestamps[-1]
    aligned_timestamps = np.arange(start_time, end_time + target_interval_ns, target_interval_ns)

    head_indices = []
    left_wrist_indices = []
    right_wrist_indices = []
    joint_indices = []

    max_time_diff_ns = max_time_diff_ms * 1e6  # 转换为纳秒

    for t in aligned_timestamps:
        # 找到 Head Camera 最近的一帧
        head_idx = np.argmin(np.abs(head_timestamps - t))
        head_diff = abs(head_timestamps[head_idx] - t)

        # 找到 Left Wrist Camera 最近的一帧
        left_idx = np.argmin(np.abs(left_wrist_timestamps - t))
        left_diff = abs(left_wrist_timestamps[left_idx] - t)

        # 找到 Right Wrist Camera 最近的一帧
        right_idx = np.argmin(np.abs(right_wrist_timestamps - t))
        right_diff = abs(right_wrist_timestamps[right_idx] - t)

        # 找到 Joint 最近的一帧（使用最近邻）
        joint_idx = np.argmin(np.abs(joint_timestamps - t))
        joint_diff = abs(joint_timestamps[joint_idx] - t)

        # 检查时间差是否在允许范围内
        max_diff = max(head_diff, left_diff, right_diff, joint_diff)
        if max_diff <= max_time_diff_ns:
            head_indices.append(head_idx)
            left_wrist_indices.append(left_idx)
            right_wrist_indices.append(right_idx)
            joint_indices.append(joint_idx)
        # 如果超出范围，跳过该帧

    return (
        aligned_timestamps[: len(head_indices)],
        head_indices,
        left_wrist_indices,
        right_wrist_indices,
        joint_indices,
    )


def build_state_vector(
    joint_positions: np.ndarray, left_effector_positions: np.ndarray, right_effector_positions: np.ndarray
) -> np.ndarray:
    """
    构建 26 维 State 向量：[Left_Arm(7) + Left_Hand(6) + Right_Arm(7) + Right_Hand(6)]

    Args:
        joint_positions: (N, 14) 关节位置，前7个是左臂，后7个是右臂
        left_effector_positions: (N, 6) 左手位置
        right_effector_positions: (N, 6) 右手位置

    Returns:
        state: (N, 26) State 向量
    """
    left_arm = joint_positions[:, :7]  # 前7个关节是左臂
    right_arm = joint_positions[:, 7:]  # 后7个关节是右臂

    state = np.concatenate([left_arm, left_effector_positions, right_arm, right_effector_positions], axis=1)
    return state


def process_image(img_path: Path, target_size: Tuple[int, int] = (320, 240)) -> np.ndarray:
    """
    处理图像：读取、Resize、转换为 RGB

    Args:
        img_path: 图像路径
        target_size: 目标尺寸 (width, height)

    Returns:
        processed_image: 处理后的图像数组
    """
    img = cv2.imread(str(img_path))
    if img is None:
        raise ValueError(f"Failed to load image: {img_path}")

    # BGR to RGB
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Resize
    img = cv2.resize(img, target_size, interpolation=cv2.INTER_LINEAR)

    return img


def convert_episode(
    episode_dir: Path,
    output_dir: Path,
    episode_id: int,
    target_fps: float = 30.0,
    image_size: Tuple[int, int] = (320, 240),
    max_time_diff_ms: float = 50.0,
) -> dict:
    """
    转换单个 episode，返回DataFrame和统计信息

    Returns:
        episode_data: 包含DataFrame和统计信息的字典，如果失败返回None
    """
    parser = AgibotParser(episode_dir)

    # 获取时间戳
    head_ts = parser.camera_timestamps.get("head", np.array([]))
    left_wrist_ts = parser.camera_timestamps.get("wrist_left", np.array([]))
    right_wrist_ts = parser.camera_timestamps.get("wrist_right", np.array([]))
    joint_ts = parser.joints_data["joint"]["timestamp"]

    if len(head_ts) == 0:
        print(f"Warning: No head camera timestamps found in {episode_dir}, skipping...")
        return None

    # 对齐时间戳
    (
        aligned_ts,
        head_indices,
        left_wrist_indices,
        right_wrist_indices,
        joint_indices,
    ) = align_timestamps(
        head_ts,
        left_wrist_ts,
        right_wrist_ts,
        joint_ts,
        target_fps=target_fps,
        max_time_diff_ms=max_time_diff_ms,
    )

    if len(aligned_ts) == 0:
        print(f"Warning: No aligned timestamps found in {episode_dir}, skipping...")
        return None

    # 构建 State 向量
    joint_pos = parser.joints_data["joint"]["position"][joint_indices]
    left_effector_pos = parser.joints_data["left_effector"]["position"][joint_indices]
    right_effector_pos = parser.joints_data["right_effector"]["position"][joint_indices]

    states = build_state_vector(joint_pos, left_effector_pos, right_effector_pos)

    # 构建 Action（Action_t = State_{t+1}）
    actions = np.zeros_like(states)
    actions[:-1] = states[1:]
    actions[-1] = states[-1]  # 最后一帧复制前一帧的 Action

    # 创建图像输出目录（v3.0格式：images/{image_key}/episode-{episode_index:06d}/frame-{frame_index:06d}.png）
    images_base_dir = output_dir / "images"
    head_img_dir = images_base_dir / "head" / f"episode-{episode_id:06d}"
    left_img_dir = images_base_dir / "wrist_left" / f"episode-{episode_id:06d}"
    right_img_dir = images_base_dir / "wrist_right" / f"episode-{episode_id:06d}"
    head_img_dir.mkdir(parents=True, exist_ok=True)
    left_img_dir.mkdir(parents=True, exist_ok=True)
    right_img_dir.mkdir(parents=True, exist_ok=True)

    # 处理图像和构建数据
    data_rows = []
    task_str = "pick up and place the torque gun"
    
    for i, (t, head_idx, left_idx, right_idx) in enumerate(
        zip(aligned_ts, head_indices, left_wrist_indices, right_wrist_indices)
    ):
        # 获取图像路径
        head_img_path = parser.get_camera_image_path("head", head_ts[head_idx])
        left_img_path = parser.get_camera_image_path("wrist_left", left_wrist_ts[left_idx])
        right_img_path = parser.get_camera_image_path("wrist_right", right_wrist_ts[right_idx])

        # v3.0格式图像路径（使用JPG格式以节省空间）
        frame_name = f"frame-{i:06d}.jpg"
        head_img_file = head_img_dir / frame_name
        left_img_file = left_img_dir / frame_name
        right_img_file = right_img_dir / frame_name

        try:
            if head_img_path and head_img_path.exists():
                head_img = process_image(head_img_path, image_size)
                cv2.imwrite(str(head_img_file), cv2.cvtColor(head_img, cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 95])
            else:
                # 创建空白图像
                head_img = np.zeros((image_size[1], image_size[0], 3), dtype=np.uint8)
                cv2.imwrite(str(head_img_file), head_img, [cv2.IMWRITE_JPEG_QUALITY, 95])

            if left_img_path and left_img_path.exists():
                left_img = process_image(left_img_path, image_size)
                cv2.imwrite(str(left_img_file), cv2.cvtColor(left_img, cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 95])
            else:
                left_img = np.zeros((image_size[1], image_size[0], 3), dtype=np.uint8)
                cv2.imwrite(str(left_img_file), left_img, [cv2.IMWRITE_JPEG_QUALITY, 95])

            if right_img_path and right_img_path.exists():
                right_img = process_image(right_img_path, image_size)
                cv2.imwrite(str(right_img_file), cv2.cvtColor(right_img, cv2.COLOR_RGB2BGR), [cv2.IMWRITE_JPEG_QUALITY, 95])
            else:
                right_img = np.zeros((image_size[1], image_size[0], 3), dtype=np.uint8)
                cv2.imwrite(str(right_img_file), right_img, [cv2.IMWRITE_JPEG_QUALITY, 95])
        except Exception as e:
            print(f"Warning: Failed to process images for frame {i}: {e}")
            continue

        # 构建数据行（v3.0格式图像路径，使用JPG）
        row = {
            "observation.state": states[i].tolist(),
            "action": actions[i].tolist(),
            "observation.images.head": f"images/head/episode-{episode_id:06d}/frame-{i:06d}.jpg",
            "observation.images.wrist_left": f"images/wrist_left/episode-{episode_id:06d}/frame-{i:06d}.jpg",
            "observation.images.wrist_right": f"images/wrist_right/episode-{episode_id:06d}/frame-{i:06d}.jpg",
            "task": task_str,
            "episode_index": episode_id,
            "frame_index": i,
        }
        data_rows.append(row)

    if len(data_rows) == 0:
        return None

    # 创建DataFrame
    df = pd.DataFrame(data_rows)

    # 计算统计信息
    all_states = np.array([row["observation.state"] for row in data_rows])
    all_actions = np.array([row["action"] for row in data_rows])

    episode_info = {
        "episode_id": episode_id,
        "dataframe": df,
        "num_frames": len(data_rows),
        "task": task_str,
        "state_stats": {
            "min": all_states.min(axis=0).tolist(),
            "max": all_states.max(axis=0).tolist(),
            "mean": all_states.mean(axis=0).tolist(),
            "std": all_states.std(axis=0).tolist(),
        },
        "action_stats": {
            "min": all_actions.min(axis=0).tolist(),
            "max": all_actions.max(axis=0).tolist(),
            "mean": all_actions.mean(axis=0).tolist(),
            "std": all_actions.std(axis=0).tolist(),
        },
    }

    return episode_info


def get_parquet_file_size_in_mb(df: pd.DataFrame) -> float:
    """估算DataFrame的parquet文件大小（MB）"""
    # 简单估算：每个float32约4字节，每个int64约8字节
    # 这里使用更保守的估算
    size_bytes = df.memory_usage(deep=True).sum()
    return size_bytes / (1024**2)


def update_chunk_file_indices(chunk_idx: int, file_idx: int, chunk_size: int = 1000) -> Tuple[int, int]:
    """更新chunk和file索引"""
    if file_idx == chunk_size - 1:
        file_idx = 0
        chunk_idx += 1
    else:
        file_idx += 1
    return chunk_idx, file_idx


def write_v30_dataset(
    output_dir: Path,
    episode_infos: List[dict],
    data_file_size_in_mb: float = 100.0,
    chunk_size: int = 1000,
):
    """生成LeRobot v3.0格式的数据集"""
    if not episode_infos or all(info is None for info in episode_infos):
        print("Warning: No valid episodes to process")
        return

    # 过滤掉None的episode
    valid_episodes = [info for info in episode_infos if info is not None]
    if not valid_episodes:
        print("Warning: No valid episodes after filtering")
        return
    
    print(f"开始生成v3.0格式数据集，共 {len(valid_episodes)} 个episodes...")

    # 合并所有DataFrame并计算全局统计
    all_dataframes = []
    all_states = []
    all_actions = []
    tasks_set = set()
    
    for info in valid_episodes:
        df = info["dataframe"]
        all_dataframes.append(df)
        
        states = np.array([np.array(s) for s in df["observation.state"]])
        actions = np.array([np.array(a) for a in df["action"]])
        all_states.append(states)
        all_actions.append(actions)
        
        if "task" in df.columns:
            tasks_set.update(df["task"].unique())

    # 合并所有数据
    all_states_combined = np.concatenate(all_states, axis=0)
    all_actions_combined = np.concatenate(all_actions, axis=0)

    # 创建tasks DataFrame
    tasks_list = sorted(list(tasks_set))
    tasks_df = pd.DataFrame({"task_index": range(len(tasks_list))}, index=tasks_list)
    tasks_path = output_dir / "meta" / "tasks.parquet"
    tasks_path.parent.mkdir(parents=True, exist_ok=True)
    tasks_df.to_parquet(tasks_path)

    # 创建task到task_index的映射
    task_to_index = {task: idx for idx, task in enumerate(tasks_list)}

    # 为每个episode添加task_index（创建副本以避免修改原始DataFrame）
    for info in valid_episodes:
        df = info["dataframe"].copy()  # 创建副本
        df["task_index"] = df["task"].map(task_to_index)
        info["dataframe"] = df  # 更新为带task_index的副本

    # 合并数据到chunk文件
    chunk_idx = 0
    file_idx = 0
    current_dataframes = []
    current_size_mb = 0.0
    global_index = 0
    episodes_metadata = []

    for ep_idx, info in enumerate(valid_episodes):
        df = info["dataframe"].copy()  # 创建副本以避免修改
        df_size_mb = get_parquet_file_size_in_mb(df)
        num_frames = len(df)

        # 更新index和episode_index
        df["index"] = range(global_index, global_index + num_frames)
        df["episode_index"] = ep_idx

        # 检查是否需要创建新文件
        if current_size_mb + df_size_mb > data_file_size_in_mb and current_dataframes:
            # 保存当前累积的数据
            concatenated_df = pd.concat(current_dataframes, ignore_index=True)
            data_path = output_dir / "data" / f"chunk-{chunk_idx:03d}" / f"file-{file_idx:03d}.parquet"
            data_path.parent.mkdir(parents=True, exist_ok=True)
            concatenated_df.to_parquet(data_path, index=False)

            # 更新已保存的episodes的元数据
            for saved_info in current_dataframes:
                saved_ep_idx = saved_info["episode_index"].iloc[0]
                episodes_metadata[saved_ep_idx]["data/chunk_index"] = chunk_idx
                episodes_metadata[saved_ep_idx]["data/file_index"] = file_idx

            # 重置
            chunk_idx, file_idx = update_chunk_file_indices(chunk_idx, file_idx, chunk_size)
            current_dataframes = []
            current_size_mb = 0.0

        # 添加当前episode的元数据
        episode_metadata = {
            "episode_index": ep_idx,
            "data/chunk_index": chunk_idx,  # 将在保存时更新
            "data/file_index": file_idx,  # 将在保存时更新
            "dataset_from_index": global_index,
            "dataset_to_index": global_index + num_frames,
            "length": num_frames,
        }
        episodes_metadata.append(episode_metadata)

        # 添加到当前累积
        current_dataframes.append(df)
        current_size_mb += df_size_mb
        global_index += num_frames

    # 保存剩余的数据
    if current_dataframes:
        concatenated_df = pd.concat(current_dataframes, ignore_index=True)
        data_path = output_dir / "data" / f"chunk-{chunk_idx:03d}" / f"file-{file_idx:03d}.parquet"
        data_path.parent.mkdir(parents=True, exist_ok=True)
        concatenated_df.to_parquet(data_path, index=False)

        # 更新最后一批episodes的元数据
        for saved_info in current_dataframes:
            saved_ep_idx = saved_info["episode_index"].iloc[0]
            episodes_metadata[saved_ep_idx]["data/chunk_index"] = chunk_idx
            episodes_metadata[saved_ep_idx]["data/file_index"] = file_idx

    # 保存episodes元数据
    episodes_df = pd.DataFrame(episodes_metadata)
    episodes_path = output_dir / "meta" / "episodes" / "chunk-000" / "file-000.parquet"
    episodes_path.parent.mkdir(parents=True, exist_ok=True)
    episodes_df.to_parquet(episodes_path, index=False)

    # 生成stats.json
    stats = {
        "observation.state": {
            "min": all_states_combined.min(axis=0).tolist(),
            "max": all_states_combined.max(axis=0).tolist(),
            "mean": all_states_combined.mean(axis=0).tolist(),
            "std": all_states_combined.std(axis=0).tolist(),
        },
        "action": {
            "min": all_actions_combined.min(axis=0).tolist(),
            "max": all_actions_combined.max(axis=0).tolist(),
            "mean": all_actions_combined.mean(axis=0).tolist(),
            "std": all_actions_combined.std(axis=0).tolist(),
        },
    }
    stats_path = output_dir / "meta" / "stats.json"
    stats_path.parent.mkdir(parents=True, exist_ok=True)
    with open(stats_path, "w") as f:
        json.dump(stats, f, indent=2)

    # 生成info.json
    info_dict = {
        "codebase_version": "v3.0",
        "total_episodes": len(valid_episodes),
        "total_frames": global_index,
        "total_tasks": len(tasks_list),
        "tasks": tasks_list,
        "state_dim": all_states_combined.shape[1],
        "action_dim": all_actions_combined.shape[1],
        "data_path": "data/chunk-{chunk_index:03d}/file-{file_index:03d}.parquet",
        "image_path": "images/{image_key}/episode-{episode_index:06d}/frame-{frame_index:06d}.jpg",
        "data_files_size_in_mb": data_file_size_in_mb,
        "fps": 30.0,
        "features": {
            "observation.state": {"dtype": "float32", "shape": [all_states_combined.shape[1]]},
            "action": {"dtype": "float32", "shape": [all_actions_combined.shape[1]]},
            "observation.images.head": {"dtype": "image", "shape": None},
            "observation.images.wrist_left": {"dtype": "image", "shape": None},
            "observation.images.wrist_right": {"dtype": "image", "shape": None},
            "task": {"dtype": "str", "shape": None},
            "episode_index": {"dtype": "int64", "shape": [1]},
            "frame_index": {"dtype": "int64", "shape": [1]},
            "index": {"dtype": "int64", "shape": [1]},
            "task_index": {"dtype": "int64", "shape": [1]},
        },
    }

    info_path = output_dir / "meta" / "info.json"
    info_path.parent.mkdir(parents=True, exist_ok=True)
    with open(info_path, "w") as f:
        json.dump(info_dict, f, indent=2)
    
    print(f"✅ v3.0格式数据集生成完成！")
    print(f"   - Episodes: {len(valid_episodes)}")
    print(f"   - Total frames: {global_index}")
    print(f"   - Tasks: {len(tasks_list)}")
    print(f"   - Data files: chunk-{chunk_idx:03d}/file-{file_idx:03d}.parquet")


def main():
    parser = argparse.ArgumentParser(description="转换 Agibot 数据到 LeRobot 格式")
    parser.add_argument("--input_dir", type=str, required=True, help="输入目录（包含多个 episode 文件夹）")
    parser.add_argument("--output_dir", type=str, required=True, help="输出目录")
    parser.add_argument("--target_fps", type=float, default=30.0, help="目标帧率（Hz）")
    parser.add_argument("--image_size", type=str, default="320x240", help="图像尺寸（格式：WxH）")
    parser.add_argument("--max_time_diff_ms", type=float, default=50.0, help="最大允许时间差（毫秒）")
    parser.add_argument("--num_episodes", type=int, default=None, help="处理的 episode 数量（None=全部）")

    args = parser.parse_args()

    input_dir = Path(args.input_dir)
    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # 解析图像尺寸
    width, height = map(int, args.image_size.split("x"))
    image_size = (width, height)

    # 查找所有 episode 目录
    episode_dirs = [d for d in input_dir.iterdir() if d.is_dir() and not d.name.startswith(".")]
    episode_dirs = sorted(episode_dirs)

    if args.num_episodes:
        episode_dirs = episode_dirs[: args.num_episodes]

    print(f"找到 {len(episode_dirs)} 个 episode")

    episode_infos = []
    for episode_idx, episode_dir in enumerate(tqdm(episode_dirs, desc="转换 episodes")):
        try:
            info = convert_episode(
                episode_dir,
                output_dir,
                episode_id=episode_idx,
                target_fps=args.target_fps,
                image_size=image_size,
                max_time_diff_ms=args.max_time_diff_ms,
            )
            episode_infos.append(info)
        except Exception as e:
            print(f"Error processing {episode_dir}: {e}")
            episode_infos.append(None)
            continue

    # 生成v3.0格式数据集
    write_v30_dataset(output_dir, episode_infos)
    print(f"转换完成！输出目录：{output_dir}")


if __name__ == "__main__":
    main()

