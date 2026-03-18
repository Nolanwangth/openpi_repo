#!/bin/bash

if [ -f /home/agi/latest/a2d-ci/install/runtime/loadmc/.downloaded-latest/package/bin/start_mc.sh ]; then
    export ROS_LOCALHOST_ONLY=0
    source /opt/ros/humble/setup.bash
    cd /home/agi/latest/a2d-ci
    source ./install/setup.bash
    bash ./install/runtime/loadmc/.downloaded-latest/package/bin/start_mc.sh
else
    echo "mc_app not found"
fi
