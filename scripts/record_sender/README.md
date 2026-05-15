
#指令


cd ~/vla/openpi_repo/scripts/record_sender
./pull_record_by_task.sh 'dig0513'



















# record_sender

从机器人拉录制到本机 `~/Desktop/datasets_raw/`（`rsync`，不删机器人上的文件）。

在本机终端里执行（先 `cd` 到本目录）：

```bash
cd ~/vla/openpi_repo/scripts/record_sender
```

**拉一个任务（只按 `templates.name` 精确匹配，不必传备注；先在本机 `DEST/任务名/` 下建顶层文件夹，其内每条 episode 子目录名为机器人上的 **原始 uuid**。每条 episode 传完后会在该任务大文件夹下的 `Video/` 里生成 **`<uuid>.mp4`**（与 episode 文件夹名一致，便于对照查找；由 `camera/head/color` 下 jpg 合成，默认 30fps，需 `ffmpeg`）。不想生成视频：`--no-mp4`。改帧率：`--mp4-fps 15` 或环境变量 `RECORD_PULL_MP4_FPS`。**

```bash
./pull_record_by_task.sh 'dig 0513'
# 例如：~/Desktop/datasets_raw/dig 0513/<uuid>/ 与 ~/Desktop/datasets_raw/dig 0513/Video/<uuid>.mp4
```

**按名字里包含某段字拉多个任务（每个任务一个子文件夹）：**

```bash
./pull_record_by_task.sh --name-contains dig
```

**先看会拉哪些、不真传：**

```bash
./pull_record_by_task.sh '任务名' --dry-run
```

密码默认已写在脚本里；换密码：`export ROBOT_SSH_PASS='你的密码'`。详细参数：`./pull_record_by_task.sh --help`（或 `python3 pull_record_by_task.py --help`）。

若 Conda 里 `python3` 报 OpenSSL，用：`/usr/bin/python3 pull_record_by_task.py ...`（参数同上）。
