#G02 上半身电源状态
std_msgs/Header     header
uint8 power_onoff_req                               #电源开关上下电请求      (0: 电源开关下电; 1:电源开关上电)
uint8 emergency_stop_button_req                      #急停开关请求      (0:急停未激活;  1: 急停激活)
uint8 power_button_fault_state                      #电源开关故障状态  (0:电源开关正常;  1: 电源开关故障)
uint8 emergency_stop_button_fault_state             #急停开关故障状态 （0: 急停开关正常;  1: 急停开关故障)
uint8 power_full_low_req                            #电源开关全功率和低功率请求 (0: 电源开关全功率;  1: 电源开关低功率)
uint8 chest_power_board_power_state                 #胸腔电源板电源状态 (0: 低功率状态;  1:  全功率状态)
uint8 domain_controller_power_state                 #域控制器供电开关状态 (0: 切断供电;  1:  正常供电)
uint8 head_interactive_board_power_state            #交互板供电开关状态 (0: 切断供电;  1: 正常供电)
uint8 curved_screen_power_state                     #曲面屏供电开关状态 (0: 切断供电;  1: 正常供电)
uint8 head_yaw_motor_power_tate                     #头部航向电机供电开关状态 (0: 切断供电;  1: 正常供电)
uint8 head_pitch_motor_power_state                  #头部俯仰电机供电开关状态 (0: 切断供电;  1: 正常供电)
uint8 waist_yaw_motor_power_state                   #腰部航向电机供电开关状态   (0: 切断供电;  1: 正常供电)
uint8 waist_pitch_motor_power_state                 #腰部俯仰电机供电开关状态 (0: 切断供电;  1: 正常供电)
uint8 leg_bending1_motor_power_state                #腿部弯折1号电机供电开关状态 (0: 切断供电;  1: 正常供电)
uint8 leg_bending2_motor_power_state                #腿部弯折2号电机供电开关状态 (0: 切断供电;  1: 正常供电)
uint8 leg_bending3_motor_power_state                #腿部弯折2号电机供电开关状态 (0: 切断供电;  1: 正常供电)
uint8 left_arm_power_state                          #左臂电机供电开关状态   (0: 切断供电;  1: 正常供电)
uint8 right_arm_power_state                         #右臂电机供电开关状态   (0: 切断供电;  1: 正常供电)
uint8 chest_light_strip_power_state                 #胸腔灯带供电开关状态   (0: 切断供电;  1: 正常供电)
uint8 fan_power_state                               #风扇供电开关状态   (0: 切断供电;  1: 正常供电)
uint8 mocap_poe_power_state                         #动捕POE供电开关状态    (0: 切断供电;  1: 正常供电)
uint8 ipad_power_state                              #IPAD供电开关状态   (0: 切断供电;  1: 正常供电)
uint8 chest_reserved_lidar_power_state              #胸腔预留激光雷达供电开关状态   (0: 请求关闭供电开关;  1: 请求打开供电开关)
uint32 chest_power_board_fault_state                #胸腔电源板故障状态     (0: 无故障;  1-4294967295: 故障码)
string power_board_software_version                  #软件版本号
string power_board_hardware_version                  #硬件版本号
string power_board_serial_number                     #序列号
