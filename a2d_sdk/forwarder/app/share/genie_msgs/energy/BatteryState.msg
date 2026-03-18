#G02 电池状态
std_msgs/Header     header
uint8       battery1_bms_charge_or_discharge            #电池1号BMS充放电状态   （0：放电状态；1：充电状态）
uint8       battery2_bms_charge_or_discharge            #电池2号BMS充放电状态   （0：放电状态；1：充电状态）
float32     battery1_bms_output_voltage                 #电池1号BMS输出电压   (单位： V)
float32     battery2_bms_output_voltage                 #电池2号BMS输出电压   (单位： V)
float32     battery1_bms_output_current                 #电池1号BMS输出电流   (单位： A)
float32     battery2_bms_output_current                 #电池2号BMS输出电流   (单位： A)
float32     battery1_bms_charge_current                 #电池1号BMS输入电流   (单位： A)
float32     battery2_bms_charge_current                 #电池2号BMS输入电流   (单位： A)
float32     battery1_bms_temperature                    #	电池1号BMS温度   (单位： ℃)
float32     battery2_bms_temperature                    #	电池2号BMS温度   (单位： ℃)
float32     battery1_bms_soc                            #电池1号BMS的SOC     (单位： 百分比 0%-100%)
float32     battery2_bms_soc                            #电池2号BMS的SOC     (单位： 百分比 0%-100%)
uint8       battery1_bms_soh                            #电池1号BMS的SOH     (单位： 百分比 0%-100%)   
uint8       battery2_bms_soh                            #电池2号BMS的SOH     (单位： 百分比 0%-100%)   
uint8       battery1_bms_short_circuit_fault_state      #电池1号BMS短路故障状态 (0:未发生电池短路； 1：发生电池短路)
uint8       battery2_bms_short_circuit_fault_state      #电池2号BMS短路故障状态 (0:未发生电池短路； 1：发生电池短路)
uint8       battery1_bms_open_circuit_fault_state       #电池1号BMS断路故障状态 (0: 未发生电池断路; 1: 发生电池断路)
uint8       battery2_bms_open_circuit_fault_state       #电池2号BMS断路故障状态 (0: 未发生电池断路; 1: 发生电池断路)
uint32      battery1_bms_other_fault_state              #电池1号BMS其他故障状态 (0: 无故障； 1-4294967295：故障码)
uint32      battery2_bms_other_fault_state              #电池2号BMS其他故障状态 (0: 无故障； 1-4294967295：故障码)
float32     battery1_outside_output_voltage             #电池1号外侧输出电压    (单位: V)
float32     battery2_outside_output_voltage             #电池1号外侧输出电压    (单位: V)   
uint8       battery1_outside_connection                 #电池1号外侧插头在位    （0：电池在位 1：电池不在位）
uint8       battery1_outside_open_circuit_fault_state   # 电池1号外侧短路故障状态 (0:电池在位 1：电池不在位)
uint8       battery2_outside_connection                 # 电池2号外侧插头在位    （0：电池在位 1：电池不在位）
uint8       battery2_outside_open_circuit_fault_state   #电池2号外侧短路故障状态 (0:电池在位 1：电池不在位)
float32     charge_plug_input_voltage                   #充电插头输入电压 (单位： V)
float32     charge_plug_input_current                   # 充电插头输入电流 (单位： A)
uint8       charge_plug_input_short_circuit_fault_state   # 	充电插头短路故障状态 (0:未发生充电插头短路 1：发生充电插头短路)
uint8       charge_plug_input_open_circuit_fault_state      #充电插头插反故障状态 (0:未发生充电插头插反 1：发生充电插头插反)
uint8       chassis_power_board_fault_state             #底盘电源板故障状态  (0:无故障 1-4294967295：故障码)
string       power_board_software_version                #软件版本号
string       power_board_hardware_version                #硬件版本号
string       power_board_serial_number                   #序列号