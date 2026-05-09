#进入copilot模式
python3 robot_service.py -s -c ./conf/copilot.pbtxt

#进入Vr模式
python3 robot_service.py -s -c ./conf/vr.pbtxt

#灵巧手触觉输出
ros2 topic echo /hal/left_ee_force --once

#robotdds 函数的地址
gedit /home/nolan/anaconda3/envs/gdk_env/lib/python3.10/site-packages/a2d_sdk/robot.py



#大拇指，食指，中指，无名指，小指，拇指弯

ha 36.75,176,173.8,174.3,172.6,1
ha 2.2 , 100.2, 97.8, 101.4, 98.8, 89.8


手指 / 关节    上限 (Max)     下限 (Min)
大拇指         36.75             2.2
食指           176.0            100.2
中指           173.8            97.8
无名指         174.3            101.4
小指           172.6            98.8
拇指弯          1.0            89.8

#gdk使用前需要
conda activate gdk_env
cd vla/OPENPI_REPO/agibot/a2d_sdk
source env.sh

#pi05的环境
#打开另一个终端
conda activate pi05_env






#终端A 冒烟测试 mock service


conda activate gdk_env
cd /home/nolan/vla/openpi_repo
PYTHONUNBUFFERED=1 python agibot/agibot_pi05_mock_trajectory_server.py --host 127.0.0.1 --port 9000



# 终端A

conda activate pi05_env
cd /home/nolan/vla/openpi_repo
PYTHONUNBUFFERED=1 /home/nolan/anaconda3/envs/pi05_env/bin/python -u agibot/agibot_pi05_server.py \
  --host 0.0.0.0 \
  --port 9000 \
  --model-path lerobot/pi05_base \
  --task "pick up the torque gun" \
  --execution-horizon 50 \
  --blend-steps 40


#终端B socket监控
cd /home/nolan/vla/openpi_repo
PYTHONUNBUFFERED=1 python agibot/agibot_socket_sniff_proxy.py \
  --listen-host 127.0.0.1 --listen-port 9100 \
  --upstream-host 127.0.0.1 --upstream-port 9000





#终端C client机器人
conda activate gdk_env
cd /home/nolan/vla/openpi_repo/agibot/a2d_sdk
source env.sh
cd /home/nolan/vla/openpi_repo
python agibot/agibot_client.py \
  --host 127.0.0.1 \
  --port 9100 \
  --hz 30 \
  --task "pick up the torque gun" \
  --request-horizon 20 \
  --execution-horizon 50


#终端C' mock client（环境、参数同终端C；真读 state/相机，动作仅终端 print，不下发机械臂）
conda activate gdk_env
cd /home/nolan/vla/openpi_repo/agibot/a2d_sdk
source env.sh
cd /home/nolan/vla/openpi_repo
python agibot/agibot_client_mock.py \
  --host 127.0.0.1 \
  --port 9100 \
  --hz 30 \
  --task "pick up the torque gun" \
  --request-horizon 20 \
  --execution-horizon 50


  
