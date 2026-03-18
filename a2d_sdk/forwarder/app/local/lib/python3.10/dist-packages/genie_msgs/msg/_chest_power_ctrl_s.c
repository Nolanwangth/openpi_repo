// generated from rosidl_generator_py/resource/_idl_support.c.em
// with input from genie_msgs:msg/ChestPowerCtrl.idl
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
#include "genie_msgs/msg/detail/chest_power_ctrl__struct.h"
#include "genie_msgs/msg/detail/chest_power_ctrl__functions.h"

ROSIDL_GENERATOR_C_IMPORT
bool std_msgs__msg__header__convert_from_py(PyObject * _pymsg, void * _ros_message);
ROSIDL_GENERATOR_C_IMPORT
PyObject * std_msgs__msg__header__convert_to_py(void * raw_ros_message);

ROSIDL_GENERATOR_C_EXPORT
bool genie_msgs__msg__chest_power_ctrl__convert_from_py(PyObject * _pymsg, void * _ros_message)
{
  // check that the passed message is of the expected Python class
  {
    char full_classname_dest[48];
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
    assert(strncmp("genie_msgs.msg._chest_power_ctrl.ChestPowerCtrl", full_classname_dest, 47) == 0);
  }
  genie_msgs__msg__ChestPowerCtrl * ros_message = _ros_message;
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
  {  // chest_power_board_power_ctrl_req
    PyObject * field = PyObject_GetAttrString(_pymsg, "chest_power_board_power_ctrl_req");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->chest_power_board_power_ctrl_req = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // head_interactive_board_power_ctrl_req
    PyObject * field = PyObject_GetAttrString(_pymsg, "head_interactive_board_power_ctrl_req");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->head_interactive_board_power_ctrl_req = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // curved_screen_power_ctrl_req
    PyObject * field = PyObject_GetAttrString(_pymsg, "curved_screen_power_ctrl_req");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->curved_screen_power_ctrl_req = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // head_yaw_motor_power_ctrl_req
    PyObject * field = PyObject_GetAttrString(_pymsg, "head_yaw_motor_power_ctrl_req");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->head_yaw_motor_power_ctrl_req = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // head_pitch_motor_power_ctrl_req
    PyObject * field = PyObject_GetAttrString(_pymsg, "head_pitch_motor_power_ctrl_req");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->head_pitch_motor_power_ctrl_req = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // waist_yaw_motor_power_ctrl_req
    PyObject * field = PyObject_GetAttrString(_pymsg, "waist_yaw_motor_power_ctrl_req");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->waist_yaw_motor_power_ctrl_req = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // waist_pitch_motor_power_ctrl_req
    PyObject * field = PyObject_GetAttrString(_pymsg, "waist_pitch_motor_power_ctrl_req");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->waist_pitch_motor_power_ctrl_req = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // leg_bending1_motor_power_ctrl_req
    PyObject * field = PyObject_GetAttrString(_pymsg, "leg_bending1_motor_power_ctrl_req");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->leg_bending1_motor_power_ctrl_req = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // leg_bending2_motor_power_ctrl_req
    PyObject * field = PyObject_GetAttrString(_pymsg, "leg_bending2_motor_power_ctrl_req");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->leg_bending2_motor_power_ctrl_req = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // leg_bending3_motor_power_ctrl_req
    PyObject * field = PyObject_GetAttrString(_pymsg, "leg_bending3_motor_power_ctrl_req");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->leg_bending3_motor_power_ctrl_req = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // left_arm_power_ctrl_req
    PyObject * field = PyObject_GetAttrString(_pymsg, "left_arm_power_ctrl_req");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->left_arm_power_ctrl_req = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // right_arm_power_ctrl_req
    PyObject * field = PyObject_GetAttrString(_pymsg, "right_arm_power_ctrl_req");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->right_arm_power_ctrl_req = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // chest_light_strip_power_ctrl_req
    PyObject * field = PyObject_GetAttrString(_pymsg, "chest_light_strip_power_ctrl_req");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->chest_light_strip_power_ctrl_req = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // fan_power_ctrl_req
    PyObject * field = PyObject_GetAttrString(_pymsg, "fan_power_ctrl_req");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->fan_power_ctrl_req = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // mocap_poe_power_ctrl_req
    PyObject * field = PyObject_GetAttrString(_pymsg, "mocap_poe_power_ctrl_req");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->mocap_poe_power_ctrl_req = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // ipad_power_ctrl_req
    PyObject * field = PyObject_GetAttrString(_pymsg, "ipad_power_ctrl_req");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->ipad_power_ctrl_req = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // chest_reserved_lidar_power_ctrl_req
    PyObject * field = PyObject_GetAttrString(_pymsg, "chest_reserved_lidar_power_ctrl_req");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->chest_reserved_lidar_power_ctrl_req = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }

  return true;
}

ROSIDL_GENERATOR_C_EXPORT
PyObject * genie_msgs__msg__chest_power_ctrl__convert_to_py(void * raw_ros_message)
{
  /* NOTE(esteve): Call constructor of ChestPowerCtrl */
  PyObject * _pymessage = NULL;
  {
    PyObject * pymessage_module = PyImport_ImportModule("genie_msgs.msg._chest_power_ctrl");
    assert(pymessage_module);
    PyObject * pymessage_class = PyObject_GetAttrString(pymessage_module, "ChestPowerCtrl");
    assert(pymessage_class);
    Py_DECREF(pymessage_module);
    _pymessage = PyObject_CallObject(pymessage_class, NULL);
    Py_DECREF(pymessage_class);
    if (!_pymessage) {
      return NULL;
    }
  }
  genie_msgs__msg__ChestPowerCtrl * ros_message = (genie_msgs__msg__ChestPowerCtrl *)raw_ros_message;
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
  {  // chest_power_board_power_ctrl_req
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->chest_power_board_power_ctrl_req);
    {
      int rc = PyObject_SetAttrString(_pymessage, "chest_power_board_power_ctrl_req", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // head_interactive_board_power_ctrl_req
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->head_interactive_board_power_ctrl_req);
    {
      int rc = PyObject_SetAttrString(_pymessage, "head_interactive_board_power_ctrl_req", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // curved_screen_power_ctrl_req
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->curved_screen_power_ctrl_req);
    {
      int rc = PyObject_SetAttrString(_pymessage, "curved_screen_power_ctrl_req", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // head_yaw_motor_power_ctrl_req
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->head_yaw_motor_power_ctrl_req);
    {
      int rc = PyObject_SetAttrString(_pymessage, "head_yaw_motor_power_ctrl_req", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // head_pitch_motor_power_ctrl_req
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->head_pitch_motor_power_ctrl_req);
    {
      int rc = PyObject_SetAttrString(_pymessage, "head_pitch_motor_power_ctrl_req", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // waist_yaw_motor_power_ctrl_req
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->waist_yaw_motor_power_ctrl_req);
    {
      int rc = PyObject_SetAttrString(_pymessage, "waist_yaw_motor_power_ctrl_req", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // waist_pitch_motor_power_ctrl_req
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->waist_pitch_motor_power_ctrl_req);
    {
      int rc = PyObject_SetAttrString(_pymessage, "waist_pitch_motor_power_ctrl_req", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // leg_bending1_motor_power_ctrl_req
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->leg_bending1_motor_power_ctrl_req);
    {
      int rc = PyObject_SetAttrString(_pymessage, "leg_bending1_motor_power_ctrl_req", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // leg_bending2_motor_power_ctrl_req
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->leg_bending2_motor_power_ctrl_req);
    {
      int rc = PyObject_SetAttrString(_pymessage, "leg_bending2_motor_power_ctrl_req", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // leg_bending3_motor_power_ctrl_req
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->leg_bending3_motor_power_ctrl_req);
    {
      int rc = PyObject_SetAttrString(_pymessage, "leg_bending3_motor_power_ctrl_req", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // left_arm_power_ctrl_req
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->left_arm_power_ctrl_req);
    {
      int rc = PyObject_SetAttrString(_pymessage, "left_arm_power_ctrl_req", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // right_arm_power_ctrl_req
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->right_arm_power_ctrl_req);
    {
      int rc = PyObject_SetAttrString(_pymessage, "right_arm_power_ctrl_req", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // chest_light_strip_power_ctrl_req
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->chest_light_strip_power_ctrl_req);
    {
      int rc = PyObject_SetAttrString(_pymessage, "chest_light_strip_power_ctrl_req", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // fan_power_ctrl_req
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->fan_power_ctrl_req);
    {
      int rc = PyObject_SetAttrString(_pymessage, "fan_power_ctrl_req", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // mocap_poe_power_ctrl_req
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->mocap_poe_power_ctrl_req);
    {
      int rc = PyObject_SetAttrString(_pymessage, "mocap_poe_power_ctrl_req", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // ipad_power_ctrl_req
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->ipad_power_ctrl_req);
    {
      int rc = PyObject_SetAttrString(_pymessage, "ipad_power_ctrl_req", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // chest_reserved_lidar_power_ctrl_req
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->chest_reserved_lidar_power_ctrl_req);
    {
      int rc = PyObject_SetAttrString(_pymessage, "chest_reserved_lidar_power_ctrl_req", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }

  // ownership of _pymessage is transferred to the caller
  return _pymessage;
}
