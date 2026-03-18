#!/bin/bash

export PS4='+ ${BASH_SOURCE}:${LINENO}: '
# set -e
set -x

if [[ $# -ne 1 && $# -ne 2 ]]; then
    echo "Usage: $0 安装包网址或路径"
    exit 1
fi

if [ "$EUID" -ne 0 ]; then
    echo "Please run as root"
    exit 1
fi

CURRENT_DIR=$(cd $(dirname $0); pwd)

# 检查是网址还是路径
if [[ $1 =~ ^https?:// ]]; then
    gdk_installer_url=$1
    gdk_installer_path=""
else
    gdk_installer_url=""
    gdk_installer_path=$1
fi

function install_package() {
    # 处理安装包
    if [ "$gdk_installer_url" != "" ]; then
        wget $gdk_installer_url -O $CURRENT_DIR/gdk_installer.tar.gz
    fi
    if [ "$gdk_installer_path" != "" ]; then
        mv $gdk_installer_path $CURRENT_DIR/gdk_installer.tar.gz
    fi
    tar -zxvf $CURRENT_DIR/gdk_installer.tar.gz -C $CURRENT_DIR

    # 处理gdk.tar.gz到~/.agibot_app_cache
    mkdir -p ~/.cache/agibot
    rm -rf ~/.cache/agibot/*
    tar -zxvf $CURRENT_DIR/agibot_app/gdk.tar.gz -C ~/.cache/agibot

    # 处理gui.tar.gz到本目录
    # tar -zxvf $CURRENT_DIR/agibot_app/gui.tar.gz -C $CURRENT_DIR

    # 删除中间产物
    rm -rf $CURRENT_DIR/agibot_app
    rm -rf $CURRENT_DIR/gdk_installer.tar.gz
}

function install_gdk() {
    # 安装gdk依赖
    cd ~/.cache/agibot/gdk
    # 使用子shell执行，这样即使install_sdk_dep.sh中有exit 0，主脚本也会继续执行
    (
        # 安装gdk依赖
        bash install_sdk_dep.sh deploy_all
    ) || true  # 添加|| true确保即使子命令失败也会继续执行
}

function install_gui() {
    gui_dir=$CURRENT_DIR/gui
    cd $gui_dir
    chmod a+x start_gui.sh
    # write a shell script to start the gui
tee /usr/local/bin/agibot > /dev/null << EOF
#!/bin/bash
cd $gui_dir
./start_gui.sh
EOF
    chmod a+x /usr/local/bin/agibot
}

install_package
install_gui
install_gdk
echo "Installation complete."
echo "Run 'agibot' to start, then open http://127.0.0.1:7860/ to use."