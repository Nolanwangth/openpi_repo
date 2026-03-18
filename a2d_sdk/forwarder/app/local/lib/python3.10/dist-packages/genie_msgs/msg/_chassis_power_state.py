# generated from rosidl_generator_py/resource/_idl.py.em
# with input from genie_msgs:msg/ChassisPowerState.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_ChassisPowerState(type):
    """Metaclass of message 'ChassisPowerState'."""

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
                'genie_msgs.msg.ChassisPowerState')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__chassis_power_state
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__chassis_power_state
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__chassis_power_state
            cls._TYPE_SUPPORT = module.type_support_msg__msg__chassis_power_state
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__chassis_power_state

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


class ChassisPowerState(metaclass=Metaclass_ChassisPowerState):
    """Message class 'ChassisPowerState'."""

    __slots__ = [
        '_header',
        '_battery_power_supply_button_state',
        '_emergency_stop_pedal_state',
        '_battery_power_supply_button_fault_state',
        '_emergency_stop_pedal_faul_state',
        '_chassis_power_board_power_state',
        '_chassis_left_traction_motor_power_state',
        '_chassis_right_traction_motor_power_state',
        '_chassis_left_steering_motor_power_state',
        '_chassis_right_steering_motor_power_state',
        '_chassis_lidar1_power_state',
        '_chassis_lidar2_power_state',
        '_chassis_ultrasonic_radar_power_state',
        '_chassis_tof_camera_power_state',
        '_chassis_ethernet_switch_power_state',
        '_chassis_output_power_state',
        '_charging_plug_power_state',
        '_battery_power_switch_power_state',
        '_battery1_bms_switch_power_state',
        '_battery2_bms_switch_power_state',
        '_battery1_unlock_state',
        '_battery2_unlock_state',
    ]

    _fields_and_field_types = {
        'header': 'std_msgs/Header',
        'battery_power_supply_button_state': 'uint8',
        'emergency_stop_pedal_state': 'uint8',
        'battery_power_supply_button_fault_state': 'uint8',
        'emergency_stop_pedal_faul_state': 'uint8',
        'chassis_power_board_power_state': 'uint8',
        'chassis_left_traction_motor_power_state': 'uint8',
        'chassis_right_traction_motor_power_state': 'uint8',
        'chassis_left_steering_motor_power_state': 'uint8',
        'chassis_right_steering_motor_power_state': 'uint8',
        'chassis_lidar1_power_state': 'uint8',
        'chassis_lidar2_power_state': 'uint8',
        'chassis_ultrasonic_radar_power_state': 'uint8',
        'chassis_tof_camera_power_state': 'uint8',
        'chassis_ethernet_switch_power_state': 'uint8',
        'chassis_output_power_state': 'uint8',
        'charging_plug_power_state': 'uint8',
        'battery_power_switch_power_state': 'uint8',
        'battery1_bms_switch_power_state': 'uint8',
        'battery2_bms_switch_power_state': 'uint8',
        'battery1_unlock_state': 'uint8',
        'battery2_unlock_state': 'uint8',
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
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        from std_msgs.msg import Header
        self.header = kwargs.get('header', Header())
        self.battery_power_supply_button_state = kwargs.get('battery_power_supply_button_state', int())
        self.emergency_stop_pedal_state = kwargs.get('emergency_stop_pedal_state', int())
        self.battery_power_supply_button_fault_state = kwargs.get('battery_power_supply_button_fault_state', int())
        self.emergency_stop_pedal_faul_state = kwargs.get('emergency_stop_pedal_faul_state', int())
        self.chassis_power_board_power_state = kwargs.get('chassis_power_board_power_state', int())
        self.chassis_left_traction_motor_power_state = kwargs.get('chassis_left_traction_motor_power_state', int())
        self.chassis_right_traction_motor_power_state = kwargs.get('chassis_right_traction_motor_power_state', int())
        self.chassis_left_steering_motor_power_state = kwargs.get('chassis_left_steering_motor_power_state', int())
        self.chassis_right_steering_motor_power_state = kwargs.get('chassis_right_steering_motor_power_state', int())
        self.chassis_lidar1_power_state = kwargs.get('chassis_lidar1_power_state', int())
        self.chassis_lidar2_power_state = kwargs.get('chassis_lidar2_power_state', int())
        self.chassis_ultrasonic_radar_power_state = kwargs.get('chassis_ultrasonic_radar_power_state', int())
        self.chassis_tof_camera_power_state = kwargs.get('chassis_tof_camera_power_state', int())
        self.chassis_ethernet_switch_power_state = kwargs.get('chassis_ethernet_switch_power_state', int())
        self.chassis_output_power_state = kwargs.get('chassis_output_power_state', int())
        self.charging_plug_power_state = kwargs.get('charging_plug_power_state', int())
        self.battery_power_switch_power_state = kwargs.get('battery_power_switch_power_state', int())
        self.battery1_bms_switch_power_state = kwargs.get('battery1_bms_switch_power_state', int())
        self.battery2_bms_switch_power_state = kwargs.get('battery2_bms_switch_power_state', int())
        self.battery1_unlock_state = kwargs.get('battery1_unlock_state', int())
        self.battery2_unlock_state = kwargs.get('battery2_unlock_state', int())

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
        if self.battery_power_supply_button_state != other.battery_power_supply_button_state:
            return False
        if self.emergency_stop_pedal_state != other.emergency_stop_pedal_state:
            return False
        if self.battery_power_supply_button_fault_state != other.battery_power_supply_button_fault_state:
            return False
        if self.emergency_stop_pedal_faul_state != other.emergency_stop_pedal_faul_state:
            return False
        if self.chassis_power_board_power_state != other.chassis_power_board_power_state:
            return False
        if self.chassis_left_traction_motor_power_state != other.chassis_left_traction_motor_power_state:
            return False
        if self.chassis_right_traction_motor_power_state != other.chassis_right_traction_motor_power_state:
            return False
        if self.chassis_left_steering_motor_power_state != other.chassis_left_steering_motor_power_state:
            return False
        if self.chassis_right_steering_motor_power_state != other.chassis_right_steering_motor_power_state:
            return False
        if self.chassis_lidar1_power_state != other.chassis_lidar1_power_state:
            return False
        if self.chassis_lidar2_power_state != other.chassis_lidar2_power_state:
            return False
        if self.chassis_ultrasonic_radar_power_state != other.chassis_ultrasonic_radar_power_state:
            return False
        if self.chassis_tof_camera_power_state != other.chassis_tof_camera_power_state:
            return False
        if self.chassis_ethernet_switch_power_state != other.chassis_ethernet_switch_power_state:
            return False
        if self.chassis_output_power_state != other.chassis_output_power_state:
            return False
        if self.charging_plug_power_state != other.charging_plug_power_state:
            return False
        if self.battery_power_switch_power_state != other.battery_power_switch_power_state:
            return False
        if self.battery1_bms_switch_power_state != other.battery1_bms_switch_power_state:
            return False
        if self.battery2_bms_switch_power_state != other.battery2_bms_switch_power_state:
            return False
        if self.battery1_unlock_state != other.battery1_unlock_state:
            return False
        if self.battery2_unlock_state != other.battery2_unlock_state:
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
    def battery_power_supply_button_state(self):
        """Message field 'battery_power_supply_button_state'."""
        return self._battery_power_supply_button_state

    @battery_power_supply_button_state.setter
    def battery_power_supply_button_state(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'battery_power_supply_button_state' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'battery_power_supply_button_state' field must be an unsigned integer in [0, 255]"
        self._battery_power_supply_button_state = value

    @builtins.property
    def emergency_stop_pedal_state(self):
        """Message field 'emergency_stop_pedal_state'."""
        return self._emergency_stop_pedal_state

    @emergency_stop_pedal_state.setter
    def emergency_stop_pedal_state(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'emergency_stop_pedal_state' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'emergency_stop_pedal_state' field must be an unsigned integer in [0, 255]"
        self._emergency_stop_pedal_state = value

    @builtins.property
    def battery_power_supply_button_fault_state(self):
        """Message field 'battery_power_supply_button_fault_state'."""
        return self._battery_power_supply_button_fault_state

    @battery_power_supply_button_fault_state.setter
    def battery_power_supply_button_fault_state(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'battery_power_supply_button_fault_state' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'battery_power_supply_button_fault_state' field must be an unsigned integer in [0, 255]"
        self._battery_power_supply_button_fault_state = value

    @builtins.property
    def emergency_stop_pedal_faul_state(self):
        """Message field 'emergency_stop_pedal_faul_state'."""
        return self._emergency_stop_pedal_faul_state

    @emergency_stop_pedal_faul_state.setter
    def emergency_stop_pedal_faul_state(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'emergency_stop_pedal_faul_state' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'emergency_stop_pedal_faul_state' field must be an unsigned integer in [0, 255]"
        self._emergency_stop_pedal_faul_state = value

    @builtins.property
    def chassis_power_board_power_state(self):
        """Message field 'chassis_power_board_power_state'."""
        return self._chassis_power_board_power_state

    @chassis_power_board_power_state.setter
    def chassis_power_board_power_state(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'chassis_power_board_power_state' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'chassis_power_board_power_state' field must be an unsigned integer in [0, 255]"
        self._chassis_power_board_power_state = value

    @builtins.property
    def chassis_left_traction_motor_power_state(self):
        """Message field 'chassis_left_traction_motor_power_state'."""
        return self._chassis_left_traction_motor_power_state

    @chassis_left_traction_motor_power_state.setter
    def chassis_left_traction_motor_power_state(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'chassis_left_traction_motor_power_state' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'chassis_left_traction_motor_power_state' field must be an unsigned integer in [0, 255]"
        self._chassis_left_traction_motor_power_state = value

    @builtins.property
    def chassis_right_traction_motor_power_state(self):
        """Message field 'chassis_right_traction_motor_power_state'."""
        return self._chassis_right_traction_motor_power_state

    @chassis_right_traction_motor_power_state.setter
    def chassis_right_traction_motor_power_state(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'chassis_right_traction_motor_power_state' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'chassis_right_traction_motor_power_state' field must be an unsigned integer in [0, 255]"
        self._chassis_right_traction_motor_power_state = value

    @builtins.property
    def chassis_left_steering_motor_power_state(self):
        """Message field 'chassis_left_steering_motor_power_state'."""
        return self._chassis_left_steering_motor_power_state

    @chassis_left_steering_motor_power_state.setter
    def chassis_left_steering_motor_power_state(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'chassis_left_steering_motor_power_state' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'chassis_left_steering_motor_power_state' field must be an unsigned integer in [0, 255]"
        self._chassis_left_steering_motor_power_state = value

    @builtins.property
    def chassis_right_steering_motor_power_state(self):
        """Message field 'chassis_right_steering_motor_power_state'."""
        return self._chassis_right_steering_motor_power_state

    @chassis_right_steering_motor_power_state.setter
    def chassis_right_steering_motor_power_state(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'chassis_right_steering_motor_power_state' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'chassis_right_steering_motor_power_state' field must be an unsigned integer in [0, 255]"
        self._chassis_right_steering_motor_power_state = value

    @builtins.property
    def chassis_lidar1_power_state(self):
        """Message field 'chassis_lidar1_power_state'."""
        return self._chassis_lidar1_power_state

    @chassis_lidar1_power_state.setter
    def chassis_lidar1_power_state(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'chassis_lidar1_power_state' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'chassis_lidar1_power_state' field must be an unsigned integer in [0, 255]"
        self._chassis_lidar1_power_state = value

    @builtins.property
    def chassis_lidar2_power_state(self):
        """Message field 'chassis_lidar2_power_state'."""
        return self._chassis_lidar2_power_state

    @chassis_lidar2_power_state.setter
    def chassis_lidar2_power_state(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'chassis_lidar2_power_state' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'chassis_lidar2_power_state' field must be an unsigned integer in [0, 255]"
        self._chassis_lidar2_power_state = value

    @builtins.property
    def chassis_ultrasonic_radar_power_state(self):
        """Message field 'chassis_ultrasonic_radar_power_state'."""
        return self._chassis_ultrasonic_radar_power_state

    @chassis_ultrasonic_radar_power_state.setter
    def chassis_ultrasonic_radar_power_state(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'chassis_ultrasonic_radar_power_state' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'chassis_ultrasonic_radar_power_state' field must be an unsigned integer in [0, 255]"
        self._chassis_ultrasonic_radar_power_state = value

    @builtins.property
    def chassis_tof_camera_power_state(self):
        """Message field 'chassis_tof_camera_power_state'."""
        return self._chassis_tof_camera_power_state

    @chassis_tof_camera_power_state.setter
    def chassis_tof_camera_power_state(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'chassis_tof_camera_power_state' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'chassis_tof_camera_power_state' field must be an unsigned integer in [0, 255]"
        self._chassis_tof_camera_power_state = value

    @builtins.property
    def chassis_ethernet_switch_power_state(self):
        """Message field 'chassis_ethernet_switch_power_state'."""
        return self._chassis_ethernet_switch_power_state

    @chassis_ethernet_switch_power_state.setter
    def chassis_ethernet_switch_power_state(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'chassis_ethernet_switch_power_state' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'chassis_ethernet_switch_power_state' field must be an unsigned integer in [0, 255]"
        self._chassis_ethernet_switch_power_state = value

    @builtins.property
    def chassis_output_power_state(self):
        """Message field 'chassis_output_power_state'."""
        return self._chassis_output_power_state

    @chassis_output_power_state.setter
    def chassis_output_power_state(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'chassis_output_power_state' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'chassis_output_power_state' field must be an unsigned integer in [0, 255]"
        self._chassis_output_power_state = value

    @builtins.property
    def charging_plug_power_state(self):
        """Message field 'charging_plug_power_state'."""
        return self._charging_plug_power_state

    @charging_plug_power_state.setter
    def charging_plug_power_state(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'charging_plug_power_state' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'charging_plug_power_state' field must be an unsigned integer in [0, 255]"
        self._charging_plug_power_state = value

    @builtins.property
    def battery_power_switch_power_state(self):
        """Message field 'battery_power_switch_power_state'."""
        return self._battery_power_switch_power_state

    @battery_power_switch_power_state.setter
    def battery_power_switch_power_state(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'battery_power_switch_power_state' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'battery_power_switch_power_state' field must be an unsigned integer in [0, 255]"
        self._battery_power_switch_power_state = value

    @builtins.property
    def battery1_bms_switch_power_state(self):
        """Message field 'battery1_bms_switch_power_state'."""
        return self._battery1_bms_switch_power_state

    @battery1_bms_switch_power_state.setter
    def battery1_bms_switch_power_state(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'battery1_bms_switch_power_state' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'battery1_bms_switch_power_state' field must be an unsigned integer in [0, 255]"
        self._battery1_bms_switch_power_state = value

    @builtins.property
    def battery2_bms_switch_power_state(self):
        """Message field 'battery2_bms_switch_power_state'."""
        return self._battery2_bms_switch_power_state

    @battery2_bms_switch_power_state.setter
    def battery2_bms_switch_power_state(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'battery2_bms_switch_power_state' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'battery2_bms_switch_power_state' field must be an unsigned integer in [0, 255]"
        self._battery2_bms_switch_power_state = value

    @builtins.property
    def battery1_unlock_state(self):
        """Message field 'battery1_unlock_state'."""
        return self._battery1_unlock_state

    @battery1_unlock_state.setter
    def battery1_unlock_state(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'battery1_unlock_state' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'battery1_unlock_state' field must be an unsigned integer in [0, 255]"
        self._battery1_unlock_state = value

    @builtins.property
    def battery2_unlock_state(self):
        """Message field 'battery2_unlock_state'."""
        return self._battery2_unlock_state

    @battery2_unlock_state.setter
    def battery2_unlock_state(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'battery2_unlock_state' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'battery2_unlock_state' field must be an unsigned integer in [0, 255]"
        self._battery2_unlock_state = value
