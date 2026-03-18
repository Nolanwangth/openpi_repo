#!/bin/bash

# 创建并进入日志目录
log_dir=/data/logs/sdk
mkdir -p $log_dir
cd $log_dir

# 创建从日志目录到install.sh的符号链接
# 如果已存在则先删除
rm -f install.sh
rm -f genie_store_auto_deploy.sh
rm -f gdk_server_installer.tar.gz
rm -f version
ln -s /home/agi/app/a2d_sdk/scripts/install.sh install.sh
ln -s /home/agi/app/a2d_sdk/scripts/genie_store_auto_deploy.sh genie_store_auto_deploy.sh
ln -s /home/agi/app/a2d_sdk/pack/a2d_sdk_server.tar.gz gdk_server_installer.tar.gz
ln -s /home/agi/app/a2d_sdk/version version

# 创建从日志目录到total_version.txt的符号链接
# 如果已存在则先删除
rm -f total_version.txt
ln -s /data/version/total_version.txt total_version.txt

# 创建从日志目录到/data/parameters的符号链接
# 如果已存在则先删除
rm -f parameters
ln -s /data/parameters camera_parameters

# 启动HTTP服务器，使用8849端口
python3 -m http.server 8849 2>&1