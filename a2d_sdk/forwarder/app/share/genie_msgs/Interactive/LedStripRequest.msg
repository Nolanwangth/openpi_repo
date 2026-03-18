std_msgs/Header header

# 灯带颜色，使用RGB格式，范围0~255
uint8 r
uint8 g
uint8 b

# 亮度（0~100%，可选，默认 100）
uint8 brightness

# 动画/模式类型，例如：solid（常亮）、blink（闪烁）、wave（波动）、breath（呼吸灯）
string mode

# 持续时间（单位：秒；0 表示无限持续）
float32 duration

# 更新频率（某些动画模式下需要，单位：Hz）
float32 update_rate

# 是否循环播放动画（适用于 wave, blink 等模式）
bool loop

# 是否立即打断之前的灯光状态
bool override

string uuid
string detail