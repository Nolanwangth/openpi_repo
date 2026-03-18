#!/bin/bash

# test this using following command:
# bash scripts/genie_store_auto_deploy.sh
# docker exec -it genie_store_env launch  go_app:test_gma_package3 gs_test 4090

# Function to detect the system architecture
get_architecture() {
    local arch=$(uname -m)
    if [[ $arch == *"x86_64"* ]]; then
        echo "X86_64"
    elif [[ $arch == *"arm"* || $arch == *"aarch64"* ]]; then
        echo "AARCH64"
    else
        echo "Unknown"
    fi
}

# Function to generate the entry.sh script
generate_entry_script() {
    cat > entry.sh << 'EOF'
#!/bin/bash

if [ $# -lt 2 ]; then
    echo "Usage: $0 <model_version> <gs_user> <gs_target>"
    echo "model_version: TAG:VERSION"
    echo "gs_user: gs_user"
    echo "gs_target: gs_target"
    exit 1
fi

set -e
set -x

args=("$@")
model_version=${args[0]}
user=${args[1]}
target=${args[2]}

model_version_flag=${model_version//:/_}
model_version_flag=${model_version_flag//\#/_}
model_version_flag=${model_version_flag//\//_}
echo "model_version_flag: $model_version_flag"

mkdir -p ~/.gs_cache

if ! mount | grep -q "172.21.7.166:/var/openebs/local/gs_test"; then
    mount -t nfs 172.21.7.166:/var/openebs/local/gs_test /nfs_datas -o nolock || echo "mount nfs failed"
fi

if ! mount | grep -q "//172.21.4.32/NAS"; then
    mount -t cifs //172.21.4.32/NAS /cifs_datas -o rw,vers=2.0,file_mode=0777,dir_mode=0777 || echo "mount cifs failed"
fi
export GS_NFS_LOCAL=/nfs_datas

if [ ! -d /data ]; then
    echo "/data doesn't exist in container"
    exit 1
fi

model_cache_dir=/data/.gs_cache/${model_version_flag}_${target}_cache
if [[ $model_version == *":"* ]]; then
  echo "GS Unpack_app from app id : ${model_version}"
  gscmd unpack_app --app_id=${model_version} --target=${target} --output=${model_cache_dir} --user=${user}
else
  echo "GS Unpack_app from package : ${model_version}"
  gscmd unpack_app --package=${model_version} --output=${model_cache_dir} --user=${user}
fi
source ${model_cache_dir}/setup.sh

gma_installer_file=$(find $model_cache_dir -name "gma_installer*.tar.gz")
if [ -z "$gma_installer_file" ]; then
    echo "gma_installer tarball not exist"
    exit 1
fi

gma_version=$(md5sum $gma_installer_file | awk '{print $1}')
deploy_gma=false
if [ -f /root/gma_version ]; then
    exist_gma_version=$(cat /root/gma_version)
else
    exist_gma_version="gma_not_exist"
fi
if [ "$exist_gma_version" == "$gma_version" ]; then
    echo "gdk environment is ready, skip deploy"
else
    echo "gdk environment is not ready, deploy"
    deploy_gma=true
fi

GMA_DIR=/root/app/gma

if [ "$deploy_gma" == "true" ]; then
    echo "deploy gma"
    tar -zxf $gma_installer_file -C /root/

    cd $GMA_DIR
    echo "install dep"
    bash ./scripts/install_from_a2d.sh
    echo $gma_version > /root/gma_version
fi

args="--config ${model_cache_dir}/gma_deploy.yml"
echo $args > $GMA_DIR/gui/genie_store_app
cd $GMA_DIR/
uv run gui/cosine_app.py 2>&1 > $GMA_DIR/gui.log &

echo "================================================================"
echo "GMA APP已经启动，请打开 http://127.0.0.1:7860 开始体验！"
echo "第一次打开页面，请先切换模式"
echo "然后点击开启模型，模型推理服务的日志会显示在当前控制台："
echo "================================================================"

if [ -f $GMA_DIR/server.log ]; then
    rm $GMA_DIR/server.log
fi
touch $GMA_DIR/server.log
tail -f $GMA_DIR/server.log

EOF
}

# Function to generate the Dockerfile based on the architecture
generate_dockerfile() {
    local arch=$1
    if [[ $arch == "X86_64" ]]; then
        cat > Dockerfile.gma << EOF
FROM registry.agibot.com/genie-edge-engineering/genie_store:x86_deploy
ENV PATH=/root/.local/bin:$PATH
RUN pip3 install uv -i https://mirrors.aliyun.com/pypi/simple/
COPY entry.sh /usr/local/bin/launch
RUN chmod +x /usr/local/bin/launch
EOF
    elif [[ $arch == "AARCH64" ]]; then
        cat > Dockerfile.gma << EOF
FROM registry.agibot.com/genie-edge-engineering/genie_store:orin_deploy
ENV PATH=/root/.local/bin:$PATH
COPY entry.sh /usr/local/bin/launch
RUN chmod +x /usr/local/bin/launch
EOF
    fi
}

# Function to remove an existing container if it exists
remove_existing_container() {
    local container_name=$1
    if docker ps -a | grep -q "$container_name"; then
        echo "$container_name container exists, will remove it"
        docker rm -f "$container_name"
    fi
}

# Function to check and pull a Docker image
check_and_pull_image() {
    local tag=$1
    if ! docker images | grep -q "genie_store" | grep -q "$tag"; then
        echo "image genie_store:$tag does not exist, try pull it first"
        docker pull registry.agibot.com/genie-edge-engineering/genie_store:$tag
        if [ $? -ne 0 ]; then
            echo "pull image genie_store:$tag failed"
            exit 1
        fi
    fi
}

# Function to remove an existing Docker image if it exists
remove_existing_image() {
    local image_name=$1
    if docker images | grep -q "$image_name"; then
        echo "image $image_name exists, will remove it"
        docker rmi "$image_name"
    else
        echo "image $image_name does not exist"
    fi
}

# Function to run a Docker container based on the architecture
run_docker_container() {
    if [ ! -d /data ]; then
        echo "data directory does not exist, please mount a data directory to /data"
        exit 1
    fi
    local arch=$1
    if [[ $arch == "X86_64" ]]; then
        docker run -itd --gpus all --privileged --restart unless-stopped --net=host --name genie_store_env -v /data:/data  -w /root/ gma_env:latest
    elif [[ $arch == "AARCH64" ]]; then
        docker run -itd --gpus all --privileged --runtime=nvidia --restart unless-stopped --net=host --name genie_store_env -v /data:/data  -v /home/agi:/home/agi  -w /root/ gma_env:latest
    fi
}

# Main execution flow
ARCH=$(get_architecture)
if [[ $ARCH == "Unknown" ]]; then
    echo "Unable to identify the current system architecture"
    exit 1
fi

generate_entry_script
generate_dockerfile "$ARCH"
remove_existing_container "genie_store_env"

if [[ $ARCH == "X86_64" ]]; then
    check_and_pull_image "x86_deploy"
elif [[ $ARCH == "AARCH64" ]]; then
    check_and_pull_image "orin_deploy"
fi

remove_existing_image "gma_env:latest"
docker build -t gma_env:latest . -f Dockerfile.gma
run_docker_container "$ARCH"