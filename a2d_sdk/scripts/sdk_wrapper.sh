#!/bin/bash

action_value=$1
action_param=$2

model=""
action_param_list=("idle" "copilot" "develop" "compressed_image" "vr")
SCRIPTPATH=/home/agi/app
HOMEPATH=$SCRIPTPATH
CONFPATH=$SCRIPTPATH/a2d_sdk/conf
if [ ! -d $SCRIPTPATH ]; then
    >&2 echo "[ERROR] app path not exists"
    exit 1
fi

export CB_PROC_THREADS_NUM=1
export DYLOG_ASYNC_INTERVAL=5000
export DYLOG_log_dir=/data/logs/
export DYLOG_LOG_SIZE=20000
/usr/bin/mkdir -p $DYLOG_log_dir
/usr/bin/chown -R agi:agi $DYLOG_log_dir

cd $SCRIPTPATH
source $SCRIPTPATH/env.sh $SCRIPTPATH/lib

if [ "$action_value" == "restart" ]; then
    $HOMEPATH/bin/scene_control restart $action_param
    exit 0
fi

if [ "$action_param" == "" ]; then
    model="idle"
else 
    model=$action_param
fi

if [[ ! " ${action_param_list[@]} " =~ " ${model} " ]]; then
    echo "unknown action param: $action_param"
    exit 1
fi

if [ "$action_value" == "start" ]; then
    $HOMEPATH/bin/scene_control switch $model
elif [ "$action_value" == "stop" ]; then
    $HOMEPATH/bin/scene_control switch idle
else
    >&2 echo "unknown action type: $action_value"
fi