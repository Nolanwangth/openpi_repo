# frame id 无用, timestamp发送时间
std_msgs/Header header

# 控制模式输入
# 0: 遥操作
# 1：HMI：
# 2: 自主模式
uint8 control_mode

# 默认为安全模式
uint8 safe_mode

string uuid
string detail