# frame id 无用, timestamp发送时间
std_msgs/Header header

uint32 map_id
uint32 map_version

nav_msgs/OccupancyGrid map
geometry_msgs/Polygon[] walls
geometry_msgs/Polygon[] infeasible_areas

string uuid
string detail