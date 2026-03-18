#!/bin/bash

# check if the user is root
if [ "$EUID" -ne 0 ]; then
  echo "Please run as root"
  exit 1
fi

CURRENT_SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)

cosine_bus=cosine_bus-2.0.0-cp310-cp310-linux_aarch64.whl
genie_msgs_pb=genie_msgs_pb-0.8.0-py3-none-any.whl
SDK_PACK_DIR="/home/agi/app/a2d_sdk/pack/a2d_sdk_server.tar.gz"
CURRENT_SCRIPT_DIR=$(cd "$(dirname "$0")" && pwd)
CURRENT_SDK_PATH=$CURRENT_SCRIPT_DIR/a2d_sdk

function install_a2d_service() {
    # check if the a2d service is already installed
    if systemctl is-active --quiet a2d_mode_switch_server; then
        echo "Service is already installed, disable it first..."
        systemctl stop a2d_mode_switch_server
        systemctl disable a2d_mode_switch_server
    fi

    cat << EOF | sudo tee /etc/systemd/system/a2d_mode_switch_server.service > /dev/null
[Unit]
Description=a2d_mode_switch_server
After=a2d_nvme.service

[Service]
ExecStart=/bin/bash $CURRENT_SCRIPT_DIR/scripts/start_mode_switch_server.sh
WorkingDirectory=$CURRENT_SCRIPT_DIR
Restart=always
User=$USER
Group=$USER
Environment=PATH=/usr/bin:/usr/local/bin
Environment=PYTHONUNBUFFERED=1

[Install]
WantedBy=multi-user.target
EOF

    # 重新加载 systemd 配置
    systemctl daemon-reload

    # 启动并设置为开机自启
    systemctl start a2d_mode_switch_server
    systemctl enable a2d_mode_switch_server

    # check if the service is running
    # systemctl status a2d_mode_switch_server
}

# 将a2d上的package拷贝到本地并解压缩
function copy_sdk_package() {
    cp -r $SDK_PACK_DIR ./
    tar --warning=no-timestamp -zxvf a2d_sdk_server.tar.gz -C $CURRENT_SCRIPT_DIR
    rm a2d_sdk_server.tar.gz
}

function install_sdk_package() {
    #install aarch64 cosine_bus
    pip install $CURRENT_SDK_PATH/$cosine_bus --force-reinstall

    # 安装genie_msgs_pb
    pip install $CURRENT_SDK_PATH/$genie_msgs_pb --force-reinstall --no-deps

    # 安装a2d_sdk
    a2d_sdk_whl=$(ls -t $CURRENT_SDK_PATH/a2d_sdk-*.whl | head -n 1)
    pip3 install $a2d_sdk_whl --force-reinstall
    
    mv $CURRENT_SDK_PATH/robot_service.py $CURRENT_SCRIPT_DIR/robot_service.py
    mv $CURRENT_SDK_PATH/a2d_env.sh $CURRENT_SCRIPT_DIR/a2d_env.sh
    rm -rf $CURRENT_SDK_PATH
}

function modify_bashrc() {
    # 检查是否存在 .bashrc 文件
    if [ -f "$HOME/.bashrc" ]; then
        # 备份原文件
        if [ ! -f "$HOME/.bashrc.backup" ]; then
            cp "$HOME/.bashrc" "$HOME/.bashrc.backup"
        fi
            
        # 检查是否存在环境变量
        if ! grep -q "source $CURRENT_SCRIPT_DIR/a2d_env.sh" "$HOME/.bashrc"; then
            echo "source $CURRENT_SCRIPT_DIR/a2d_env.sh" >> "$HOME/.bashrc"
        fi
            
        echo "bashrc 已修改,原文件已备份为 .bashrc.backup"
    else
        echo "未找到 .bashrc 文件"
    fi
}

function install_a2d_sdk_server() {
    if [ -d "$CURRENT_SDK_PATH" ]; then
        read -p "是否要删除现有的a2d_sdk, 或者将其备份? (y/n): " answer
        if [[ "$answer" =~ ^[Yy]$ ]]; then
            rm -rf $CURRENT_SDK_PATH
        else
            mv $CURRENT_SDK_PATH $CURRENT_SDK_PATH.backup
        fi
    fi
    mkdir -p $CURRENT_SDK_PATH
    copy_sdk_package
    install_sdk_package
    modify_bashrc
    
}

# 读取/data/version文件夹下所有模块的版本号，并写入total_version.txt
function read_version() {
    local target_dir="/data/version"
    local output_file="${target_dir}/total_version.txt"
    
    # 清空并重建文件
    : > "$output_file"  # 比touch更高效
    
    find "$target_dir" -maxdepth 1 -name "*.yaml" -print0 | while IFS= read -r -d '' file; do
        # 处理每个文件
        {
            # 保留原文件格式并添加分隔符
            awk '{print} END {print ""}' "$file"
            echo "---"  # 添加YAML文档分隔符
        } >> "$output_file"
    done
    
    # 删除最后一个多余的分隔符
    sed -i '$ d' "$output_file"
}


install_a2d_service
read_version

if [ "$1" = "on_x86" ]; then
  exit 0
elif [ -z "$1" ]; then
  install_a2d_sdk_server
else
  echo "unknown argument: $1"
  exit 1
fi




