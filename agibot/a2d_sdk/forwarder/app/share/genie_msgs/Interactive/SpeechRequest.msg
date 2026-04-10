std_msgs/Header header

# 要播报的文本内容
string text

# 播报优先级，数值越大优先级越高
int32 priority

# 语音语言（如 "zh-CN", "en-US"）
string voice_language

# 语音播报风格
string voice_style

# 是否是紧急播报（跳过排队，立即播）
bool urgent

string uuid
string detail