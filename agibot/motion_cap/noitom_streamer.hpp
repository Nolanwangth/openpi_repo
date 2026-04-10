#pragma once
#include <rclcpp/rclcpp.hpp>
#include <memory>
#include <string>
#include <array>
#include <vector>
#include <chrono>  // 引入时间相关库，用于控制延时
#include <thread>  // 引入线程库
#include <algorithm>  // 引入算法库
#include <iostream>  // 引入标准输入输出库
#include "MocapApi.h"
#include <std_srvs/srv/trigger.hpp>
#include "genie_msgs/msg/mocap_data.hpp"
#include "genie_msgs/msg/mocap_network.hpp"
#include <tf2_ros/transform_broadcaster.h>
#include <geometry_msgs/msg/transform_stamped.hpp>


// 宏定义，用于验证API的返回值并进行错误处理
#define VERIFY(r)                                                        \
    if (auto r_ = (r); r_ != MocapApi::Error_None)                       \
    {                                                                    \
        RCLCPP_ERROR(this->get_logger(), "操作 '%s' 返回错误: %d", #r, r_); \
    }

using namespace MocapApi;

class NoitomStreamer : public rclcpp::Node {
public:
    NoitomStreamer(const rclcpp::NodeOptions & options);
    ~NoitomStreamer();

private:
    // 捕捉模式枚举，暂时没有用到
    enum class CaptureMode {
        AUTO,
        UPPER_BODY,
        FULL_BODY,
        LEFT_ARM,
        RIGHT_ARM
    };

    // 关节数据结构体
    struct JointData {
        int64_t timestamp{0};        
        bool isActive{false};        
        int errorCode{0};            
        float position[3]{0};        
        float orientation[4]{0};     
    };


    // 会在节点初始化之后自动调用
    void initApp();
    // 通用命令执行函数，输入命令就能执行并处理错误
    void executeCommand(EMCPCommand commandType, const std::string& commandName);
    
    // 会在节点初始化之后自动调用
    void start();
    void stop();
    void setFrameRate(int fps); // TODO
    // 添加服务回调函数声明
    void calibrate(
        const std::shared_ptr<std_srvs::srv::Trigger::Request> request,
        std::shared_ptr<std_srvs::srv::Trigger::Response> response);
    void setZeroPosition(
        const std::shared_ptr<std_srvs::srv::Trigger::Request> request,
        std::shared_ptr<std_srvs::srv::Trigger::Response> response);
    void setZeroPosture(
        const std::shared_ptr<std_srvs::srv::Trigger::Request> request,
        std::shared_ptr<std_srvs::srv::Trigger::Response> response);
    void initNoitom(
        const std::shared_ptr<std_srvs::srv::Trigger::Request> request,
        std::shared_ptr<std_srvs::srv::Trigger::Response> response);
    std::atomic<bool> start_poll_{false};

    void setCaptureMode(CaptureMode mode); // TODO
    std::string getSoftwareVersion() const; 
    std::string getDeviceSN() const; // TODO
    std::string getHardwareProductionDate() const; // TODO

    // ROS定时器调用的主循环，轮询 handleEvent，处理三种事件
    void pollEvents();
    void handleEvent(const MCPEvent_t &ev);
    // 三种事件分别调用三种handle函数
    // 1. 运动数据更新，会publish
    void handleAvatarUpdated(const MCPEvent_MotionData_t &motionData);
    void publishMocapData(const std::vector<MCPJointHandle_t>& jointHandles);
    void displayMocapData(const std::vector<MCPJointHandle_t>& jointHandles);
    // 2. 命令回复，大多数情况会给出result，calibrate会给出progress
    void handleCommandReply(const MCPEvent_CommandRespond_t &commandReply);
    void displayCalibratatingPostures();
    void displayCalibratatingProgress();
    // 3. 通知，目前没有用到，可以忽略
    void handleNotify(const MCPEvent_NotifyData_t &notify);
    void handleSystemUpdated(const MocapApi::MCPSystemHandle_t systemHandle_);
    
    // 储存参数
    std::string hub_ip_address_;
    unsigned short hub_port_;
    std::string orin_ip_address_;
    unsigned short orin_port_;
    CaptureMode current_capture_mode_;
    int current_frame_rate_;
    std::array<JointData, 59> motion_capture_data_;  // joint 59, sensor 27

    // 消息发布器
    rclcpp::Publisher<genie_msgs::msg::MocapData>::SharedPtr mocap_data_publisher_;
    rclcpp::Publisher<genie_msgs::msg::MocapNetwork>::SharedPtr mocap_network_publisher_;
    std::unique_ptr<tf2_ros::TransformBroadcaster> tf_broadcaster_;
    // 主轮询定时器
    rclcpp::TimerBase::SharedPtr timer_;
    // hmi服务声明
    rclcpp::Service<std_srvs::srv::Trigger>::SharedPtr calibrate_service_;
    rclcpp::Service<std_srvs::srv::Trigger>::SharedPtr zero_position_service_;
    rclcpp::Service<std_srvs::srv::Trigger>::SharedPtr zero_posture_service_;
    rclcpp::Service<std_srvs::srv::Trigger>::SharedPtr init_noitom_service_;
    
    // mocap api 句柄
    MCPApplicationHandle_t mcpApplicationHandle = 0;
    MCPSettingsHandle_t mcpSettingsHandle = 0;
    MCPRenderSettingsHandle_t mcpRenderSettingsHandle = 0;
    MCPCommandHandle_t mcpCommandHandle = 0;
    MCPCalibrateMotionProgressHandle_t mcpCalibrateMotionProgressHandle = 0;
    MCPCommandHandle_t last_command_handle = 0;
    std::string last_command_name = "";

    // mocap api 接口
    IMCPCommand* mcpCommand_ = nullptr;
    IMCPApplication* mcpApplication_ = nullptr;
    IMCPJoint* mcpJoint_ = nullptr;
    IMCPAvatar* mcpAvatar_ = nullptr;
    IMCPSettings* mcpSettings_ = nullptr;
    IMCPCalibrateMotionProgress* mcpCalibrateMotionProgress_ = nullptr;
    IMCPRenderSettings* mcpRenderSettings_ = nullptr;
    IMCPSystem* mcpSystem_ = nullptr;
};
