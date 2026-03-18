#!/bin/bash

if [ -f /home/agi/latest/a2d-ci/install/runtime/loadmc/.downloaded-latest/package/bin/tools/retarget_trans.py ]; then
    export PYTHONPATH=$PYTHONPATH:/usr/lib/python3/dist-packages
    export ROS_LOCALHOST_ONLY=0
    source /opt/ros/humble/setup.bash
    cd /home/agi/latest/a2d-ci
    source ./install/setup.bash
    source ./install/runtime/loadmc/.downloaded-latest/package/share/genie_msgs/local_setup.bash
    python3 ./install/runtime/loadmc/.downloaded-latest/package/bin/tools/retarget_trans.py
else
    echo "mc_adapter not found"
fi
