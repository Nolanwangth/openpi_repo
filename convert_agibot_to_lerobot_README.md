# Agibot 到 LeRobot 数据转换工具

这个脚本将智元机器人（Agibot）采集的原始数据转换为 LeRobot v3.0 标准格式，可直接用于训练 Pi05 模型。

## 功能特性

1. **时间戳对齐**：以 Head Camera 为 Master Clock，30Hz 采样率对齐所有传感器数据
2. **多视角同步**：自动对齐 Head、Left Wrist、Right Wrist 三个相机
3. **State 向量构建**：26 维向量 [Left_Arm(7) + Left_Hand(6) + Right_Arm(7) + Right_Hand(6)]
4. **Action 生成**：Action_t = State_{t+1}（绝对位置控制）
5. **图像处理**：自动 Resize 到指定尺寸（默认 320x240），使用 JPG 格式节省存储空间
6. **v3.0 标准格式**：生成符合 LeRobot v3.0 标准的完整数据集结构
   - 合并多个 episode 到 chunk 文件
   - 生成 episodes 元数据
   - 生成 stats.json 和 tasks.parquet

## 输入数据格式

每个 episode 目录应包含以下结构：

```
episode_uuid/
├── meta_info.json          # 元数据信息
├── record/
│   └── raw_joints.h5      # 关节数据（H5格式）
└── camera/
    ├── head/color/        # Head 相机图片（.jpg，文件名为时间戳）
    ├── hand_left/color/   # 左手相机图片
    └── hand_right/color/  # 右手相机图片
```

### H5 文件结构

- `state/joint/position`: (N, 14) - 14个关节位置（前7个左臂，后7个右臂）
- `state/joint/timestamp`: (N,) - 关节时间戳（纳秒）
- `state/left_effector/position`: (N, 6) - 左手位置（6个自由度）
- `state/left_effector/timestamp`: (N,) - 左手时间戳
- `state/right_effector/position`: (N, 6) - 右手位置（6个自由度）
- `state/right_effector/timestamp`: (N,) - 右手时间戳

## 输出数据格式（LeRobot v3.0 标准）

```
output_dir/
├── data/
│   └── chunk-000/
│       ├── file-000.parquet   # 多个episode合并的数据文件
│       ├── file-001.parquet
│       └── ...
├── images/
│   ├── head/
│   │   └── episode-XXXXXX/
│   │       └── frame-XXXXXX.jpg
│   ├── wrist_left/
│   │   └── episode-XXXXXX/
│   │       └── frame-XXXXXX.jpg
│   └── wrist_right/
│       └── episode-XXXXXX/
│           └── frame-XXXXXX.jpg
└── meta/
    ├── episodes/
    │   └── chunk-000/
    │       └── file-000.parquet   # Episode元数据
    ├── info.json                  # 数据集信息（包含codebase_version: "v3.0"）
    ├── stats.json                 # 统计信息（用于归一化）
    └── tasks.parquet              # 任务元数据
```

### 数据文件（Parquet）列

- `observation.state`: List[float] - 26维状态向量
- `action`: List[float] - 26维动作向量
- `observation.images.head`: str - Head 相机图片路径（v3.0格式：`images/head/episode-XXXXXX/frame-XXXXXX.jpg`）
- `observation.images.wrist_left`: str - 左手相机图片路径
- `observation.images.wrist_right`: str - 右手相机图片路径
- `task`: str - 任务描述（默认："pick up and place the torque gun"）
- `task_index`: int - 任务索引
- `episode_index`: int - Episode索引
- `frame_index`: int - 帧索引（在episode内的索引）
- `index`: int - 全局帧索引

### Episode 元数据（Parquet）列

- `episode_index`: int - Episode索引
- `data/chunk_index`: int - 数据所在的chunk索引
- `data/file_index`: int - 数据所在的文件索引
- `dataset_from_index`: int - 在数据集中的起始索引
- `dataset_to_index`: int - 在数据集中的结束索引
- `length`: int - Episode长度（帧数）

## 使用方法

### 基本用法

```bash
conda activate lerobot_conv
python convert_agibot_to_lerobot.py \
    --input_dir record \
    --output_dir lerobot_dataset \
    --target_fps 30.0 \
    --image_size 320x240 \
    --max_time_diff_ms 50.0
```

### 参数说明

- `--input_dir`: 输入目录，包含多个 episode 文件夹
- `--output_dir`: 输出目录，将创建 LeRobot 标准格式的数据集
- `--target_fps`: 目标帧率（默认：30.0 Hz）
- `--image_size`: 图像尺寸，格式为 WxH（默认：320x240）
- `--max_time_diff_ms`: 最大允许时间差（默认：50.0 毫秒），超过此值将丢弃该帧
- `--num_episodes`: 处理的 episode 数量（默认：None，处理全部）

### 示例

```bash
# 处理前10个episode，使用256x256图像
python convert_agibot_to_lerobot.py \
    --input_dir record \
    --output_dir lerobot_dataset \
    --num_episodes 10 \
    --image_size 256x256

# 使用更严格的时间同步（30ms）
python convert_agibot_to_lerobot.py \
    --input_dir record \
    --output_dir lerobot_dataset \
    --max_time_diff_ms 30.0
```

## 时间戳对齐逻辑

1. **Master Clock**：以 Head Camera 的时间戳为基准
2. **均匀采样**：在 Head Camera 的时间范围内，以目标 FPS 生成均匀时间戳
3. **最近邻匹配**：对于每个目标时间戳，找到各传感器最近的一帧
4. **同步检查**：如果所有传感器的时间差都在允许范围内（默认50ms），则保留该帧；否则丢弃

## State 和 Action 定义

### State（26维）

```
[Left_Arm(7), Left_Hand(6), Right_Arm(7), Right_Hand(6)]
```

- Left_Arm: 左臂7个关节位置（来自 joint/position 的前7列）
- Left_Hand: 左手6个自由度（来自 left_effector/position）
- Right_Arm: 右臂7个关节位置（来自 joint/position 的后7列）
- Right_Hand: 右手6个自由度（来自 right_effector/position）

### Action（26维）

采用绝对位置控制：

```
Action_t = State_{t+1}
```

对于最后一帧，复制前一帧的 Action。

## 依赖库

```bash
conda activate lerobot_conv
pip install h5py pandas numpy opencv-python tqdm pyarrow
```

**注意**：脚本已移除对 `datasets` 库的依赖，直接使用 pandas 处理 Parquet 文件。

## 注意事项

1. **时间戳格式**：所有时间戳应为纳秒（nanoseconds）
2. **图像格式**：输出使用 JPG 格式（质量95%），节省存储空间。路径符合 v3.0 标准格式
3. **内存使用**：处理大量 episode 时可能需要较大内存。脚本会按文件大小（默认100MB）自动分块
4. **时间同步**：如果相机之间时间差较大，可能需要调整 `max_time_diff_ms` 参数
5. **v3.0 格式**：生成的数据集完全符合 LeRobot v3.0 标准，可直接用于 Pi05 训练
6. **任务描述**：所有 episode 默认使用任务 "pick up and place the torque gun"，可在代码中修改

## 故障排除

### 问题：找不到 Head Camera 时间戳

**解决方案**：检查 `camera/head/color/` 目录是否存在，或检查 `camera/head_color/head_color.txt` 文件

### 问题：对齐后的帧数很少

**解决方案**：
- 增大 `max_time_diff_ms` 参数
- 检查各传感器的时间戳是否在合理范围内

### 问题：State 维度不正确

**解决方案**：检查 H5 文件中的关节数据格式，确保 `joint/position` 为 (N, 14)，`effector/position` 为 (N, 6)

## 输出文件说明

### info.json

包含数据集的基本信息和特征定义：

- `codebase_version`: "v3.0" - 数据集版本标识
- `total_episodes`: 总 episode 数
- `total_frames`: 总帧数
- `total_tasks`: 任务数量
- `tasks`: 任务列表
- `state_dim`: State 维度（应为26）
- `action_dim`: Action 维度（应为26）
- `data_path`: 数据文件路径模板
- `image_path`: 图像文件路径模板
- `fps`: 帧率（30.0）
- `features`: 特征定义（包含所有字段的类型和形状）

### stats.json

包含数据集的统计信息，用于归一化：

- `observation.state`: min, max, mean, std（26维）
- `action`: min, max, mean, std（26维）

### tasks.parquet

包含任务元数据：

- `task_index`: 任务索引
- 索引：任务字符串（如 "pick up and place the torque gun"）

### episodes/chunk-000/file-000.parquet

包含每个 episode 的元数据，用于快速定位数据：

- `episode_index`: Episode 索引
- `data/chunk_index`: 数据所在的 chunk
- `data/file_index`: 数据所在的文件
- `dataset_from_index`: 在数据集中的起始索引
- `dataset_to_index`: 在数据集中的结束索引
- `length`: Episode 长度

## 兼容性

✅ **完全兼容 LeRobot v3.0 标准**  
✅ **可直接用于 Pi05 模型训练**  
✅ **数据内容符合 Pi05 要求**（State/Action维度、图像格式、任务字段等）

生成的数据集可以直接使用 `LeRobotDataset` 加载：

```python
from lerobot.datasets.lerobot_dataset import LeRobotDataset

dataset = LeRobotDataset(
    repo_id="dummy",
    root="/path/to/lerobot_dataset"
)
```

