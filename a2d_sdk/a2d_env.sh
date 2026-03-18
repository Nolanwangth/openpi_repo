#!/bin/bash

# usage: source env.sh [ros_domain_id]

# if [ -z "$1" ]; then
#     export ROS_DOMAIN_ID=88
# else
#     export ROS_DOMAIN_ID=$1
# fi

export LOCATOR_IP=10.42.0.101
export AORTA_DISCOVERY_URI=http://10.42.0.101:2379

#gdk log dir
LOG_DIR="/data/logs/sdk"
mkdir -p $LOG_DIR

export PROTOCOL_BUFFERS_PYTHON_IMPLEMENTATION=python
export DYLOG_log_dir=$LOG_DIR
export DYLOG_LOG_SIZE=20000
export DYLOG_DEFAULT_LEVEL=FATAL

# 存在ros2则source
if [ -f "/opt/ros/humble/setup.bash" ]; then
    source /opt/ros/humble/setup.bash
    export ROS_VERSION=2
    export ROS_PYTHON_VERSION=3
    export ROS_LOCALHOST_ONLY=1
    export ROS_DISTRO=humble
    export RMW_IMPLEMENTATION=rmw_fastrtps_cpp
    
    ros2 daemon stop
    ros2 daemon start

    if [ -f "/home/agi/app/share/genie_msgs/local_setup.bash" ]; then
        source /home/agi/app/share/genie_msgs/local_setup.bash
    fi
fi