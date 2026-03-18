std_msgs/Header header

string name                     # 磁盘标识（如 "main_ssd", "usb1", "emmc"）
uint64 total_capacity_mb        # 总容量
uint64 used_capacity_mb         # 已用容量
uint64 available_capacity_mb    # 可用容量
float32 usage_ratio             # 使用率（0.0 ~ 1.0）
bool mounted                    # 是否已挂载
string mount_point              # 挂载路径（如 "/"、"/mnt/usb1"）