#include "noitom_streamer.hpp"

using namespace MocapApi;

NoitomStreamer::NoitomStreamer(const rclcpp::NodeOptions & options)
    : Node("noitom_streamer", options)
{

    RCLCPP_INFO(this->get_logger(), "NoitomStreamer 开始初始化");

    // ROS 参数设置
    this->declare_parameter<uint16_t>("/remote/mocap/hub_port", 8080);
    this->declare_parameter<std::string>("/remote/mocap/hub_ip_address", "10.42.0.202");
    // this->declare_parameter<std::string>("/remote/mocap/hub_ip_address", "172.16.37.128");
    // this->declare_parameter<uint16_t>("/remote/mocap/hub_port", 7003);
    this->declare_parameter<uint16_t>("/remote/mocap/orin_port", 8002);
    this->declare_parameter<std::string>("/remote/mocap/orin_ip_address", "10.42.0.101");
    // this->declare_parameter<std::string>("/remote/mocap/orin_ip_address", "172.16.37.1");
    // this->declare_parameter<uint16_t>("/remote/mocap/orin_port", 7012);

    this->declare_parameter<int>("/remote/mocap/frame_rate", 100);
    
    hub_port_ = this->get_parameter("/remote/mocap/hub_port").as_int();
    hub_ip_address_ = this->get_parameter("/remote/mocap/hub_ip_address").as_string();
    orin_port_ = this->get_parameter("/remote/mocap/orin_port").as_int();
    orin_ip_address_ = this->get_parameter("/remote/mocap/orin_ip_address").as_string();

    current_frame_rate_ = this->get_parameter("/remote/mocap/frame_rate").as_int();
    current_capture_mode_ = CaptureMode::AUTO;

    RCLCPP_INFO(this->get_logger(), "hub_port_ = %d", hub_port_);
    RCLCPP_INFO(this->get_logger(), "hub_ip_address_ = %s", hub_ip_address_.c_str());
    RCLCPP_INFO(this->get_logger(), "orin_port_ = %d", orin_port_);
    RCLCPP_INFO(this->get_logger(), "orin_ip_address_ = %s", orin_ip_address_.c_str());
    RCLCPP_INFO(this->get_logger(), "current_frame_rate_ = %d", current_frame_rate_);

    // 初始化数据发布器
    mocap_data_publisher_ = this->create_publisher<genie_msgs::msg::MocapData>("/remote/mocap_data", 10);
    mocap_network_publisher_ = this->create_publisher<genie_msgs::msg::MocapNetwork>("/remote/mocap_network", 10);
    // 初始化tf广播器
    tf_broadcaster_ = std::make_unique<tf2_ros::TransformBroadcaster>(*this);

    // 初始化服务
    calibrate_service_ = this->create_service<std_srvs::srv::Trigger>(
        "/remote/mocap/calibrate",
        std::bind(&NoitomStreamer::calibrate, this,
        std::placeholders::_1, std::placeholders::_2));
    zero_position_service_ = this->create_service<std_srvs::srv::Trigger>(
        "/remote/mocap/zero_position",
        std::bind(&NoitomStreamer::setZeroPosition, this,
        std::placeholders::_1, std::placeholders::_2));
    zero_posture_service_ = this->create_service<std_srvs::srv::Trigger>(
        "/remote/mocap/zero_posture",
        std::bind(&NoitomStreamer::setZeroPosture, this,
        std::placeholders::_1, std::placeholders::_2));
    init_noitom_service_ = this->create_service<std_srvs::srv::Trigger>(
        "/remote/init_mocap_remote_hal",
        std::bind(&NoitomStreamer::initNoitom, this,
        std::placeholders::_1, std::placeholders::_2));


    // 获取MocapApi接口指针
    void* rawPtr = nullptr;
    VERIFY(MCPGetGenericInterface(IMCPApplication_Version, &rawPtr));
    mcpApplication_ = static_cast<IMCPApplication*>(rawPtr);

    VERIFY(MCPGetGenericInterface(IMCPCommand_Version, &rawPtr));
    mcpCommand_ = static_cast<IMCPCommand*>(rawPtr);

    VERIFY(MCPGetGenericInterface(IMCPJoint_Version, &rawPtr));
    mcpJoint_ = static_cast<IMCPJoint*>(rawPtr);

    VERIFY(MCPGetGenericInterface(IMCPAvatar_Version, &rawPtr));
    mcpAvatar_ = static_cast<IMCPAvatar*>(rawPtr);

    VERIFY(MCPGetGenericInterface(IMCPSettings_Version, &rawPtr));
    mcpSettings_ = static_cast<IMCPSettings*>(rawPtr);

    VERIFY(MCPGetGenericInterface(IMCPCalibrateMotionProgress_Version, &rawPtr));
    mcpCalibrateMotionProgress_ = static_cast<IMCPCalibrateMotionProgress*>(rawPtr);

    VERIFY(MCPGetGenericInterface(IMCPRenderSettings_Version, &rawPtr));
    mcpRenderSettings_ = static_cast<IMCPRenderSettings*>(rawPtr);
    
    VERIFY(MCPGetGenericInterface(IMCPSystem_Version, &rawPtr));
    mcpSystem_ = static_cast<IMCPSystem*>(rawPtr);

    RCLCPP_DEBUG(this->get_logger(), "mcpApplication_ = %p", mcpApplication_);
    RCLCPP_DEBUG(this->get_logger(), "mcpCommand_ = %p", mcpCommand_);
    RCLCPP_DEBUG(this->get_logger(), "mcpJoint_ = %p", mcpJoint_);
    RCLCPP_DEBUG(this->get_logger(), "mcpAvatar_ = %p", mcpAvatar_);
    RCLCPP_DEBUG(this->get_logger(), "mcpSettings_ = %p", mcpSettings_);
    RCLCPP_DEBUG(this->get_logger(), "mcpRenderSettings_ = %p", mcpRenderSettings_);
    RCLCPP_DEBUG(this->get_logger(), "mcpSystem_ = %p", mcpSystem_);
    if (!mcpApplication_ || !mcpCommand_ || !mcpJoint_ || !mcpAvatar_ || !mcpSettings_ || !mcpRenderSettings_) {
        RCLCPP_ERROR(this->get_logger(), "无法初始化MocapApi接口");
        throw std::runtime_error("MocapApi接口初始化失败");
    }

    RCLCPP_INFO(this->get_logger(), "MocapApi接口初始化成功");

    // 创建定时器
    start_poll_.store(true);
    timer_ = this->create_wall_timer(
            std::chrono::milliseconds(1000 / current_frame_rate_),
            std::bind(&NoitomStreamer::pollEvents, this));
    RCLCPP_INFO(this->get_logger(), "timer初始化成功");

    // 初始化应用程序
    initApp();

    RCLCPP_INFO(this->get_logger(), "应用程序初始化成功");

    std::string version = getSoftwareVersion();
    RCLCPP_INFO(this->get_logger(), "软件版本: %s", version.c_str());

    // 启动数据流
    start();

    RCLCPP_INFO(this->get_logger(), "数据流启动成功");
    RCLCPP_INFO(this->get_logger(), "数据正在流入...");

}

NoitomStreamer::~NoitomStreamer() {

    stop();

    if (mcpApplication_) {
        // 关闭应用程序
        if (mcpApplicationHandle) {
            VERIFY(mcpApplication_->CloseApplication(mcpApplicationHandle));
            VERIFY(mcpApplication_->DestroyApplication(mcpApplicationHandle));
        }
    }

    RCLCPP_INFO(this->get_logger(), "NoitomStreamer已销毁");
}


void NoitomStreamer::initApp() {
    // 创建普通设置
    VERIFY(mcpSettings_->CreateSettings(&mcpSettingsHandle));
    // 设置UDP和BVH数据参数
    // Server 是noitom提供的hub的ip 10.42.0.202	8080
    VERIFY(mcpSettings_->SetSettingsUDPServer(hub_ip_address_.c_str(), hub_port_, mcpSettingsHandle));
    // Ex 是我们orin的控制板 10.42.0.101 8002
    VERIFY(mcpSettings_->SetSettingsUDPEx(orin_ip_address_.c_str(), orin_port_, mcpSettingsHandle));
    // VERIFY(mcpSettings_->SetSettingsUDP(orin_port_, mcpSettingsHandle));
    VERIFY(mcpSettings_->SetSettingsBvhData(BvhDataType_Binary, mcpSettingsHandle));
    VERIFY(mcpSettings_->SetSettingsBvhTransformation(BvhTransformation_Enable, mcpSettingsHandle));
    VERIFY(mcpSettings_->SetSettingsBvhRotation(BvhRotation_YXZ, mcpSettingsHandle));
    
    // 创建渲染设置
    VERIFY(mcpRenderSettings_->CreateRenderSettings(&mcpRenderSettingsHandle));
    // 添加坐标系统设置
    VERIFY(mcpRenderSettings_->SetUpVector(UpVector_ZAxis, 1, mcpRenderSettingsHandle));      // Z轴向上
    VERIFY(mcpRenderSettings_->SetFrontVector(FrontVector_ParityOdd, 1, mcpRenderSettingsHandle)); // 设置前向量奇偶性
    VERIFY(mcpRenderSettings_->SetCoordSystem(CoordSystem_RightHanded, mcpRenderSettingsHandle)); // 右手坐标系
    VERIFY(mcpRenderSettings_->SetRotatingDirection(RotatingDirection_CounterClockwise, mcpRenderSettingsHandle)); // 逆时针旋转
    VERIFY(mcpRenderSettings_->SetUnit(Uint_Meter, mcpRenderSettingsHandle));             // 使用米为单位

    // 初始化Mocap应用程序
    VERIFY(mcpApplication_->CreateApplication(&mcpApplicationHandle));
    // 把设置和渲染设置添加到应用程序
    VERIFY(mcpApplication_->SetApplicationSettings(mcpSettingsHandle, mcpApplicationHandle));
    VERIFY(mcpApplication_->SetApplicationRenderSettings(mcpRenderSettingsHandle, mcpApplicationHandle));
    
    // 销毁设置并打开应用程序
    VERIFY(mcpSettings_->DestroySettings(mcpSettingsHandle));
    VERIFY(mcpRenderSettings_->DestroyRenderSettings(mcpRenderSettingsHandle));
    VERIFY(mcpApplication_->OpenApplication(mcpApplicationHandle));
}

void NoitomStreamer::executeCommand(EMCPCommand commandType, const std::string& commandName) {
    EMCPError result = mcpCommand_->CreateCommand(commandType, &mcpCommandHandle);
    if (result == Error_None)
    {
        RCLCPP_INFO(this->get_logger(), "命令 %s 创建成功。", commandName.c_str());
        // 发送命令并监控返回状态
        VERIFY(mcpCommand_->SetCommandExtraLong(CommandExtraLong_DeviceRadio, 2483, mcpCommandHandle));
        // 记录发送的命令句柄和名称
        last_command_handle = mcpCommandHandle;
        last_command_name = commandName;


        // 发送命令
        EMCPError result = mcpApplication_->QueuedServerCommand(mcpCommandHandle, mcpApplicationHandle);
        if (result == Error_None)  // 如果命令发送成功
        {
            RCLCPP_INFO(this->get_logger(), "命令发送成功。");
        }
        else  // 否则打印失败信息
        {
            RCLCPP_ERROR(this->get_logger(), "发送命令失败: %d", result);
        }
    }
    else // 如果有错误，直接销毁命令
    {
        // 销毁命令以免内存泄漏
        mcpCommand_->DestroyCommand(mcpCommandHandle);
        RCLCPP_ERROR(this->get_logger(), "创建 %s 命令失败: %d", commandName.c_str(), result);
    }
}

void NoitomStreamer::start() {
    executeCommand(CommandStartCapture, "StartCapture");
}

void NoitomStreamer::stop() {
    executeCommand(CommandStopCapture, "StopCapture");
}

void NoitomStreamer::calibrate(
    const std::shared_ptr<std_srvs::srv::Trigger::Request> request,
    std::shared_ptr<std_srvs::srv::Trigger::Response> response)
{
    RCLCPP_INFO(this->get_logger(), "开始动作校准...");
    executeCommand(CommandCalibrateMotion, "CalibrateMotion");
    response->success = true;
    response->message = "开始校准动作捕捉系统";
}

void NoitomStreamer::setZeroPosition(
    const std::shared_ptr<std_srvs::srv::Trigger::Request> request,
    std::shared_ptr<std_srvs::srv::Trigger::Response> response)
{
    RCLCPP_INFO(this->get_logger(), "开始执行零位校准...");
    executeCommand(CommandZeroPosition, "ZeroPosition");
    response->success = true;
    response->message = "开始零位校准";
}

void NoitomStreamer::setZeroPosture(
    const std::shared_ptr<std_srvs::srv::Trigger::Request> request,
    std::shared_ptr<std_srvs::srv::Trigger::Response> response)
{
    RCLCPP_INFO(this->get_logger(), "开始恢复原始姿态...");
    executeCommand(CommandResumeOriginalPosture, "ResumeOriginalPosture");
    response->success = true;
    response->message = "开始恢复原始姿态";
}

void NoitomStreamer::initNoitom(
    const std::shared_ptr<std_srvs::srv::Trigger::Request> request,
    std::shared_ptr<std_srvs::srv::Trigger::Response> response)
{
    
    start_poll_.store(false);
    RCLCPP_INFO(this->get_logger(), "动捕系统通知关闭");
    RCLCPP_INFO(this->get_logger(), "等待初始化");
    response->success = true;
    response->message = "通知完成";
}

void NoitomStreamer::setFrameRate(int fps) {
    // TODO
    return;
}

void NoitomStreamer::setCaptureMode(CaptureMode mode) {
    // TODO
    return;
}

std::string NoitomStreamer::getSoftwareVersion() const {
    const char *version = MCPGetMocapApiVersionString();
    RCLCPP_INFO(this->get_logger(), "MocapApi Version: %s", version);
    return std::string(version);
}

std::string NoitomStreamer::getDeviceSN() const {
    // TODO
    return "";
}

std::string NoitomStreamer::getHardwareProductionDate() const {
    // TODO
    return "";
}


void NoitomStreamer::pollEvents() {
    try {
        if (!start_poll_.load()) {
            // 关闭应用程序
            if (mcpApplication_) {
                if (mcpApplicationHandle) {
                    VERIFY(mcpApplication_->CloseApplication(mcpApplicationHandle));
                    VERIFY(mcpApplication_->DestroyApplication(mcpApplicationHandle));
                }
            }
            initApp();
            start();
            RCLCPP_INFO(this->get_logger(), "动捕系统poll已重新开启");
            start_poll_.store(true);
            return;
        }
        std::vector<MCPEvent_t> vEvents;
        uint32_t unEvent = 0;

        RCLCPP_DEBUG(this->get_logger(), "开始轮询事件");

        VERIFY(mcpApplication_->PollApplicationNextEvent(nullptr, &unEvent, mcpApplicationHandle));
        RCLCPP_DEBUG(this->get_logger(), "初始轮询 事件数量: %u", unEvent);

        vEvents.resize(unEvent);
        std::for_each(vEvents.begin(), vEvents.end(), [](MCPEvent_t &ev) { ev.size = sizeof(MCPEvent_t); });

        auto mcpError = mcpApplication_->PollApplicationNextEvent(vEvents.data(), &unEvent, mcpApplicationHandle);
        RCLCPP_DEBUG(this->get_logger(), "PollApplicationNextEvent 返回: %d", mcpError);

        if (mcpError == Error_None)
        {
            RCLCPP_DEBUG(this->get_logger(), "成功获取 %u 个事件", unEvent);
            vEvents.resize(unEvent);
            std::for_each(vEvents.begin(), vEvents.end(), [this](const MCPEvent_t &ev) { this->handleEvent(ev); });
        }
        else if (mcpError != Error_MoreEvent)
        {
            RCLCPP_ERROR(this->get_logger(), "PollApplicationNextEvent 返回错误: %d", mcpError);
            throw std::runtime_error("无法获取下一个事件。");
        }

    } catch (const std::exception& e) {
        RCLCPP_ERROR(this->get_logger(), "在 pollEvents 中发生异常: %s", e.what());
        // 可以选择重置状态或执行其他恢复操作
    }
    RCLCPP_DEBUG(this->get_logger(), "pollEvents 完成");
}

void NoitomStreamer::handleEvent(const MCPEvent_t &ev) {
    // 根据事件类型进行不同处理
    switch (ev.eventType)
    {
    case MCPEvent_AvatarUpdated:  // 处理Avatar更新事件
        handleAvatarUpdated(ev.eventData.motionData);
        break;
    case MCPEvent_Error:  // 处理错误事件
        RCLCPP_ERROR(this->get_logger(), "事件处理错误 %d", ev.eventData.systemError.error);
        break;
    case MCPEvent_CommandReply:  // 处理命令回复事件
        handleCommandReply(ev.eventData.commandRespond);
        break;
    case MCPEvent_Notify:  // 处理通知事件
        handleNotify(ev.eventData.notifyData);
        break;
    default:  // 处理未定义的事件
        RCLCPP_WARN(this->get_logger(), "Unhandled event");
        break;
    }
}

void NoitomStreamer::handleAvatarUpdated(const MCPEvent_MotionData_t &motionData) {
    // 获取Avatar名称
    const char *szAvatarName = nullptr;
    VERIFY(mcpAvatar_->GetAvatarName(&szAvatarName, motionData.avatarHandle));
    // RCLCPP_INFO(this->get_logger(), "Avatar '%s' updated", szAvatarName);

    // 获取关节句柄
    std::vector<MCPJointHandle_t> vJointHandles;
    uint32_t unSizeOfJointHandle = 0;

    RCLCPP_DEBUG(this->get_logger(), "开始获取Avatar关节");

    VERIFY(mcpAvatar_->GetAvatarJoints(nullptr, &unSizeOfJointHandle, motionData.avatarHandle));
    RCLCPP_DEBUG(this->get_logger(), "Avatar关节数量: %u", unSizeOfJointHandle);

    vJointHandles.resize(unSizeOfJointHandle);

    auto mcpError = mcpAvatar_->GetAvatarJoints(vJointHandles.data(), &unSizeOfJointHandle, motionData.avatarHandle);
    RCLCPP_DEBUG(this->get_logger(), "GetAvatarJoints 返回: %d", mcpError);

    if (mcpError == Error_None)
    {
        vJointHandles.resize(unSizeOfJointHandle);
        
        // 发布动捕数据
        publishMocapData(vJointHandles);

        // rviz 显示
        displayMocapData(vJointHandles);
    }
    else
    {
        RCLCPP_ERROR(this->get_logger(), "GetAvatarJoints 返回错误: %d", mcpError);
        throw std::runtime_error("无法获取Avatar关节。");
    }
}

void NoitomStreamer::publishMocapData(const std::vector<MCPJointHandle_t>& jointHandles) {
    // 创建MocapData消息
    genie_msgs::msg::MocapData mocap_msg;
    
    // 设置消息头
    mocap_msg.header.stamp = this->now();
    mocap_msg.header.frame_id = "mocap_frame";
    
    // 设置状态（这里需要根据实际情况设置）
    mocap_msg.status = 0;  // 假设正常状态
    mocap_msg.err_code = 0;  // 假设无错误
    
    // 遍历所有关节
    for (const auto& jointHandle : jointHandles) {
        genie_msgs::msg::MocapJointState joint_state;
        
        // 获取关节名称
        const char *szJointName = nullptr;
        VERIFY(mcpJoint_->GetJointName(&szJointName, jointHandle));
        joint_state.name = std::string(szJointName);
        
        // 获取关节ID（如果有的话）
        joint_state.id = 0;  // 默认ID，根据需要修改
        
        // 设置状态和错误码
        joint_state.status = 0;  // 默认正常状态
        joint_state.err_code = 0;  // 默认无错误
        
        // 获取位置
        float px, py, pz;
        VERIFY(mcpJoint_->GetJointGlobalPosition(&px, &py, &pz, jointHandle));
        joint_state.position.x = px;
        joint_state.position.y = py;
        joint_state.position.z = pz;
        
        // 获取旋转（四元数）
        float qx, qy, qz, qw;
        VERIFY(mcpJoint_->GetJointGlobalRotation(&qx, &qy, &qz, &qw, jointHandle));
        joint_state.orientation.x = qx;
        joint_state.orientation.y = qy;
        joint_state.orientation.z = qz;
        joint_state.orientation.w = qw;
        
        // 将关节状态添加到消息中
        mocap_msg.mocap_joint_states.push_back(joint_state);
    }
    
    // 发布消息
    mocap_data_publisher_->publish(mocap_msg);
    
    RCLCPP_DEBUG(this->get_logger(), 
                "发布动捕数据: %lu 个关节",
                mocap_msg.mocap_joint_states.size());
}

void NoitomStreamer::displayMocapData(const std::vector<MCPJointHandle_t>& jointHandles) {
    const auto current_time = this->now();
    
    for (size_t i = 0; i < jointHandles.size(); ++i) {
        const auto& jointHandle = jointHandles[i];
        
        // 获取关节名称
        const char *szJointName = nullptr;
        VERIFY(mcpJoint_->GetJointName(&szJointName, jointHandle));
        
        // 创建TransformStamped消息
        geometry_msgs::msg::TransformStamped transform_stamped;
        transform_stamped.header.stamp = current_time;
        transform_stamped.header.frame_id = "map";  // 父坐标系
        transform_stamped.child_frame_id = szJointName;  // 子坐标系使用关节名称
        
        // 设置位置
        float px, py, pz;
        VERIFY(mcpJoint_->GetJointGlobalPosition(&px, &py, &pz, jointHandle));
        transform_stamped.transform.translation.x = px;
        transform_stamped.transform.translation.y = py;
        transform_stamped.transform.translation.z = pz;
        
        // 设置方向（四元数）
        float qx, qy, qz, qw;
        VERIFY(mcpJoint_->GetJointGlobalRotation(&qx, &qy, &qz, &qw, jointHandle));
        transform_stamped.transform.rotation.x = qx;
        transform_stamped.transform.rotation.y = qy;
        transform_stamped.transform.rotation.z = qz;
        transform_stamped.transform.rotation.w = qw;

        // 发布transform
        tf_broadcaster_->sendTransform(transform_stamped);
        
        RCLCPP_DEBUG(this->get_logger(), 
                   "发布TF: %s -> %s, 位置(%.3f, %.3f, %.3f), 旋转(%.3f, %.3f, %.3f, %.3f)", 
                   transform_stamped.header.frame_id.c_str(),
                   transform_stamped.child_frame_id.c_str(),
                   px, py, pz,
                   qx, qy, qz, qw);
    }
}

void NoitomStreamer::handleCommandReply(const MCPEvent_CommandRespond_t &commandReply) {

    if (commandReply._commandHandle != last_command_handle) {
        RCLCPP_ERROR(this->get_logger(), "命令句柄不匹配"); 
        return;
    }
    switch (commandReply._replay) {
    case MCPReplay_Response:
        // 几乎不会出现
        RCLCPP_INFO(this->get_logger(), "服务器已收到 '%s' 命令，即将执行", 
            last_command_name.c_str());
        break;
    case MCPReplay_Result:
        // 简单命令会进这里，直接给出result
        RCLCPP_INFO(this->get_logger(), "服务器已完成执行 '%s' 命令", 
            last_command_name.c_str());
        mcpCommand_->DestroyCommand(last_command_handle);
        break;
    case MCPReplay_Running:
        // 只有可能在calibrate的时候进 running
        RCLCPP_INFO(this->get_logger(), "服务器正在执行 '%s' 命令", 
            last_command_name.c_str());
        // 如果进这里，说明在calibrate，直接显示校准动作
        displayCalibratatingPostures();
        displayCalibratatingProgress();
        break;
    default:
        break;
    }

    return;
}

void NoitomStreamer::displayCalibratatingPostures() {
    uint32_t count = 0;

    VERIFY(mcpCommand_->GetCommandProgress(EMCPCommandProgress::CommandProgress_CalibrateMotion
                , reinterpret_cast<intptr_t>(&mcpCalibrateMotionProgressHandle)
                , last_command_handle));

    // 获取校准动作数量
    if (Error_None == mcpCalibrateMotionProgress_->GetCalibrateMotionProgressCountOfSupportPoses(
        &count, mcpCalibrateMotionProgressHandle)) {
        
        RCLCPP_INFO(this->get_logger(), "开始校准动作...");
        RCLCPP_INFO(this->get_logger(), "校准动作数量: %u", count);
        
        for (int i = 0; i < count; ++i) {
            std::string name;
            uint32_t len = 0;
            VERIFY(mcpCalibrateMotionProgress_->GetCalibrateMotionProgressNameOfSupportPose(
                nullptr, &len, i, mcpCalibrateMotionProgressHandle));
            name.resize(len);
            VERIFY(mcpCalibrateMotionProgress_->GetCalibrateMotionProgressNameOfSupportPose(
                name.data(), &len, i, mcpCalibrateMotionProgressHandle));
                
            RCLCPP_INFO(this->get_logger(), "需要校准姿势: %s", name.c_str());
        }
    }
    else {
        RCLCPP_WARN(this->get_logger(), "校准过程中未收到校准状态信息");
    }
}

void NoitomStreamer::displayCalibratatingProgress() {
    std::string pose;
    pose.resize(256);
    uint32_t step = 0, size = pose.size();
    
    VERIFY(mcpCalibrateMotionProgress_->GetCalibrateMotionProgressStepOfCurrentPose(
        &step, pose.data(), &size, mcpCalibrateMotionProgressHandle));
    pose.resize(size);

    switch (step) {
    case CalibrateMotionProgressStep_Prepare: {
        RCLCPP_INFO(this->get_logger(), "准备校准 %s 姿势!", pose.c_str());
        break;
    }
        
    case CalibrateMotionProgressStep_Countdown: {
        uint32_t countdown = 0;
        VERIFY(mcpCalibrateMotionProgress_->GetCalibrateMotionProgressCountdownOfPose(
            &countdown, pose.data(), mcpCalibrateMotionProgressHandle));
        RCLCPP_INFO(this->get_logger(), "校准 %s 姿势倒计时: %d!", pose.c_str(), countdown);
        break;
    }
        
    case CalibrateMotionProgressStep_Progress: {
        uint32_t progress = 0;
        VERIFY(mcpCalibrateMotionProgress_->GetCalibrateMotionProgressProgressOfPose(
            &progress, pose.data(), mcpCalibrateMotionProgressHandle));
        RCLCPP_INFO(this->get_logger(), "校准 %s 姿势进度: %d%%", pose.c_str(), progress);
        break;
    }
        
    default: {
        RCLCPP_WARN(this->get_logger(), "未知的校准步骤状态");
        break;
    }
    }
}

void NoitomStreamer::handleNotify(const MCPEvent_NotifyData_t &notify) {

    switch (notify._notify) {
    case MocapApi::Notify_SystemUpdated: {
        handleSystemUpdated(static_cast<MocapApi::MCPSystemHandle_t>(notify._notifyHandle));
        break;
    }
    default: {
        RCLCPP_WARN(this->get_logger(), "未知的通知类型");
        break;
    }
    }
}

void NoitomStreamer::handleSystemUpdated(
    const MocapApi::MCPSystemHandle_t systemHandle_) {
    const char* pVersion = nullptr;
    VERIFY(mcpSystem_->GetMasterVersion(&pVersion, systemHandle_));
    const char* pSerialNumber = nullptr;
    VERIFY(mcpSystem_->GetMasterSerialNumber(&pSerialNumber, systemHandle_));

    RCLCPP_INFO(this->get_logger(), "MasterInfo : \r\n\tVersion: %s\r\n\tSerialNumber : %s", 
                pVersion, pSerialNumber);
}


int main(int argc, char * argv[])
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<NoitomStreamer>(rclcpp::NodeOptions()));
    rclcpp::shutdown();

    return 0;
}
