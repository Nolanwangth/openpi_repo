# generated from rosidl_generator_py/resource/_idl.py.em
# with input from genie_msgs:msg/ChestPowerCtrl.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_ChestPowerCtrl(type):
    """Metaclass of message 'ChestPowerCtrl'."""

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
                'genie_msgs.msg.ChestPowerCtrl')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__chest_power_ctrl
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__chest_power_ctrl
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__chest_power_ctrl
            cls._TYPE_SUPPORT = module.type_support_msg__msg__chest_power_ctrl
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__chest_power_ctrl

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


class ChestPowerCtrl(metaclass=Metaclass_ChestPowerCtrl):
    """Message class 'ChestPowerCtrl'."""

    __slots__ = [
        '_header',
        '_chest_power_board_power_ctrl_req',
        '_head_interactive_board_power_ctrl_req',
        '_curved_screen_power_ctrl_req',
        '_head_yaw_motor_power_ctrl_req',
        '_head_pitch_motor_power_ctrl_req',
        '_waist_yaw_motor_power_ctrl_req',
        '_waist_pitch_motor_power_ctrl_req',
        '_leg_bending1_motor_power_ctrl_req',
        '_leg_bending2_motor_power_ctrl_req',
        '_leg_bending3_motor_power_ctrl_req',
        '_left_arm_power_ctrl_req',
        '_right_arm_power_ctrl_req',
        '_chest_light_strip_power_ctrl_req',
        '_fan_power_ctrl_req',
        '_mocap_poe_power_ctrl_req',
        '_ipad_power_ctrl_req',
        '_chest_reserved_lidar_power_ctrl_req',
    ]

    _fields_and_field_types = {
        'header': 'std_msgs/Header',
        'chest_power_board_power_ctrl_req': 'uint8',
        'head_interactive_board_power_ctrl_req': 'uint8',
        'curved_screen_power_ctrl_req': 'uint8',
        'head_yaw_motor_power_ctrl_req': 'uint8',
        'head_pitch_motor_power_ctrl_req': 'uint8',
        'waist_yaw_motor_power_ctrl_req': 'uint8',
        'waist_pitch_motor_power_ctrl_req': 'uint8',
        'leg_bending1_motor_power_ctrl_req': 'uint8',
        'leg_bending2_motor_power_ctrl_req': 'uint8',
        'leg_bending3_motor_power_ctrl_req': 'uint8',
        'left_arm_power_ctrl_req': 'uint8',
        'right_arm_power_ctrl_req': 'uint8',
        'chest_light_strip_power_ctrl_req': 'uint8',
        'fan_power_ctrl_req': 'uint8',
        'mocap_poe_power_ctrl_req': 'uint8',
        'ipad_power_ctrl_req': 'uint8',
        'chest_reserved_lidar_power_ctrl_req': 'uint8',
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
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        from std_msgs.msg import Header
        self.header = kwargs.get('header', Header())
        self.chest_power_board_power_ctrl_req = kwargs.get('chest_power_board_power_ctrl_req', int())
        self.head_interactive_board_power_ctrl_req = kwargs.get('head_interactive_board_power_ctrl_req', int())
        self.curved_screen_power_ctrl_req = kwargs.get('curved_screen_power_ctrl_req', int())
        self.head_yaw_motor_power_ctrl_req = kwargs.get('head_yaw_motor_power_ctrl_req', int())
        self.head_pitch_motor_power_ctrl_req = kwargs.get('head_pitch_motor_power_ctrl_req', int())
        self.waist_yaw_motor_power_ctrl_req = kwargs.get('waist_yaw_motor_power_ctrl_req', int())
        self.waist_pitch_motor_power_ctrl_req = kwargs.get('waist_pitch_motor_power_ctrl_req', int())
        self.leg_bending1_motor_power_ctrl_req = kwargs.get('leg_bending1_motor_power_ctrl_req', int())
        self.leg_bending2_motor_power_ctrl_req = kwargs.get('leg_bending2_motor_power_ctrl_req', int())
        self.leg_bending3_motor_power_ctrl_req = kwargs.get('leg_bending3_motor_power_ctrl_req', int())
        self.left_arm_power_ctrl_req = kwargs.get('left_arm_power_ctrl_req', int())
        self.right_arm_power_ctrl_req = kwargs.get('right_arm_power_ctrl_req', int())
        self.chest_light_strip_power_ctrl_req = kwargs.get('chest_light_strip_power_ctrl_req', int())
        self.fan_power_ctrl_req = kwargs.get('fan_power_ctrl_req', int())
        self.mocap_poe_power_ctrl_req = kwargs.get('mocap_poe_power_ctrl_req', int())
        self.ipad_power_ctrl_req = kwargs.get('ipad_power_ctrl_req', int())
        self.chest_reserved_lidar_power_ctrl_req = kwargs.get('chest_reserved_lidar_power_ctrl_req', int())

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
        if self.chest_power_board_power_ctrl_req != other.chest_power_board_power_ctrl_req:
            return False
        if self.head_interactive_board_power_ctrl_req != other.head_interactive_board_power_ctrl_req:
            return False
        if self.curved_screen_power_ctrl_req != other.curved_screen_power_ctrl_req:
            return False
        if self.head_yaw_motor_power_ctrl_req != other.head_yaw_motor_power_ctrl_req:
            return False
        if self.head_pitch_motor_power_ctrl_req != other.head_pitch_motor_power_ctrl_req:
            return False
        if self.waist_yaw_motor_power_ctrl_req != other.waist_yaw_motor_power_ctrl_req:
            return False
        if self.waist_pitch_motor_power_ctrl_req != other.waist_pitch_motor_power_ctrl_req:
            return False
        if self.leg_bending1_motor_power_ctrl_req != other.leg_bending1_motor_power_ctrl_req:
            return False
        if self.leg_bending2_motor_power_ctrl_req != other.leg_bending2_motor_power_ctrl_req:
            return False
        if self.leg_bending3_motor_power_ctrl_req != other.leg_bending3_motor_power_ctrl_req:
            return False
        if self.left_arm_power_ctrl_req != other.left_arm_power_ctrl_req:
            return False
        if self.right_arm_power_ctrl_req != other.right_arm_power_ctrl_req:
            return False
        if self.chest_light_strip_power_ctrl_req != other.chest_light_strip_power_ctrl_req:
            return False
        if self.fan_power_ctrl_req != other.fan_power_ctrl_req:
            return False
        if self.mocap_poe_power_ctrl_req != other.mocap_poe_power_ctrl_req:
            return False
        if self.ipad_power_ctrl_req != other.ipad_power_ctrl_req:
            return False
        if self.chest_reserved_lidar_power_ctrl_req != other.chest_reserved_lidar_power_ctrl_req:
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
    def chest_power_board_power_ctrl_req(self):
        """Message field 'chest_power_board_power_ctrl_req'."""
        return self._chest_power_board_power_ctrl_req

    @chest_power_board_power_ctrl_req.setter
    def chest_power_board_power_ctrl_req(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'chest_power_board_power_ctrl_req' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'chest_power_board_power_ctrl_req' field must be an unsigned integer in [0, 255]"
        self._chest_power_board_power_ctrl_req = value

    @builtins.property
    def head_interactive_board_power_ctrl_req(self):
        """Message field 'head_interactive_board_power_ctrl_req'."""
        return self._head_interactive_board_power_ctrl_req

    @head_interactive_board_power_ctrl_req.setter
    def head_interactive_board_power_ctrl_req(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'head_interactive_board_power_ctrl_req' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'head_interactive_board_power_ctrl_req' field must be an unsigned integer in [0, 255]"
        self._head_interactive_board_power_ctrl_req = value

    @builtins.property
    def curved_screen_power_ctrl_req(self):
        """Message field 'curved_screen_power_ctrl_req'."""
        return self._curved_screen_power_ctrl_req

    @curved_screen_power_ctrl_req.setter
    def curved_screen_power_ctrl_req(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'curved_screen_power_ctrl_req' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'curved_screen_power_ctrl_req' field must be an unsigned integer in [0, 255]"
        self._curved_screen_power_ctrl_req = value

    @builtins.property
    def head_yaw_motor_power_ctrl_req(self):
        """Message field 'head_yaw_motor_power_ctrl_req'."""
        return self._head_yaw_motor_power_ctrl_req

    @head_yaw_motor_power_ctrl_req.setter
    def head_yaw_motor_power_ctrl_req(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'head_yaw_motor_power_ctrl_req' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'head_yaw_motor_power_ctrl_req' field must be an unsigned integer in [0, 255]"
        self._head_yaw_motor_power_ctrl_req = value

    @builtins.property
    def head_pitch_motor_power_ctrl_req(self):
        """Message field 'head_pitch_motor_power_ctrl_req'."""
        return self._head_pitch_motor_power_ctrl_req

    @head_pitch_motor_power_ctrl_req.setter
    def head_pitch_motor_power_ctrl_req(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'head_pitch_motor_power_ctrl_req' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'head_pitch_motor_power_ctrl_req' field must be an unsigned integer in [0, 255]"
        self._head_pitch_motor_power_ctrl_req = value

    @builtins.property
    def waist_yaw_motor_power_ctrl_req(self):
        """Message field 'waist_yaw_motor_power_ctrl_req'."""
        return self._waist_yaw_motor_power_ctrl_req

    @waist_yaw_motor_power_ctrl_req.setter
    def waist_yaw_motor_power_ctrl_req(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'waist_yaw_motor_power_ctrl_req' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'waist_yaw_motor_power_ctrl_req' field must be an unsigned integer in [0, 255]"
        self._waist_yaw_motor_power_ctrl_req = value

    @builtins.property
    def waist_pitch_motor_power_ctrl_req(self):
        """Message field 'waist_pitch_motor_power_ctrl_req'."""
        return self._waist_pitch_motor_power_ctrl_req

    @waist_pitch_motor_power_ctrl_req.setter
    def waist_pitch_motor_power_ctrl_req(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'waist_pitch_motor_power_ctrl_req' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'waist_pitch_motor_power_ctrl_req' field must be an unsigned integer in [0, 255]"
        self._waist_pitch_motor_power_ctrl_req = value

    @builtins.property
    def leg_bending1_motor_power_ctrl_req(self):
        """Message field 'leg_bending1_motor_power_ctrl_req'."""
        return self._leg_bending1_motor_power_ctrl_req

    @leg_bending1_motor_power_ctrl_req.setter
    def leg_bending1_motor_power_ctrl_req(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'leg_bending1_motor_power_ctrl_req' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'leg_bending1_motor_power_ctrl_req' field must be an unsigned integer in [0, 255]"
        self._leg_bending1_motor_power_ctrl_req = value

    @builtins.property
    def leg_bending2_motor_power_ctrl_req(self):
        """Message field 'leg_bending2_motor_power_ctrl_req'."""
        return self._leg_bending2_motor_power_ctrl_req

    @leg_bending2_motor_power_ctrl_req.setter
    def leg_bending2_motor_power_ctrl_req(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'leg_bending2_motor_power_ctrl_req' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'leg_bending2_motor_power_ctrl_req' field must be an unsigned integer in [0, 255]"
        self._leg_bending2_motor_power_ctrl_req = value

    @builtins.property
    def leg_bending3_motor_power_ctrl_req(self):
        """Message field 'leg_bending3_motor_power_ctrl_req'."""
        return self._leg_bending3_motor_power_ctrl_req

    @leg_bending3_motor_power_ctrl_req.setter
    def leg_bending3_motor_power_ctrl_req(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'leg_bending3_motor_power_ctrl_req' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'leg_bending3_motor_power_ctrl_req' field must be an unsigned integer in [0, 255]"
        self._leg_bending3_motor_power_ctrl_req = value

    @builtins.property
    def left_arm_power_ctrl_req(self):
        """Message field 'left_arm_power_ctrl_req'."""
        return self._left_arm_power_ctrl_req

    @left_arm_power_ctrl_req.setter
    def left_arm_power_ctrl_req(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'left_arm_power_ctrl_req' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'left_arm_power_ctrl_req' field must be an unsigned integer in [0, 255]"
        self._left_arm_power_ctrl_req = value

    @builtins.property
    def right_arm_power_ctrl_req(self):
        """Message field 'right_arm_power_ctrl_req'."""
        return self._right_arm_power_ctrl_req

    @right_arm_power_ctrl_req.setter
    def right_arm_power_ctrl_req(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'right_arm_power_ctrl_req' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'right_arm_power_ctrl_req' field must be an unsigned integer in [0, 255]"
        self._right_arm_power_ctrl_req = value

    @builtins.property
    def chest_light_strip_power_ctrl_req(self):
        """Message field 'chest_light_strip_power_ctrl_req'."""
        return self._chest_light_strip_power_ctrl_req

    @chest_light_strip_power_ctrl_req.setter
    def chest_light_strip_power_ctrl_req(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'chest_light_strip_power_ctrl_req' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'chest_light_strip_power_ctrl_req' field must be an unsigned integer in [0, 255]"
        self._chest_light_strip_power_ctrl_req = value

    @builtins.property
    def fan_power_ctrl_req(self):
        """Message field 'fan_power_ctrl_req'."""
        return self._fan_power_ctrl_req

    @fan_power_ctrl_req.setter
    def fan_power_ctrl_req(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'fan_power_ctrl_req' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'fan_power_ctrl_req' field must be an unsigned integer in [0, 255]"
        self._fan_power_ctrl_req = value

    @builtins.property
    def mocap_poe_power_ctrl_req(self):
        """Message field 'mocap_poe_power_ctrl_req'."""
        return self._mocap_poe_power_ctrl_req

    @mocap_poe_power_ctrl_req.setter
    def mocap_poe_power_ctrl_req(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'mocap_poe_power_ctrl_req' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'mocap_poe_power_ctrl_req' field must be an unsigned integer in [0, 255]"
        self._mocap_poe_power_ctrl_req = value

    @builtins.property
    def ipad_power_ctrl_req(self):
        """Message field 'ipad_power_ctrl_req'."""
        return self._ipad_power_ctrl_req

    @ipad_power_ctrl_req.setter
    def ipad_power_ctrl_req(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'ipad_power_ctrl_req' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'ipad_power_ctrl_req' field must be an unsigned integer in [0, 255]"
        self._ipad_power_ctrl_req = value

    @builtins.property
    def chest_reserved_lidar_power_ctrl_req(self):
        """Message field 'chest_reserved_lidar_power_ctrl_req'."""
        return self._chest_reserved_lidar_power_ctrl_req

    @chest_reserved_lidar_power_ctrl_req.setter
    def chest_reserved_lidar_power_ctrl_req(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'chest_reserved_lidar_power_ctrl_req' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'chest_reserved_lidar_power_ctrl_req' field must be an unsigned integer in [0, 255]"
        self._chest_reserved_lidar_power_ctrl_req = value
