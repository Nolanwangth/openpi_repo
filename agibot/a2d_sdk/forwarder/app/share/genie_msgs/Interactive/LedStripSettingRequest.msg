std_msgs/Header header

bool led_switch

# 亮度（0~100%，可选，默认 100）
uint8 brightness

# 动画/模式类型，例如：solid（常亮）、blink（闪烁）、wave（波动）、breath（呼吸灯）
string mode

# 更新频率（某些动画模式下需要，单位：Hz）
float32 update_rate


string uuid
string detail