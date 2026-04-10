# frame id 无用, timestamp发送时间
std_msgs/Header header

# 控制模式来源
# 0: unknown
# 1: 遥操作遥控
# 2： HMI遥控
# 3： GDK遥控
# 8:  自主导航模式
uint8 control_source

# 底盘运动模式
# 0：阿卡曼
# 1：原地转向
# 2：蟹行
# 3：固定模式
# 6：自定义
uint8 control_mode