# PI05 TCP 部署说明（Client/Server）

这份文档对应两个脚本：

- 模型服务端（`pi05_env`）：`agibot/agibot_pi05_server.py`
- 机器人客户端（`gdk_env`）：`agibot/agibot_client.py`

目标是让机器人以 **30Hz** 驱动：每 33ms 采集观测与执行动作；模型端采用 **chunk 请求模式**（一次返回 50 步），客户端按本地节奏消耗动作并按需要重请求。

---

## 1. 架构总览

### 1.1 数据流

1. `agibot_client.py`（机器人端）每个周期读取最新：
   - 26 维状态（臂 14 + 手 12）
   - 三路图像（`head` / `left_wrist` / `right_wrist`）
2. 客户端在“需要重规划”时，通过 TCP 发 `chunk_request`（带最新观测 + RTC上下文）给服务端。
3. `agibot_pi05_server.py` 收到后：
   - 走 LeRobot 官方 `preprocessor`
   - 调用 `PI05Policy.predict_action_chunk(...)`
   - 启用 RTC 参数（`inference_delay`, `prev_chunk_left_over`, `execution_horizon`）
   - 返回完整 `action_chunk`（默认50步）
4. 客户端本地按 30Hz 逐步执行 chunk；执行到 `request_horizon`（默认10步）再次请求新 chunk。

### 1.2 节奏是谁驱动

- 节奏由 **客户端** 驱动（30Hz）。
- 服务端是请求-响应型：收到一帧观测，返回一段动作 chunk。

---

## 2. 环境要求

### 2.1 服务端（模型）

- conda 环境：`pi05_env`
- 模型路径默认：`lerobot/pi05_base`
- 需要 GPU（推荐 CUDA）

### 2.2 客户端（机器人）

- conda 环境：`gdk_env`
- 依赖 `a2d_sdk`
- `agibot_client.py` 已支持自动加载 `a2d_sdk/env.sh`（不再要求手动 source）
  - 默认路径：`/home/nolan/vla/openpi_repo/agibot/a2d_sdk`
  - 可通过 `--a2d-sdk-dir` 覆盖

---

## 3. 启动步骤

### 3.1 先启动服务端

```bash
conda run -n pi05_env python agibot/agibot_pi05_server.py \
  --host 127.0.0.1 \
  --port 9000 \
  --model-path lerobot/pi05_base \
  --task "pick up the torque gun" \
  --execution-horizon 10 \
  --blend-steps 8
```

### 3.2 再启动客户端

```bash
conda run -n gdk_env python agibot/agibot_client.py \
  --host 127.0.0.1 \
  --port 9000 \
  --hz 30 \
  --task "pick up the torque gun" \
  --request-horizon 10 \
  --execution-horizon 10
```

如果 `a2d_sdk` 不在默认目录，增加：

```bash
--a2d-sdk-dir /your/path/to/agibot/a2d_sdk
```

---

## 4. TCP 协议定义

当前协议是 **JSON Lines**（每条消息一行，`\n` 结尾）。

### 4.1 Client -> Server（chunk_request）

```json
{
  "type": "chunk_request",
  "timestamp": 1712345678.123,
  "task": "pick up the torque gun",
  "joints": [ ... >=26维 ... ],
  "images": {
    "head": {"encoding":"jpeg_base64","data":"..."},
    "left_wrist": {"encoding":"jpeg_base64","data":"..."},
    "right_wrist": {"encoding":"jpeg_base64","data":"..."}
  },
  "inference_delay": 10,
  "execution_horizon": 10,
  "prev_chunk_left_over": [[...26维...], [...]]
}
```

服务端也兼容：

- `images.*` 直接传 `HxWx3` 的 list
- `encoding: raw_uint8_hwc` + `shape`

### 4.2 Server -> Client（action_chunk）

```json
{
  "type": "action_chunk",
  "timestamp": 1712345678.456,
  "actions": [[...26维...], [...], ...],
  "rtc_enabled": true,
  "chunk_id": 123,
  "chunk_size": 50
}
```

---

## 5. PI05 + RTC 在服务端如何工作

- PI05 每次推理产生一个 action chunk（默认 50 步）。
- 客户端执行到一定步数（`request_horizon`）时，用当前 chunk 残余作为 `prev_chunk_left_over` 触发下一次推理。
- RTC 通过 `predict_action_chunk(..., inference_delay, prev_chunk_left_over, execution_horizon)` 生效。

参数建议：

- `--execution-horizon 10`
- `--blend-steps 8`

---

## 6. 常见问题

### 6.1 客户端连不上服务端

- 先确认服务端已启动并监听同一 host/port
- 检查防火墙与端口占用

### 6.2 模型端 OOM

- 关闭占用 GPU 的其他进程
- 降低并发，仅保留单客户端

### 6.3 客户端只有 env.sh 日志无后续

- 这是 `a2d_sdk/env.sh` 的启动输出
- 关注后续是否出现：`[client] connected to server ...`

### 6.4 图像不是 224x224 能用吗

- 可以
- 服务端 preprocessor 会自动 resize/pad 到模型配置分辨率

---

## 7. 以后替换成“其他 server”，客户端还能不能复用

结论：**大概率可以复用，前提是保持协议一致。**

### 7.1 完全可复用的条件

新 server 满足：

1. 接收同样的 observation JSON 字段（尤其 `joints` + `images`）
2. 返回同样的 action JSON 字段（至少包含 `action` 且维度为 26）
3. 一次请求返回一步动作（或客户端可按你约定方式取一步）

则 `agibot_client.py` 基本不需要改。

### 7.2 需要改客户端的场景

- 返回动作维度不是 26（例如 32）
- 不是 request/response 模型（例如纯流式推送）
- 图像字段或编码变更（非 `jpeg_base64`/`raw_uint8_hwc`）
- 你希望客户端执行策略变化（比如动作滤波、安全联锁）

### 7.3 推荐做法

为长期复用，建议把协议版本写入消息：

- `protocol_version: "v1"`
- server/client 都检查版本，不匹配直接报错

---

## 8. 文件职责

- `agibot/agibot_pi05_server.py`
  - PI05 模型加载
  - 预处理/后处理
  - RTC + chunk 融合
  - TCP 服务

- `agibot/agibot_client.py`
  - 自动加载 `a2d_sdk/env.sh`
  - 30Hz 采集与执行
  - 按 `request_horizon` 请求新 chunk，并调用 `ArmHand30Hz.command` 执行

- `agibot/arm_hand_policy_interface.py`
  - 机器人臂手状态读取与动作下发
  - 限幅/安全相关逻辑

