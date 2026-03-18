#! /bin/bash

current_dir=$(dirname $(readlink -f $0))

if [ -f $current_dir/a2d_mode_switch_server.pyc ]; then
    python3 $current_dir/a2d_mode_switch_server.pyc
else
    python3 $current_dir/a2d_mode_switch_server.py
fi
