# generated from rosidl_generator_py/resource/_idl.py.em
# with input from genie_msgs:msg/ChestPowerState.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_ChestPowerState(type):
    """Metaclass of message 'ChestPowerState'."""

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
                'genie_msgs.msg.ChestPowerState')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__chest_power_state
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__chest_power_state
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__chest_power_state
            cls._TYPE_SUPPORT = module.type_support_msg__msg__chest_power_state
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__chest_power_state

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


class ChestPowerState(metaclass=Metaclass_ChestPowerState):
    """Message class 'ChestPowerState'."""

    __slots__ = [
        '_header',
        '_power_onoff_req',
        '_emergency_stop_button_req',
        '_power_button_fault_state',
        '_emergency_stop_button_fault_state',
        '_power_full_low_req',
        '_chest_power_board_power_state',
        '_domain_controller_power_state',
        '_head_interactive_board_power_state',
        '_curved_screen_power_state',
        '_head_yaw_motor_power_tate',
        '_head_pitch_motor_power_state',
        '_waist_yaw_motor_power_state',
        '_waist_pitch_motor_power_state',
        '_leg_bending1_motor_power_state',
        '_leg_bending2_motor_power_state',
        '_leg_bending3_motor_power_state',
        '_left_arm_power_state',
        '_right_arm_power_state',
        '_chest_light_strip_power_state',
        '_fan_power_state',
        '_mocap_poe_power_state',
        '_ipad_power_state',
        '_chest_reserved_lidar_power_state',
        '_chest_power_board_fault_state',
        '_power_board_software_version',
        '_power_board_hardware_version',
        '_power_board_serial_number',
    ]

    _fields_and_field_types = {
        'header': 'std_msgs/Header',
        'power_onoff_req': 'uint8',
        'emergency_stop_button_req': 'uint8',
        'power_button_fault_state': 'uint8',
        'emergency_stop_button_fault_state': 'uint8',
        'power_full_low_req': 'uint8',
        'chest_power_board_power_state': 'uint8',
        'domain_controller_power_state': 'uint8',
        'head_interactive_board_power_state': 'uint8',
        'curved_screen_power_state': 'uint8',
        'head_yaw_motor_power_tate': 'uint8',
        'head_pitch_motor_power_state': 'uint8',
        'waist_yaw_motor_power_state': 'uint8',
        'waist_pitch_motor_power_state': 'uint8',
        'leg_bending1_motor_power_state': 'uint8',
        'leg_bending2_motor_power_state': 'uint8',
        'leg_bending3_motor_power_state': 'uint8',
        'left_arm_power_state': 'uint8',
        'right_arm_power_state': 'uint8',
        'chest_light_strip_power_state': 'uint8',
        'fan_power_state': 'uint8',
        'mocap_poe_power_state': 'uint8',
        'ipad_power_state': 'uint8',
        'chest_reserved_lidar_power_state': 'uint8',
        'chest_power_board_fault_state': 'uint32',
        'power_board_software_version': 'string',
        'power_board_hardware_version': 'string',
        'power_board_serial_number': 'string',
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
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint32'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        from std_msgs.msg import Header
        self.header = kwargs.get('header', Header())
        self.power_onoff_req = kwargs.get('power_onoff_req', int())
        self.emergency_stop_button_req = kwargs.get('emergency_stop_button_req', int())
        self.power_button_fault_state = kwargs.get('power_button_fault_state', int())
        self.emergency_stop_button_fault_state = kwargs.get('emergency_stop_button_fault_state', int())
        self.power_full_low_req = kwargs.get('power_full_low_req', int())
        self.chest_power_board_power_state = kwargs.get('chest_power_board_power_state', int())
        self.domain_controller_power_state = kwargs.get('domain_controller_power_state', int())
        self.head_interactive_board_power_state = kwargs.get('head_interactive_board_power_state', int())
        self.curved_screen_power_state = kwargs.get('curved_screen_power_state', int())
        self.head_yaw_motor_power_tate = kwargs.get('head_yaw_motor_power_tate', int())
        self.head_pitch_motor_power_state = kwargs.get('head_pitch_motor_power_state', int())
        self.waist_yaw_motor_power_state = kwargs.get('waist_yaw_motor_power_state', int())
        self.waist_pitch_motor_power_state = kwargs.get('waist_pitch_motor_power_state', int())
        self.leg_bending1_motor_power_state = kwargs.get('leg_bending1_motor_power_state', int())
        self.leg_bending2_motor_power_state = kwargs.get('leg_bending2_motor_power_state', int())
        self.leg_bending3_motor_power_state = kwargs.get('leg_bending3_motor_power_state', int())
        self.left_arm_power_state = kwargs.get('left_arm_power_state', int())
        self.right_arm_power_state = kwargs.get('right_arm_power_state', int())
        self.chest_light_strip_power_state = kwargs.get('chest_light_strip_power_state', int())
        self.fan_power_state = kwargs.get('fan_power_state', int())
        self.mocap_poe_power_state = kwargs.get('mocap_poe_power_state', int())
        self.ipad_power_state = kwargs.get('ipad_power_state', int())
        self.chest_reserved_lidar_power_state = kwargs.get('chest_reserved_lidar_power_state', int())
        self.chest_power_board_fault_state = kwargs.get('chest_power_board_fault_state', int())
        self.power_board_software_version = kwargs.get('power_board_software_version', str())
        self.power_board_hardware_version = kwargs.get('power_board_hardware_version', str())
        self.power_board_serial_number = kwargs.get('power_board_serial_number', str())

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
        if self.power_onoff_req != other.power_onoff_req:
            return False
        if self.emergency_stop_button_req != other.emergency_stop_button_req:
            return False
        if self.power_button_fault_state != other.power_button_fault_state:
            return False
        if self.emergency_stop_button_fault_state != other.emergency_stop_button_fault_state:
            return False
        if self.power_full_low_req != other.power_full_low_req:
            return False
        if self.chest_power_board_power_state != other.chest_power_board_power_state:
            return False
        if self.domain_controller_power_state != other.domain_controller_power_state:
            return False
        if self.head_interactive_board_power_state != other.head_interactive_board_power_state:
            return False
        if self.curved_screen_power_state != other.curved_screen_power_state:
            return False
        if self.head_yaw_motor_power_tate != other.head_yaw_motor_power_tate:
            return False
        if self.head_pitch_motor_power_state != other.head_pitch_motor_power_state:
            return False
        if self.waist_yaw_motor_power_state != other.waist_yaw_motor_power_state:
            return False
        if self.waist_pitch_motor_power_state != other.waist_pitch_motor_power_state:
            return False
        if self.leg_bending1_motor_power_state != other.leg_bending1_motor_power_state:
            return False
        if self.leg_bending2_motor_power_state != other.leg_bending2_motor_power_state:
            return False
        if self.leg_bending3_motor_power_state != other.leg_bending3_motor_power_state:
            return False
        if self.left_arm_power_state != other.left_arm_power_state:
            return False
        if self.right_arm_power_state != other.right_arm_power_state:
            return False
        if self.chest_light_strip_power_state != other.chest_light_strip_power_state:
            return False
        if self.fan_power_state != other.fan_power_state:
            return False
        if self.mocap_poe_power_state != other.mocap_poe_power_state:
            return False
        if self.ipad_power_state != other.ipad_power_state:
            return False
        if self.chest_reserved_lidar_power_state != other.chest_reserved_lidar_power_state:
            return False
        if self.chest_power_board_fault_state != other.chest_power_board_fault_state:
            return False
        if self.power_board_software_version != other.power_board_software_version:
            return False
        if self.power_board_hardware_version != other.power_board_hardware_version:
            return False
        if self.power_board_serial_number != other.power_board_serial_number:
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
    def power_onoff_req(self):
        """Message field 'power_onoff_req'."""
        return self._power_onoff_req

    @power_onoff_req.setter
    def power_onoff_req(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'power_onoff_req' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'power_onoff_req' field must be an unsigned integer in [0, 255]"
        self._power_onoff_req = value

    @builtins.property
    def emergency_stop_button_req(self):
        """Message field 'emergency_stop_button_req'."""
        return self._emergency_stop_button_req

    @emergency_stop_button_req.setter
    def emergency_stop_button_req(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'emergency_stop_button_req' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'emergency_stop_button_req' field must be an unsigned integer in [0, 255]"
        self._emergency_stop_button_req = value

    @builtins.property
    def power_button_fault_state(self):
        """Message field 'power_button_fault_state'."""
        return self._power_button_fault_state

    @power_button_fault_state.setter
    def power_button_fault_state(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'power_button_fault_state' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'power_button_fault_state' field must be an unsigned integer in [0, 255]"
        self._power_button_fault_state = value

    @builtins.property
    def emergency_stop_button_fault_state(self):
        """Message field 'emergency_stop_button_fault_state'."""
        return self._emergency_stop_button_fault_state

    @emergency_stop_button_fault_state.setter
    def emergency_stop_button_fault_state(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'emergency_stop_button_fault_state' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'emergency_stop_button_fault_state' field must be an unsigned integer in [0, 255]"
        self._emergency_stop_button_fault_state = value

    @builtins.property
    def power_full_low_req(self):
        """Message field 'power_full_low_req'."""
        return self._power_full_low_req

    @power_full_low_req.setter
    def power_full_low_req(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'power_full_low_req' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'power_full_low_req' field must be an unsigned integer in [0, 255]"
        self._power_full_low_req = value

    @builtins.property
    def chest_power_board_power_state(self):
        """Message field 'chest_power_board_power_state'."""
        return self._chest_power_board_power_state

    @chest_power_board_power_state.setter
    def chest_power_board_power_state(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'chest_power_board_power_state' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'chest_power_board_power_state' field must be an unsigned integer in [0, 255]"
        self._chest_power_board_power_state = value

    @builtins.property
    def domain_controller_power_state(self):
        """Message field 'domain_controller_power_state'."""
        return self._domain_controller_power_state

    @domain_controller_power_state.setter
    def domain_controller_power_state(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'domain_controller_power_state' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'domain_controller_power_state' field must be an unsigned integer in [0, 255]"
        self._domain_controller_power_state = value

    @builtins.property
    def head_interactive_board_power_state(self):
        """Message field 'head_interactive_board_power_state'."""
        return self._head_interactive_board_power_state

    @head_interactive_board_power_state.setter
    def head_interactive_board_power_state(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'head_interactive_board_power_state' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'head_interactive_board_power_state' field must be an unsigned integer in [0, 255]"
        self._head_interactive_board_power_state = value

    @builtins.property
    def curved_screen_power_state(self):
        """Message field 'curved_screen_power_state'."""
        return self._curved_screen_power_state

    @curved_screen_power_state.setter
    def curved_screen_power_state(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'curved_screen_power_state' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'curved_screen_power_state' field must be an unsigned integer in [0, 255]"
        self._curved_screen_power_state = value

    @builtins.property
    def head_yaw_motor_power_tate(self):
        """Message field 'head_yaw_motor_power_tate'."""
        return self._head_yaw_motor_power_tate

    @head_yaw_motor_power_tate.setter
    def head_yaw_motor_power_tate(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'head_yaw_motor_power_tate' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'head_yaw_motor_power_tate' field must be an unsigned integer in [0, 255]"
        self._head_yaw_motor_power_tate = value

    @builtins.property
    def head_pitch_motor_power_state(self):
        """Message field 'head_pitch_motor_power_state'."""
        return self._head_pitch_motor_power_state

    @head_pitch_motor_power_state.setter
    def head_pitch_motor_power_state(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'head_pitch_motor_power_state' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'head_pitch_motor_power_state' field must be an unsigned integer in [0, 255]"
        self._head_pitch_motor_power_state = value

    @builtins.property
    def waist_yaw_motor_power_state(self):
        """Message field 'waist_yaw_motor_power_state'."""
        return self._waist_yaw_motor_power_state

    @waist_yaw_motor_power_state.setter
    def waist_yaw_motor_power_state(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'waist_yaw_motor_power_state' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'waist_yaw_motor_power_state' field must be an unsigned integer in [0, 255]"
        self._waist_yaw_motor_power_state = value

    @builtins.property
    def waist_pitch_motor_power_state(self):
        """Message field 'waist_pitch_motor_power_state'."""
        return self._waist_pitch_motor_power_state

    @waist_pitch_motor_power_state.setter
    def waist_pitch_motor_power_state(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'waist_pitch_motor_power_state' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'waist_pitch_motor_power_state' field must be an unsigned integer in [0, 255]"
        self._waist_pitch_motor_power_state = value

    @builtins.property
    def leg_bending1_motor_power_state(self):
        """Message field 'leg_bending1_motor_power_state'."""
        return self._leg_bending1_motor_power_state

    @leg_bending1_motor_power_state.setter
    def leg_bending1_motor_power_state(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'leg_bending1_motor_power_state' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'leg_bending1_motor_power_state' field must be an unsigned integer in [0, 255]"
        self._leg_bending1_motor_power_state = value

    @builtins.property
    def leg_bending2_motor_power_state(self):
        """Message field 'leg_bending2_motor_power_state'."""
        return self._leg_bending2_motor_power_state

    @leg_bending2_motor_power_state.setter
    def leg_bending2_motor_power_state(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'leg_bending2_motor_power_state' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'leg_bending2_motor_power_state' field must be an unsigned integer in [0, 255]"
        self._leg_bending2_motor_power_state = value

    @builtins.property
    def leg_bending3_motor_power_state(self):
        """Message field 'leg_bending3_motor_power_state'."""
        return self._leg_bending3_motor_power_state

    @leg_bending3_motor_power_state.setter
    def leg_bending3_motor_power_state(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'leg_bending3_motor_power_state' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'leg_bending3_motor_power_state' field must be an unsigned integer in [0, 255]"
        self._leg_bending3_motor_power_state = value

    @builtins.property
    def left_arm_power_state(self):
        """Message field 'left_arm_power_state'."""
        return self._left_arm_power_state

    @left_arm_power_state.setter
    def left_arm_power_state(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'left_arm_power_state' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'left_arm_power_state' field must be an unsigned integer in [0, 255]"
        self._left_arm_power_state = value

    @builtins.property
    def right_arm_power_state(self):
        """Message field 'right_arm_power_state'."""
        return self._right_arm_power_state

    @right_arm_power_state.setter
    def right_arm_power_state(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'right_arm_power_state' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'right_arm_power_state' field must be an unsigned integer in [0, 255]"
        self._right_arm_power_state = value

    @builtins.property
    def chest_light_strip_power_state(self):
        """Message field 'chest_light_strip_power_state'."""
        return self._chest_light_strip_power_state

    @chest_light_strip_power_state.setter
    def chest_light_strip_power_state(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'chest_light_strip_power_state' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'chest_light_strip_power_state' field must be an unsigned integer in [0, 255]"
        self._chest_light_strip_power_state = value

    @builtins.property
    def fan_power_state(self):
        """Message field 'fan_power_state'."""
        return self._fan_power_state

    @fan_power_state.setter
    def fan_power_state(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'fan_power_state' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'fan_power_state' field must be an unsigned integer in [0, 255]"
        self._fan_power_state = value

    @builtins.property
    def mocap_poe_power_state(self):
        """Message field 'mocap_poe_power_state'."""
        return self._mocap_poe_power_state

    @mocap_poe_power_state.setter
    def mocap_poe_power_state(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'mocap_poe_power_state' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'mocap_poe_power_state' field must be an unsigned integer in [0, 255]"
        self._mocap_poe_power_state = value

    @builtins.property
    def ipad_power_state(self):
        """Message field 'ipad_power_state'."""
        return self._ipad_power_state

    @ipad_power_state.setter
    def ipad_power_state(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'ipad_power_state' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'ipad_power_state' field must be an unsigned integer in [0, 255]"
        self._ipad_power_state = value

    @builtins.property
    def chest_reserved_lidar_power_state(self):
        """Message field 'chest_reserved_lidar_power_state'."""
        return self._chest_reserved_lidar_power_state

    @chest_reserved_lidar_power_state.setter
    def chest_reserved_lidar_power_state(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'chest_reserved_lidar_power_state' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'chest_reserved_lidar_power_state' field must be an unsigned integer in [0, 255]"
        self._chest_reserved_lidar_power_state = value

    @builtins.property
    def chest_power_board_fault_state(self):
        """Message field 'chest_power_board_fault_state'."""
        return self._chest_power_board_fault_state

    @chest_power_board_fault_state.setter
    def chest_power_board_fault_state(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'chest_power_board_fault_state' field must be of type 'int'"
            assert value >= 0 and value < 4294967296, \
                "The 'chest_power_board_fault_state' field must be an unsigned integer in [0, 4294967295]"
        self._chest_power_board_fault_state = value

    @builtins.property
    def power_board_software_version(self):
        """Message field 'power_board_software_version'."""
        return self._power_board_software_version

    @power_board_software_version.setter
    def power_board_software_version(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'power_board_software_version' field must be of type 'str'"
        self._power_board_software_version = value

    @builtins.property
    def power_board_hardware_version(self):
        """Message field 'power_board_hardware_version'."""
        return self._power_board_hardware_version

    @power_board_hardware_version.setter
    def power_board_hardware_version(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'power_board_hardware_version' field must be of type 'str'"
        self._power_board_hardware_version = value

    @builtins.property
    def power_board_serial_number(self):
        """Message field 'power_board_serial_number'."""
        return self._power_board_serial_number

    @power_board_serial_number.setter
    def power_board_serial_number(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'power_board_serial_number' field must be of type 'str'"
        self._power_board_serial_number = value
