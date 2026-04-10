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
