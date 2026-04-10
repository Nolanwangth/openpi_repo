# frame id 无用, timestamp发送时间
std_msgs/Header header

# 语音播报开关
bool voice_output_switch

# 音量设置：0~100 对应 0%~100%
uint8 volume

# 语音控制开关
bool voice_control_switch

# 语音语言（如 "zh-CN", "en-US"）
string voice_language

# 语音播报风格
string voice_style

# 报警音开关
bool audio_alarm_switch

# 交互屏开关
bool interactive_screen_switch

# 交互屏亮度：0~100 对应 0%~100%
uint8 brightness

string uuid
string detail