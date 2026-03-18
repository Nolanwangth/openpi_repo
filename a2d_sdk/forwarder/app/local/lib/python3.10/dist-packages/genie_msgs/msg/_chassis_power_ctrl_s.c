// generated from rosidl_generator_py/resource/_idl_support.c.em
// with input from genie_msgs:msg/ChassisPowerCtrl.idl
// generated code does not contain a copyright notice
#define NPY_NO_DEPRECATED_API NPY_1_7_API_VERSION
#include <Python.h>
#include <stdbool.h>
#ifndef _WIN32
# pragma GCC diagnostic push
# pragma GCC diagnostic ignored "-Wunused-function"
#endif
#include "numpy/ndarrayobject.h"
#ifndef _WIN32
# pragma GCC diagnostic pop
#endif
#include "rosidl_runtime_c/visibility_control.h"
#include "genie_msgs/msg/detail/chassis_power_ctrl__struct.h"
#include "genie_msgs/msg/detail/chassis_power_ctrl__functions.h"

ROSIDL_GENERATOR_C_IMPORT
bool std_msgs__msg__header__convert_from_py(PyObject * _pymsg, void * _ros_message);
ROSIDL_GENERATOR_C_IMPORT
PyObject * std_msgs__msg__header__convert_to_py(void * raw_ros_message);

ROSIDL_GENERATOR_C_EXPORT
bool genie_msgs__msg__chassis_power_ctrl__convert_from_py(PyObject * _pymsg, void * _ros_message)
{
  // check that the passed message is of the expected Python class
  {
    char full_classname_dest[52];
    {
      char * class_name = NULL;
      char * module_name = NULL;
      {
        PyObject * class_attr = PyObject_GetAttrString(_pymsg, "__class__");
        if (class_attr) {
          PyObject * name_attr = PyObject_GetAttrString(class_attr, "__name__");
          if (name_attr) {
            class_name = (char *)PyUnicode_1BYTE_DATA(name_attr);
            Py_DECREF(name_attr);
          }
          PyObject * module_attr = PyObject_GetAttrString(class_attr, "__module__");
          if (module_attr) {
            module_name = (char *)PyUnicode_1BYTE_DATA(module_attr);
            Py_DECREF(module_attr);
          }
          Py_DECREF(class_attr);
        }
      }
      if (!class_name || !module_name) {
        return false;
      }
      snprintf(full_classname_dest, sizeof(full_classname_dest), "%s.%s", module_name, class_name);
    }
    assert(strncmp("genie_msgs.msg._chassis_power_ctrl.ChassisPowerCtrl", full_classname_dest, 51) == 0);
  }
  genie_msgs__msg__ChassisPowerCtrl * ros_message = _ros_message;
  {  // header
    PyObject * field = PyObject_GetAttrString(_pymsg, "header");
    if (!field) {
      return false;
    }
    if (!std_msgs__msg__header__convert_from_py(field, &ros_message->header)) {
      Py_DECREF(field);
      return false;
    }
    Py_DECREF(field);
  }
  {  // chassis_power_board_power_ctrlreq
    PyObject * field = PyObject_GetAttrString(_pymsg, "chassis_power_board_power_ctrlreq");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->chassis_power_board_power_ctrlreq = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // chassis_left_traction_motor_power_ctrl_req
    PyObject * field = PyObject_GetAttrString(_pymsg, "chassis_left_traction_motor_power_ctrl_req");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->chassis_left_traction_motor_power_ctrl_req = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // chassis_righttraction_motor_power_ctrl_req
    PyObject * field = PyObject_GetAttrString(_pymsg, "chassis_righttraction_motor_power_ctrl_req");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->chassis_righttraction_motor_power_ctrl_req = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // chassis_left_steering_motor_power_ctrl_req
    PyObject * field = PyObject_GetAttrString(_pymsg, "chassis_left_steering_motor_power_ctrl_req");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->chassis_left_steering_motor_power_ctrl_req = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // chassis_right_steering_motor_power_ctrl_req
    PyObject * field = PyObject_GetAttrString(_pymsg, "chassis_right_steering_motor_power_ctrl_req");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->chassis_right_steering_motor_power_ctrl_req = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // chassis_lidar1_power_ctrl_req
    PyObject * field = PyObject_GetAttrString(_pymsg, "chassis_lidar1_power_ctrl_req");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->chassis_lidar1_power_ctrl_req = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // chassis_lidar2_power_ctrl_req
    PyObject * field = PyObject_GetAttrString(_pymsg, "chassis_lidar2_power_ctrl_req");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->chassis_lidar2_power_ctrl_req = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // chassis_ultrasonic_radar_power_ctrl_req
    PyObject * field = PyObject_GetAttrString(_pymsg, "chassis_ultrasonic_radar_power_ctrl_req");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->chassis_ultrasonic_radar_power_ctrl_req = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // chassis_tof_camera_power_ctrl_req
    PyObject * field = PyObject_GetAttrString(_pymsg, "chassis_tof_camera_power_ctrl_req");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->chassis_tof_camera_power_ctrl_req = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // chassis_ethernet_switch_power_ctrl_req
    PyObject * field = PyObject_GetAttrString(_pymsg, "chassis_ethernet_switch_power_ctrl_req");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->chassis_ethernet_switch_power_ctrl_req = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // chassis_output_power_ctrl_req
    PyObject * field = PyObject_GetAttrString(_pymsg, "chassis_output_power_ctrl_req");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->chassis_output_power_ctrl_req = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // charging_plug_power_ctrl_req
    PyObject * field = PyObject_GetAttrString(_pymsg, "charging_plug_power_ctrl_req");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->charging_plug_power_ctrl_req = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // battery_power_switch_power_ctrl_req
    PyObject * field = PyObject_GetAttrString(_pymsg, "battery_power_switch_power_ctrl_req");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->battery_power_switch_power_ctrl_req = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // battery1_bms_switch_power_ctrl_req
    PyObject * field = PyObject_GetAttrString(_pymsg, "battery1_bms_switch_power_ctrl_req");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->battery1_bms_switch_power_ctrl_req = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // battery2_bms_switch_power_ctrl_req
    PyObject * field = PyObject_GetAttrString(_pymsg, "battery2_bms_switch_power_ctrl_req");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->battery2_bms_switch_power_ctrl_req = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // battery1_unlock_ctrl_req
    PyObject * field = PyObject_GetAttrString(_pymsg, "battery1_unlock_ctrl_req");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->battery1_unlock_ctrl_req = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // battery2_unlock_ctrl_req
    PyObject * field = PyObject_GetAttrString(_pymsg, "battery2_unlock_ctrl_req");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->battery2_unlock_ctrl_req = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // charger_max_charging_current_ctrl_req
    PyObject * field = PyObject_GetAttrString(_pymsg, "charger_max_charging_current_ctrl_req");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->charger_max_charging_current_ctrl_req = (float)PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // charger_max_charging_voltage_ctrl_req
    PyObject * field = PyObject_GetAttrString(_pymsg, "charger_max_charging_voltage_ctrl_req");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->charger_max_charging_voltage_ctrl_req = (float)PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }

  return true;
}

ROSIDL_GENERATOR_C_EXPORT
PyObject * genie_msgs__msg__chassis_power_ctrl__convert_to_py(void * raw_ros_message)
{
  /* NOTE(esteve): Call constructor of ChassisPowerCtrl */
  PyObject * _pymessage = NULL;
  {
    PyObject * pymessage_module = PyImport_ImportModule("genie_msgs.msg._chassis_power_ctrl");
    assert(pymessage_module);
    PyObject * pymessage_class = PyObject_GetAttrString(pymessage_module, "ChassisPowerCtrl");
    assert(pymessage_class);
    Py_DECREF(pymessage_module);
    _pymessage = PyObject_CallObject(pymessage_class, NULL);
    Py_DECREF(pymessage_class);
    if (!_pymessage) {
      return NULL;
    }
  }
  genie_msgs__msg__ChassisPowerCtrl * ros_message = (genie_msgs__msg__ChassisPowerCtrl *)raw_ros_message;
  {  // header
    PyObject * field = NULL;
    field = std_msgs__msg__header__convert_to_py(&ros_message->header);
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "header", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // chassis_power_board_power_ctrlreq
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->chassis_power_board_power_ctrlreq);
    {
      int rc = PyObject_SetAttrString(_pymessage, "chassis_power_board_power_ctrlreq", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // chassis_left_traction_motor_power_ctrl_req
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->chassis_left_traction_motor_power_ctrl_req);
    {
      int rc = PyObject_SetAttrString(_pymessage, "chassis_left_traction_motor_power_ctrl_req", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // chassis_righttraction_motor_power_ctrl_req
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->chassis_righttraction_motor_power_ctrl_req);
    {
      int rc = PyObject_SetAttrString(_pymessage, "chassis_righttraction_motor_power_ctrl_req", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // chassis_left_steering_motor_power_ctrl_req
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->chassis_left_steering_motor_power_ctrl_req);
    {
      int rc = PyObject_SetAttrString(_pymessage, "chassis_left_steering_motor_power_ctrl_req", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // chassis_right_steering_motor_power_ctrl_req
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->chassis_right_steering_motor_power_ctrl_req);
    {
      int rc = PyObject_SetAttrString(_pymessage, "chassis_right_steering_motor_power_ctrl_req", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // chassis_lidar1_power_ctrl_req
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->chassis_lidar1_power_ctrl_req);
    {
      int rc = PyObject_SetAttrString(_pymessage, "chassis_lidar1_power_ctrl_req", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // chassis_lidar2_power_ctrl_req
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->chassis_lidar2_power_ctrl_req);
    {
      int rc = PyObject_SetAttrString(_pymessage, "chassis_lidar2_power_ctrl_req", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // chassis_ultrasonic_radar_power_ctrl_req
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->chassis_ultrasonic_radar_power_ctrl_req);
    {
      int rc = PyObject_SetAttrString(_pymessage, "chassis_ultrasonic_radar_power_ctrl_req", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // chassis_tof_camera_power_ctrl_req
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->chassis_tof_camera_power_ctrl_req);
    {
      int rc = PyObject_SetAttrString(_pymessage, "chassis_tof_camera_power_ctrl_req", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // chassis_ethernet_switch_power_ctrl_req
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->chassis_ethernet_switch_power_ctrl_req);
    {
      int rc = PyObject_SetAttrString(_pymessage, "chassis_ethernet_switch_power_ctrl_req", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // chassis_output_power_ctrl_req
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->chassis_output_power_ctrl_req);
    {
      int rc = PyObject_SetAttrString(_pymessage, "chassis_output_power_ctrl_req", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // charging_plug_power_ctrl_req
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->charging_plug_power_ctrl_req);
    {
      int rc = PyObject_SetAttrString(_pymessage, "charging_plug_power_ctrl_req", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // battery_power_switch_power_ctrl_req
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->battery_power_switch_power_ctrl_req);
    {
      int rc = PyObject_SetAttrString(_pymessage, "battery_power_switch_power_ctrl_req", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // battery1_bms_switch_power_ctrl_req
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->battery1_bms_switch_power_ctrl_req);
    {
      int rc = PyObject_SetAttrString(_pymessage, "battery1_bms_switch_power_ctrl_req", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // battery2_bms_switch_power_ctrl_req
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->battery2_bms_switch_power_ctrl_req);
    {
      int rc = PyObject_SetAttrString(_pymessage, "battery2_bms_switch_power_ctrl_req", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // battery1_unlock_ctrl_req
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->battery1_unlock_ctrl_req);
    {
      int rc = PyObject_SetAttrString(_pymessage, "battery1_unlock_ctrl_req", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // battery2_unlock_ctrl_req
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->battery2_unlock_ctrl_req);
    {
      int rc = PyObject_SetAttrString(_pymessage, "battery2_unlock_ctrl_req", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // charger_max_charging_current_ctrl_req
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->charger_max_charging_current_ctrl_req);
    {
      int rc = PyObject_SetAttrString(_pymessage, "charger_max_charging_current_ctrl_req", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // charger_max_charging_voltage_ctrl_req
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->charger_max_charging_voltage_ctrl_req);
    {
      int rc = PyObject_SetAttrString(_pymessage, "charger_max_charging_voltage_ctrl_req", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }

  // ownership of _pymessage is transferred to the caller
  return _pymessage;
}
