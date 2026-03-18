# generated from rosidl_generator_py/resource/_idl.py.em
# with input from genie_msgs:msg/ChassisPowerCtrl.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import math  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_ChassisPowerCtrl(type):
    """Metaclass of message 'ChassisPowerCtrl'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
    }

    @classmethod
    def __import_type_support__(cls):
        try:
            from rosidl_generator_py import import_type_support
            module = import_type_support('genie_msgs')
        except ImportError:
            import logging
            import traceback
            logger = logging.getLogger(
                'genie_msgs.msg.ChassisPowerCtrl')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__chassis_power_ctrl
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__chassis_power_ctrl
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__chassis_power_ctrl
            cls._TYPE_SUPPORT = module.type_support_msg__msg__chassis_power_ctrl
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__chassis_power_ctrl

            from std_msgs.msg import Header
            if Header.__class__._TYPE_SUPPORT is None:
                Header.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
        }


class ChassisPowerCtrl(metaclass=Metaclass_ChassisPowerCtrl):
    """Message class 'ChassisPowerCtrl'."""

    __slots__ = [
        '_header',
        '_chassis_power_board_power_ctrlreq',
        '_chassis_left_traction_motor_power_ctrl_req',
        '_chassis_righttraction_motor_power_ctrl_req',
        '_chassis_left_steering_motor_power_ctrl_req',
        '_chassis_right_steering_motor_power_ctrl_req',
        '_chassis_lidar1_power_ctrl_req',
        '_chassis_lidar2_power_ctrl_req',
        '_chassis_ultrasonic_radar_power_ctrl_req',
        '_chassis_tof_camera_power_ctrl_req',
        '_chassis_ethernet_switch_power_ctrl_req',
        '_chassis_output_power_ctrl_req',
        '_charging_plug_power_ctrl_req',
        '_battery_power_switch_power_ctrl_req',
        '_battery1_bms_switch_power_ctrl_req',
        '_battery2_bms_switch_power_ctrl_req',
        '_battery1_unlock_ctrl_req',
        '_battery2_unlock_ctrl_req',
        '_charger_max_charging_current_ctrl_req',
        '_charger_max_charging_voltage_ctrl_req',
    ]

    _fields_and_field_types = {
        'header': 'std_msgs/Header',
        'chassis_power_board_power_ctrlreq': 'uint8',
        'chassis_left_traction_motor_power_ctrl_req': 'uint8',
        'chassis_righttraction_motor_power_ctrl_req': 'uint8',
        'chassis_left_steering_motor_power_ctrl_req': 'uint8',
        'chassis_right_steering_motor_power_ctrl_req': 'uint8',
        'chassis_lidar1_power_ctrl_req': 'uint8',
        'chassis_lidar2_power_ctrl_req': 'uint8',
        'chassis_ultrasonic_radar_power_ctrl_req': 'uint8',
        'chassis_tof_camera_power_ctrl_req': 'uint8',
        'chassis_ethernet_switch_power_ctrl_req': 'uint8',
        'chassis_output_power_ctrl_req': 'uint8',
        'charging_plug_power_ctrl_req': 'uint8',
        'battery_power_switch_power_ctrl_req': 'uint8',
        'battery1_bms_switch_power_ctrl_req': 'uint8',
        'battery2_bms_switch_power_ctrl_req': 'uint8',
        'battery1_unlock_ctrl_req': 'uint8',
        'battery2_unlock_ctrl_req': 'uint8',
        'charger_max_charging_current_ctrl_req': 'float',
        'charger_max_charging_voltage_ctrl_req': 'float',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.NamespacedType(['std_msgs', 'msg'], 'Header'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        from std_msgs.msg import Header
        self.header = kwargs.get('header', Header())
        self.chassis_power_board_power_ctrlreq = kwargs.get('chassis_power_board_power_ctrlreq', int())
        self.chassis_left_traction_motor_power_ctrl_req = kwargs.get('chassis_left_traction_motor_power_ctrl_req', int())
        self.chassis_righttraction_motor_power_ctrl_req = kwargs.get('chassis_righttraction_motor_power_ctrl_req', int())
        self.chassis_left_steering_motor_power_ctrl_req = kwargs.get('chassis_left_steering_motor_power_ctrl_req', int())
        self.chassis_right_steering_motor_power_ctrl_req = kwargs.get('chassis_right_steering_motor_power_ctrl_req', int())
        self.chassis_lidar1_power_ctrl_req = kwargs.get('chassis_lidar1_power_ctrl_req', int())
        self.chassis_lidar2_power_ctrl_req = kwargs.get('chassis_lidar2_power_ctrl_req', int())
        self.chassis_ultrasonic_radar_power_ctrl_req = kwargs.get('chassis_ultrasonic_radar_power_ctrl_req', int())
        self.chassis_tof_camera_power_ctrl_req = kwargs.get('chassis_tof_camera_power_ctrl_req', int())
        self.chassis_ethernet_switch_power_ctrl_req = kwargs.get('chassis_ethernet_switch_power_ctrl_req', int())
        self.chassis_output_power_ctrl_req = kwargs.get('chassis_output_power_ctrl_req', int())
        self.charging_plug_power_ctrl_req = kwargs.get('charging_plug_power_ctrl_req', int())
        self.battery_power_switch_power_ctrl_req = kwargs.get('battery_power_switch_power_ctrl_req', int())
        self.battery1_bms_switch_power_ctrl_req = kwargs.get('battery1_bms_switch_power_ctrl_req', int())
        self.battery2_bms_switch_power_ctrl_req = kwargs.get('battery2_bms_switch_power_ctrl_req', int())
        self.battery1_unlock_ctrl_req = kwargs.get('battery1_unlock_ctrl_req', int())
        self.battery2_unlock_ctrl_req = kwargs.get('battery2_unlock_ctrl_req', int())
        self.charger_max_charging_current_ctrl_req = kwargs.get('charger_max_charging_current_ctrl_req', float())
        self.charger_max_charging_voltage_ctrl_req = kwargs.get('charger_max_charging_voltage_ctrl_req', float())

    def __repr__(self):
        typename = self.__class__.__module__.split('.')
        typename.pop()
        typename.append(self.__class__.__name__)
        args = []
        for s, t in zip(self.__slots__, self.SLOT_TYPES):
            field = getattr(self, s)
            fieldstr = repr(field)
            # We use Python array type for fields that can be directly stored
            # in them, and "normal" sequences for everything else.  If it is
            # a type that we store in an array, strip off the 'array' portion.
            if (
                isinstance(t, rosidl_parser.definition.AbstractSequence) and
                isinstance(t.value_type, rosidl_parser.definition.BasicType) and
                t.value_type.typename in ['float', 'double', 'int8', 'uint8', 'int16', 'uint16', 'int32', 'uint32', 'int64', 'uint64']
            ):
                if len(field) == 0:
                    fieldstr = '[]'
                else:
                    assert fieldstr.startswith('array(')
                    prefix = "array('X', "
                    suffix = ')'
                    fieldstr = fieldstr[len(prefix):-len(suffix)]
            args.append(s[1:] + '=' + fieldstr)
        return '%s(%s)' % ('.'.join(typename), ', '.join(args))

    def __eq__(self, other):
        if not isinstance(other, self.__class__):
            return False
        if self.header != other.header:
            return False
        if self.chassis_power_board_power_ctrlreq != other.chassis_power_board_power_ctrlreq:
            return False
        if self.chassis_left_traction_motor_power_ctrl_req != other.chassis_left_traction_motor_power_ctrl_req:
            return False
        if self.chassis_righttraction_motor_power_ctrl_req != other.chassis_righttraction_motor_power_ctrl_req:
            return False
        if self.chassis_left_steering_motor_power_ctrl_req != other.chassis_left_steering_motor_power_ctrl_req:
            return False
        if self.chassis_right_steering_motor_power_ctrl_req != other.chassis_right_steering_motor_power_ctrl_req:
            return False
        if self.chassis_lidar1_power_ctrl_req != other.chassis_lidar1_power_ctrl_req:
            return False
        if self.chassis_lidar2_power_ctrl_req != other.chassis_lidar2_power_ctrl_req:
            return False
        if self.chassis_ultrasonic_radar_power_ctrl_req != other.chassis_ultrasonic_radar_power_ctrl_req:
            return False
        if self.chassis_tof_camera_power_ctrl_req != other.chassis_tof_camera_power_ctrl_req:
            return False
        if self.chassis_ethernet_switch_power_ctrl_req != other.chassis_ethernet_switch_power_ctrl_req:
            return False
        if self.chassis_output_power_ctrl_req != other.chassis_output_power_ctrl_req:
            return False
        if self.charging_plug_power_ctrl_req != other.charging_plug_power_ctrl_req:
            return False
        if self.battery_power_switch_power_ctrl_req != other.battery_power_switch_power_ctrl_req:
            return False
        if self.battery1_bms_switch_power_ctrl_req != other.battery1_bms_switch_power_ctrl_req:
            return False
        if self.battery2_bms_switch_power_ctrl_req != other.battery2_bms_switch_power_ctrl_req:
            return False
        if self.battery1_unlock_ctrl_req != other.battery1_unlock_ctrl_req:
            return False
        if self.battery2_unlock_ctrl_req != other.battery2_unlock_ctrl_req:
            return False
        if self.charger_max_charging_current_ctrl_req != other.charger_max_charging_current_ctrl_req:
            return False
        if self.charger_max_charging_voltage_ctrl_req != other.charger_max_charging_voltage_ctrl_req:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def header(self):
        """Message field 'header'."""
        return self._header

    @header.setter
    def header(self, value):
        if __debug__:
            from std_msgs.msg import Header
            assert \
                isinstance(value, Header), \
                "The 'header' field must be a sub message of type 'Header'"
        self._header = value

    @builtins.property
    def chassis_power_board_power_ctrlreq(self):
        """Message field 'chassis_power_board_power_ctrlreq'."""
        return self._chassis_power_board_power_ctrlreq

    @chassis_power_board_power_ctrlreq.setter
    def chassis_power_board_power_ctrlreq(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'chassis_power_board_power_ctrlreq' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'chassis_power_board_power_ctrlreq' field must be an unsigned integer in [0, 255]"
        self._chassis_power_board_power_ctrlreq = value

    @builtins.property
    def chassis_left_traction_motor_power_ctrl_req(self):
        """Message field 'chassis_left_traction_motor_power_ctrl_req'."""
        return self._chassis_left_traction_motor_power_ctrl_req

    @chassis_left_traction_motor_power_ctrl_req.setter
    def chassis_left_traction_motor_power_ctrl_req(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'chassis_left_traction_motor_power_ctrl_req' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'chassis_left_traction_motor_power_ctrl_req' field must be an unsigned integer in [0, 255]"
        self._chassis_left_traction_motor_power_ctrl_req = value

    @builtins.property
    def chassis_righttraction_motor_power_ctrl_req(self):
        """Message field 'chassis_righttraction_motor_power_ctrl_req'."""
        return self._chassis_righttraction_motor_power_ctrl_req

    @chassis_righttraction_motor_power_ctrl_req.setter
    def chassis_righttraction_motor_power_ctrl_req(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'chassis_righttraction_motor_power_ctrl_req' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'chassis_righttraction_motor_power_ctrl_req' field must be an unsigned integer in [0, 255]"
        self._chassis_righttraction_motor_power_ctrl_req = value

    @builtins.property
    def chassis_left_steering_motor_power_ctrl_req(self):
        """Message field 'chassis_left_steering_motor_power_ctrl_req'."""
        return self._chassis_left_steering_motor_power_ctrl_req

    @chassis_left_steering_motor_power_ctrl_req.setter
    def chassis_left_steering_motor_power_ctrl_req(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'chassis_left_steering_motor_power_ctrl_req' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'chassis_left_steering_motor_power_ctrl_req' field must be an unsigned integer in [0, 255]"
        self._chassis_left_steering_motor_power_ctrl_req = value

    @builtins.property
    def chassis_right_steering_motor_power_ctrl_req(self):
        """Message field 'chassis_right_steering_motor_power_ctrl_req'."""
        return self._chassis_right_steering_motor_power_ctrl_req

    @chassis_right_steering_motor_power_ctrl_req.setter
    def chassis_right_steering_motor_power_ctrl_req(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'chassis_right_steering_motor_power_ctrl_req' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'chassis_right_steering_motor_power_ctrl_req' field must be an unsigned integer in [0, 255]"
        self._chassis_right_steering_motor_power_ctrl_req = value

    @builtins.property
    def chassis_lidar1_power_ctrl_req(self):
        """Message field 'chassis_lidar1_power_ctrl_req'."""
        return self._chassis_lidar1_power_ctrl_req

    @chassis_lidar1_power_ctrl_req.setter
    def chassis_lidar1_power_ctrl_req(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'chassis_lidar1_power_ctrl_req' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'chassis_lidar1_power_ctrl_req' field must be an unsigned integer in [0, 255]"
        self._chassis_lidar1_power_ctrl_req = value

    @builtins.property
    def chassis_lidar2_power_ctrl_req(self):
        """Message field 'chassis_lidar2_power_ctrl_req'."""
        return self._chassis_lidar2_power_ctrl_req

    @chassis_lidar2_power_ctrl_req.setter
    def chassis_lidar2_power_ctrl_req(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'chassis_lidar2_power_ctrl_req' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'chassis_lidar2_power_ctrl_req' field must be an unsigned integer in [0, 255]"
        self._chassis_lidar2_power_ctrl_req = value

    @builtins.property
    def chassis_ultrasonic_radar_power_ctrl_req(self):
        """Message field 'chassis_ultrasonic_radar_power_ctrl_req'."""
        return self._chassis_ultrasonic_radar_power_ctrl_req

    @chassis_ultrasonic_radar_power_ctrl_req.setter
    def chassis_ultrasonic_radar_power_ctrl_req(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'chassis_ultrasonic_radar_power_ctrl_req' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'chassis_ultrasonic_radar_power_ctrl_req' field must be an unsigned integer in [0, 255]"
        self._chassis_ultrasonic_radar_power_ctrl_req = value

    @builtins.property
    def chassis_tof_camera_power_ctrl_req(self):
        """Message field 'chassis_tof_camera_power_ctrl_req'."""
        return self._chassis_tof_camera_power_ctrl_req

    @chassis_tof_camera_power_ctrl_req.setter
    def chassis_tof_camera_power_ctrl_req(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'chassis_tof_camera_power_ctrl_req' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'chassis_tof_camera_power_ctrl_req' field must be an unsigned integer in [0, 255]"
        self._chassis_tof_camera_power_ctrl_req = value

    @builtins.property
    def chassis_ethernet_switch_power_ctrl_req(self):
        """Message field 'chassis_ethernet_switch_power_ctrl_req'."""
        return self._chassis_ethernet_switch_power_ctrl_req

    @chassis_ethernet_switch_power_ctrl_req.setter
    def chassis_ethernet_switch_power_ctrl_req(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'chassis_ethernet_switch_power_ctrl_req' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'chassis_ethernet_switch_power_ctrl_req' field must be an unsigned integer in [0, 255]"
        self._chassis_ethernet_switch_power_ctrl_req = value

    @builtins.property
    def chassis_output_power_ctrl_req(self):
        """Message field 'chassis_output_power_ctrl_req'."""
        return self._chassis_output_power_ctrl_req

    @chassis_output_power_ctrl_req.setter
    def chassis_output_power_ctrl_req(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'chassis_output_power_ctrl_req' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'chassis_output_power_ctrl_req' field must be an unsigned integer in [0, 255]"
        self._chassis_output_power_ctrl_req = value

    @builtins.property
    def charging_plug_power_ctrl_req(self):
        """Message field 'charging_plug_power_ctrl_req'."""
        return self._charging_plug_power_ctrl_req

    @charging_plug_power_ctrl_req.setter
    def charging_plug_power_ctrl_req(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'charging_plug_power_ctrl_req' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'charging_plug_power_ctrl_req' field must be an unsigned integer in [0, 255]"
        self._charging_plug_power_ctrl_req = value

    @builtins.property
    def battery_power_switch_power_ctrl_req(self):
        """Message field 'battery_power_switch_power_ctrl_req'."""
        return self._battery_power_switch_power_ctrl_req

    @battery_power_switch_power_ctrl_req.setter
    def battery_power_switch_power_ctrl_req(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'battery_power_switch_power_ctrl_req' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'battery_power_switch_power_ctrl_req' field must be an unsigned integer in [0, 255]"
        self._battery_power_switch_power_ctrl_req = value

    @builtins.property
    def battery1_bms_switch_power_ctrl_req(self):
        """Message field 'battery1_bms_switch_power_ctrl_req'."""
        return self._battery1_bms_switch_power_ctrl_req

    @battery1_bms_switch_power_ctrl_req.setter
    def battery1_bms_switch_power_ctrl_req(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'battery1_bms_switch_power_ctrl_req' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'battery1_bms_switch_power_ctrl_req' field must be an unsigned integer in [0, 255]"
        self._battery1_bms_switch_power_ctrl_req = value

    @builtins.property
    def battery2_bms_switch_power_ctrl_req(self):
        """Message field 'battery2_bms_switch_power_ctrl_req'."""
        return self._battery2_bms_switch_power_ctrl_req

    @battery2_bms_switch_power_ctrl_req.setter
    def battery2_bms_switch_power_ctrl_req(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'battery2_bms_switch_power_ctrl_req' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'battery2_bms_switch_power_ctrl_req' field must be an unsigned integer in [0, 255]"
        self._battery2_bms_switch_power_ctrl_req = value

    @builtins.property
    def battery1_unlock_ctrl_req(self):
        """Message field 'battery1_unlock_ctrl_req'."""
        return self._battery1_unlock_ctrl_req

    @battery1_unlock_ctrl_req.setter
    def battery1_unlock_ctrl_req(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'battery1_unlock_ctrl_req' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'battery1_unlock_ctrl_req' field must be an unsigned integer in [0, 255]"
        self._battery1_unlock_ctrl_req = value

    @builtins.property
    def battery2_unlock_ctrl_req(self):
        """Message field 'battery2_unlock_ctrl_req'."""
        return self._battery2_unlock_ctrl_req

    @battery2_unlock_ctrl_req.setter
    def battery2_unlock_ctrl_req(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'battery2_unlock_ctrl_req' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'battery2_unlock_ctrl_req' field must be an unsigned integer in [0, 255]"
        self._battery2_unlock_ctrl_req = value

    @builtins.property
    def charger_max_charging_current_ctrl_req(self):
        """Message field 'charger_max_charging_current_ctrl_req'."""
        return self._charger_max_charging_current_ctrl_req

    @charger_max_charging_current_ctrl_req.setter
    def charger_max_charging_current_ctrl_req(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'charger_max_charging_current_ctrl_req' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'charger_max_charging_current_ctrl_req' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._charger_max_charging_current_ctrl_req = value

    @builtins.property
    def charger_max_charging_voltage_ctrl_req(self):
        """Message field 'charger_max_charging_voltage_ctrl_req'."""
        return self._charger_max_charging_voltage_ctrl_req

    @charger_max_charging_voltage_ctrl_req.setter
    def charger_max_charging_voltage_ctrl_req(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'charger_max_charging_voltage_ctrl_req' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'charger_max_charging_voltage_ctrl_req' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._charger_max_charging_voltage_ctrl_req = value
