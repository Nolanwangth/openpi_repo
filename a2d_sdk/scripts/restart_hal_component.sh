#!/bin/bash

component_name=$1

if [ -z "$component_name" ]; then
    echo "请提供组件名称作为参数"
    echo "可用命令："
    echo "  power-off           - 关闭电源"
    echo "  soft-estop         - 软急停"
    echo "  reset-hub1         - 重启HUB1(相机)"
    echo "  reset-hub2         - 重启HUB2(键鼠wifi-usbdebug)"
    echo "  reset-left-arm     - 重启左臂"
    echo "  reset-right-arm    - 重启右臂"
    echo "  reset-lift-motor   - 重启升降电机"
    exit 1
fi

case "$component_name" in
    "power-off")
        echo "执行关闭电源操作"
        sshpass -p 1 ssh -o StrictHostKeyChecking=no agi@10.42.0.101 "echo 1 | sudo -S /home/agi/app/bin/power_tool power-off"
        ;;
    "soft-estop")
        echo "执行软急停操作"
        sshpass -p 1 ssh -o StrictHostKeyChecking=no agi@10.42.0.101 "echo 1 | sudo -S /home/agi/app/bin/power_tool soft-estop"
        ;;
    "reset-hub1")
        echo "重启HUB1(相机)"
        sshpass -p 1 ssh -o StrictHostKeyChecking=no agi@10.42.0.101 "echo 1 | sudo -S /home/agi/app/bin/power_tool reset-hub1"
        ;;
    "reset-hub2")
        echo "重启HUB2(键鼠wifi-usbdebug)"
        sshpass -p 1 ssh -o StrictHostKeyChecking=no agi@10.42.0.101 "echo 1 | sudo -S /home/agi/app/bin/power_tool reset-hub2"
        ;;
    "reset-left-arm")
        echo "重启左臂"
        sshpass -p 1 ssh -o StrictHostKeyChecking=no agi@10.42.0.101 "echo 1 | sudo -S /home/agi/app/bin/power_tool reset-left-arm"
        ;;
    "reset-right-arm")
        echo "重启右臂"
        sshpass -p 1 ssh -o StrictHostKeyChecking=no agi@10.42.0.101 "echo 1 | sudo -S /home/agi/app/bin/power_tool reset-right-arm"
        ;;
    "reset-lift-motor")
        echo "重启升降电机"
        sshpass -p 1 ssh -o StrictHostKeyChecking=no agi@10.42.0.101 "echo 1 | sudo -S /home/agi/app/bin/power_tool reset-lift-motor"
        ;;
    *)
        echo "无效的命令: $component_name"
        exit 1
        ;;
esac