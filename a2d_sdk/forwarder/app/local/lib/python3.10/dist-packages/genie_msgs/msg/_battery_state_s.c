// generated from rosidl_generator_py/resource/_idl_support.c.em
// with input from genie_msgs:msg/BatteryState.idl
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
#include "genie_msgs/msg/detail/battery_state__struct.h"
#include "genie_msgs/msg/detail/battery_state__functions.h"

#include "rosidl_runtime_c/string.h"
#include "rosidl_runtime_c/string_functions.h"

ROSIDL_GENERATOR_C_IMPORT
bool std_msgs__msg__header__convert_from_py(PyObject * _pymsg, void * _ros_message);
ROSIDL_GENERATOR_C_IMPORT
PyObject * std_msgs__msg__header__convert_to_py(void * raw_ros_message);

ROSIDL_GENERATOR_C_EXPORT
bool genie_msgs__msg__battery_state__convert_from_py(PyObject * _pymsg, void * _ros_message)
{
  // check that the passed message is of the expected Python class
  {
    char full_classname_dest[43];
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
    assert(strncmp("genie_msgs.msg._battery_state.BatteryState", full_classname_dest, 42) == 0);
  }
  genie_msgs__msg__BatteryState * ros_message = _ros_message;
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
  {  // battery1_bms_charge_or_discharge
    PyObject * field = PyObject_GetAttrString(_pymsg, "battery1_bms_charge_or_discharge");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->battery1_bms_charge_or_discharge = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // battery2_bms_charge_or_discharge
    PyObject * field = PyObject_GetAttrString(_pymsg, "battery2_bms_charge_or_discharge");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->battery2_bms_charge_or_discharge = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // battery1_bms_output_voltage
    PyObject * field = PyObject_GetAttrString(_pymsg, "battery1_bms_output_voltage");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->battery1_bms_output_voltage = (float)PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // battery2_bms_output_voltage
    PyObject * field = PyObject_GetAttrString(_pymsg, "battery2_bms_output_voltage");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->battery2_bms_output_voltage = (float)PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // battery1_bms_output_current
    PyObject * field = PyObject_GetAttrString(_pymsg, "battery1_bms_output_current");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->battery1_bms_output_current = (float)PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // battery2_bms_output_current
    PyObject * field = PyObject_GetAttrString(_pymsg, "battery2_bms_output_current");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->battery2_bms_output_current = (float)PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // battery1_bms_charge_current
    PyObject * field = PyObject_GetAttrString(_pymsg, "battery1_bms_charge_current");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->battery1_bms_charge_current = (float)PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // battery2_bms_charge_current
    PyObject * field = PyObject_GetAttrString(_pymsg, "battery2_bms_charge_current");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->battery2_bms_charge_current = (float)PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // battery1_bms_temperature
    PyObject * field = PyObject_GetAttrString(_pymsg, "battery1_bms_temperature");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->battery1_bms_temperature = (float)PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // battery2_bms_temperature
    PyObject * field = PyObject_GetAttrString(_pymsg, "battery2_bms_temperature");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->battery2_bms_temperature = (float)PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // battery1_bms_soc
    PyObject * field = PyObject_GetAttrString(_pymsg, "battery1_bms_soc");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->battery1_bms_soc = (float)PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // battery2_bms_soc
    PyObject * field = PyObject_GetAttrString(_pymsg, "battery2_bms_soc");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->battery2_bms_soc = (float)PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // battery1_bms_soh
    PyObject * field = PyObject_GetAttrString(_pymsg, "battery1_bms_soh");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->battery1_bms_soh = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // battery2_bms_soh
    PyObject * field = PyObject_GetAttrString(_pymsg, "battery2_bms_soh");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->battery2_bms_soh = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // battery1_bms_short_circuit_fault_state
    PyObject * field = PyObject_GetAttrString(_pymsg, "battery1_bms_short_circuit_fault_state");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->battery1_bms_short_circuit_fault_state = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // battery2_bms_short_circuit_fault_state
    PyObject * field = PyObject_GetAttrString(_pymsg, "battery2_bms_short_circuit_fault_state");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->battery2_bms_short_circuit_fault_state = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // battery1_bms_open_circuit_fault_state
    PyObject * field = PyObject_GetAttrString(_pymsg, "battery1_bms_open_circuit_fault_state");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->battery1_bms_open_circuit_fault_state = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // battery2_bms_open_circuit_fault_state
    PyObject * field = PyObject_GetAttrString(_pymsg, "battery2_bms_open_circuit_fault_state");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->battery2_bms_open_circuit_fault_state = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // battery1_bms_other_fault_state
    PyObject * field = PyObject_GetAttrString(_pymsg, "battery1_bms_other_fault_state");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->battery1_bms_other_fault_state = PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // battery2_bms_other_fault_state
    PyObject * field = PyObject_GetAttrString(_pymsg, "battery2_bms_other_fault_state");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->battery2_bms_other_fault_state = PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // battery1_outside_output_voltage
    PyObject * field = PyObject_GetAttrString(_pymsg, "battery1_outside_output_voltage");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->battery1_outside_output_voltage = (float)PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // battery2_outside_output_voltage
    PyObject * field = PyObject_GetAttrString(_pymsg, "battery2_outside_output_voltage");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->battery2_outside_output_voltage = (float)PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // battery1_outside_connection
    PyObject * field = PyObject_GetAttrString(_pymsg, "battery1_outside_connection");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->battery1_outside_connection = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // battery1_outside_open_circuit_fault_state
    PyObject * field = PyObject_GetAttrString(_pymsg, "battery1_outside_open_circuit_fault_state");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->battery1_outside_open_circuit_fault_state = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // battery2_outside_connection
    PyObject * field = PyObject_GetAttrString(_pymsg, "battery2_outside_connection");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->battery2_outside_connection = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // battery2_outside_open_circuit_fault_state
    PyObject * field = PyObject_GetAttrString(_pymsg, "battery2_outside_open_circuit_fault_state");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->battery2_outside_open_circuit_fault_state = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // charge_plug_input_voltage
    PyObject * field = PyObject_GetAttrString(_pymsg, "charge_plug_input_voltage");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->charge_plug_input_voltage = (float)PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // charge_plug_input_current
    PyObject * field = PyObject_GetAttrString(_pymsg, "charge_plug_input_current");
    if (!field) {
      return false;
    }
    assert(PyFloat_Check(field));
    ros_message->charge_plug_input_current = (float)PyFloat_AS_DOUBLE(field);
    Py_DECREF(field);
  }
  {  // charge_plug_input_short_circuit_fault_state
    PyObject * field = PyObject_GetAttrString(_pymsg, "charge_plug_input_short_circuit_fault_state");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->charge_plug_input_short_circuit_fault_state = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // charge_plug_input_open_circuit_fault_state
    PyObject * field = PyObject_GetAttrString(_pymsg, "charge_plug_input_open_circuit_fault_state");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->charge_plug_input_open_circuit_fault_state = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // chassis_power_board_fault_state
    PyObject * field = PyObject_GetAttrString(_pymsg, "chassis_power_board_fault_state");
    if (!field) {
      return false;
    }
    assert(PyLong_Check(field));
    ros_message->chassis_power_board_fault_state = (uint8_t)PyLong_AsUnsignedLong(field);
    Py_DECREF(field);
  }
  {  // power_board_software_version
    PyObject * field = PyObject_GetAttrString(_pymsg, "power_board_software_version");
    if (!field) {
      return false;
    }
    assert(PyUnicode_Check(field));
    PyObject * encoded_field = PyUnicode_AsUTF8String(field);
    if (!encoded_field) {
      Py_DECREF(field);
      return false;
    }
    rosidl_runtime_c__String__assign(&ros_message->power_board_software_version, PyBytes_AS_STRING(encoded_field));
    Py_DECREF(encoded_field);
    Py_DECREF(field);
  }
  {  // power_board_hardware_version
    PyObject * field = PyObject_GetAttrString(_pymsg, "power_board_hardware_version");
    if (!field) {
      return false;
    }
    assert(PyUnicode_Check(field));
    PyObject * encoded_field = PyUnicode_AsUTF8String(field);
    if (!encoded_field) {
      Py_DECREF(field);
      return false;
    }
    rosidl_runtime_c__String__assign(&ros_message->power_board_hardware_version, PyBytes_AS_STRING(encoded_field));
    Py_DECREF(encoded_field);
    Py_DECREF(field);
  }
  {  // power_board_serial_number
    PyObject * field = PyObject_GetAttrString(_pymsg, "power_board_serial_number");
    if (!field) {
      return false;
    }
    assert(PyUnicode_Check(field));
    PyObject * encoded_field = PyUnicode_AsUTF8String(field);
    if (!encoded_field) {
      Py_DECREF(field);
      return false;
    }
    rosidl_runtime_c__String__assign(&ros_message->power_board_serial_number, PyBytes_AS_STRING(encoded_field));
    Py_DECREF(encoded_field);
    Py_DECREF(field);
  }

  return true;
}

ROSIDL_GENERATOR_C_EXPORT
PyObject * genie_msgs__msg__battery_state__convert_to_py(void * raw_ros_message)
{
  /* NOTE(esteve): Call constructor of BatteryState */
  PyObject * _pymessage = NULL;
  {
    PyObject * pymessage_module = PyImport_ImportModule("genie_msgs.msg._battery_state");
    assert(pymessage_module);
    PyObject * pymessage_class = PyObject_GetAttrString(pymessage_module, "BatteryState");
    assert(pymessage_class);
    Py_DECREF(pymessage_module);
    _pymessage = PyObject_CallObject(pymessage_class, NULL);
    Py_DECREF(pymessage_class);
    if (!_pymessage) {
      return NULL;
    }
  }
  genie_msgs__msg__BatteryState * ros_message = (genie_msgs__msg__BatteryState *)raw_ros_message;
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
  {  // battery1_bms_charge_or_discharge
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->battery1_bms_charge_or_discharge);
    {
      int rc = PyObject_SetAttrString(_pymessage, "battery1_bms_charge_or_discharge", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // battery2_bms_charge_or_discharge
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->battery2_bms_charge_or_discharge);
    {
      int rc = PyObject_SetAttrString(_pymessage, "battery2_bms_charge_or_discharge", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // battery1_bms_output_voltage
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->battery1_bms_output_voltage);
    {
      int rc = PyObject_SetAttrString(_pymessage, "battery1_bms_output_voltage", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // battery2_bms_output_voltage
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->battery2_bms_output_voltage);
    {
      int rc = PyObject_SetAttrString(_pymessage, "battery2_bms_output_voltage", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // battery1_bms_output_current
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->battery1_bms_output_current);
    {
      int rc = PyObject_SetAttrString(_pymessage, "battery1_bms_output_current", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // battery2_bms_output_current
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->battery2_bms_output_current);
    {
      int rc = PyObject_SetAttrString(_pymessage, "battery2_bms_output_current", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // battery1_bms_charge_current
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->battery1_bms_charge_current);
    {
      int rc = PyObject_SetAttrString(_pymessage, "battery1_bms_charge_current", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // battery2_bms_charge_current
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->battery2_bms_charge_current);
    {
      int rc = PyObject_SetAttrString(_pymessage, "battery2_bms_charge_current", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // battery1_bms_temperature
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->battery1_bms_temperature);
    {
      int rc = PyObject_SetAttrString(_pymessage, "battery1_bms_temperature", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // battery2_bms_temperature
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->battery2_bms_temperature);
    {
      int rc = PyObject_SetAttrString(_pymessage, "battery2_bms_temperature", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // battery1_bms_soc
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->battery1_bms_soc);
    {
      int rc = PyObject_SetAttrString(_pymessage, "battery1_bms_soc", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // battery2_bms_soc
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->battery2_bms_soc);
    {
      int rc = PyObject_SetAttrString(_pymessage, "battery2_bms_soc", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // battery1_bms_soh
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->battery1_bms_soh);
    {
      int rc = PyObject_SetAttrString(_pymessage, "battery1_bms_soh", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // battery2_bms_soh
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->battery2_bms_soh);
    {
      int rc = PyObject_SetAttrString(_pymessage, "battery2_bms_soh", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // battery1_bms_short_circuit_fault_state
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->battery1_bms_short_circuit_fault_state);
    {
      int rc = PyObject_SetAttrString(_pymessage, "battery1_bms_short_circuit_fault_state", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // battery2_bms_short_circuit_fault_state
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->battery2_bms_short_circuit_fault_state);
    {
      int rc = PyObject_SetAttrString(_pymessage, "battery2_bms_short_circuit_fault_state", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // battery1_bms_open_circuit_fault_state
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->battery1_bms_open_circuit_fault_state);
    {
      int rc = PyObject_SetAttrString(_pymessage, "battery1_bms_open_circuit_fault_state", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // battery2_bms_open_circuit_fault_state
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->battery2_bms_open_circuit_fault_state);
    {
      int rc = PyObject_SetAttrString(_pymessage, "battery2_bms_open_circuit_fault_state", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // battery1_bms_other_fault_state
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->battery1_bms_other_fault_state);
    {
      int rc = PyObject_SetAttrString(_pymessage, "battery1_bms_other_fault_state", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // battery2_bms_other_fault_state
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->battery2_bms_other_fault_state);
    {
      int rc = PyObject_SetAttrString(_pymessage, "battery2_bms_other_fault_state", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // battery1_outside_output_voltage
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->battery1_outside_output_voltage);
    {
      int rc = PyObject_SetAttrString(_pymessage, "battery1_outside_output_voltage", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // battery2_outside_output_voltage
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->battery2_outside_output_voltage);
    {
      int rc = PyObject_SetAttrString(_pymessage, "battery2_outside_output_voltage", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // battery1_outside_connection
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->battery1_outside_connection);
    {
      int rc = PyObject_SetAttrString(_pymessage, "battery1_outside_connection", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // battery1_outside_open_circuit_fault_state
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->battery1_outside_open_circuit_fault_state);
    {
      int rc = PyObject_SetAttrString(_pymessage, "battery1_outside_open_circuit_fault_state", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // battery2_outside_connection
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->battery2_outside_connection);
    {
      int rc = PyObject_SetAttrString(_pymessage, "battery2_outside_connection", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // battery2_outside_open_circuit_fault_state
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->battery2_outside_open_circuit_fault_state);
    {
      int rc = PyObject_SetAttrString(_pymessage, "battery2_outside_open_circuit_fault_state", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // charge_plug_input_voltage
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->charge_plug_input_voltage);
    {
      int rc = PyObject_SetAttrString(_pymessage, "charge_plug_input_voltage", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // charge_plug_input_current
    PyObject * field = NULL;
    field = PyFloat_FromDouble(ros_message->charge_plug_input_current);
    {
      int rc = PyObject_SetAttrString(_pymessage, "charge_plug_input_current", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // charge_plug_input_short_circuit_fault_state
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->charge_plug_input_short_circuit_fault_state);
    {
      int rc = PyObject_SetAttrString(_pymessage, "charge_plug_input_short_circuit_fault_state", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // charge_plug_input_open_circuit_fault_state
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->charge_plug_input_open_circuit_fault_state);
    {
      int rc = PyObject_SetAttrString(_pymessage, "charge_plug_input_open_circuit_fault_state", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // chassis_power_board_fault_state
    PyObject * field = NULL;
    field = PyLong_FromUnsignedLong(ros_message->chassis_power_board_fault_state);
    {
      int rc = PyObject_SetAttrString(_pymessage, "chassis_power_board_fault_state", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // power_board_software_version
    PyObject * field = NULL;
    field = PyUnicode_DecodeUTF8(
      ros_message->power_board_software_version.data,
      strlen(ros_message->power_board_software_version.data),
      "replace");
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "power_board_software_version", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // power_board_hardware_version
    PyObject * field = NULL;
    field = PyUnicode_DecodeUTF8(
      ros_message->power_board_hardware_version.data,
      strlen(ros_message->power_board_hardware_version.data),
      "replace");
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "power_board_hardware_version", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }
  {  // power_board_serial_number
    PyObject * field = NULL;
    field = PyUnicode_DecodeUTF8(
      ros_message->power_board_serial_number.data,
      strlen(ros_message->power_board_serial_number.data),
      "replace");
    if (!field) {
      return NULL;
    }
    {
      int rc = PyObject_SetAttrString(_pymessage, "power_board_serial_number", field);
      Py_DECREF(field);
      if (rc) {
        return NULL;
      }
    }
  }

  // ownership of _pymessage is transferred to the caller
  return _pymessage;
}
