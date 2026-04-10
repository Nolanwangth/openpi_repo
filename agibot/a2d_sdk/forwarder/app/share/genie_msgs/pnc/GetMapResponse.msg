std_msgs/Header header

# 0: 命令执行成功
# 1: 命令执行失败
uint8 SUCCESS=0
uint8 FAIL=1
uint8 result

uint32 id
uint32 version

nav_msgs/OccupancyGrid map
geometry_msgs/Polygon[] walls
geometry_msgs/Polygon[] infeasible_areas

string uuid
string reason