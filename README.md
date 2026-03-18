# OpenPI Repo (Agibot to LeRobot)

本项目用于 **Agibot (灵巧手/机器人)** 数据到 **LeRobot** 格式的转换与训练。集成了 `lerobot` 库和 `a2d_sdk` 通信工具。

---

## 🛠️ 环境指南 (Conda Environments)

本项目涉及三个核心环境，请根据任务切换：

| 环境名称 | 核心用途 | 关键组件 |
| :--- | :--- | :--- |
| `agipi` | **主开发/训练** | `torch`, `accelerate`, `pi05_base` |
| `agipi_robo` | **实机控制** | `a2d-sdk`, `cosine-bus` (底层硬件通信) |
| `lerobot_conv` | **数据转换备份** | `h5py`, `numpy` |

> **激活主环境指令**: `conda activate agipi`

---

## 📂 仓库结构说明

* `lerobot/`: 核心算法库（已脱离嵌套 Git，作为普通文件夹管理）。
* `a2d_sdk/`: 机器人硬件驱动与通信 SDK。
* `convert_agibot_to_lerobot.py`: 将 Agibot 原始数据转换为 LeRobot 格式的主脚本。
* `.gitignore`: 已配置 **14GB 数据集保护**，防止误传大型权重和 `.h5` 文件。

---

## 🚀 开发工作流

### 1. 提交代码 (Git Graph / CLI)
修改代码后，请确保不要包含大型二进制文件：
```bash
git add .
git commit -m "feat: 描述你的改动"
git push origin main