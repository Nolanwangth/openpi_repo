# generated from rosidl_generator_py/resource/_idl.py.em
# with input from genie_msgs:msg/ChassisSensors.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_ChassisSensors(type):
    """Metaclass of message 'ChassisSensors'."""

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
                'genie_msgs.msg.ChassisSensors')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__chassis_sensors
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__chassis_sensors
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__chassis_sensors
            cls._TYPE_SUPPORT = module.type_support_msg__msg__chassis_sensors
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__chassis_sensors

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


class ChassisSensors(metaclass=Metaclass_ChassisSensors):
    """Message class 'ChassisSensors'."""

    __slots__ = [
        '_header',
        '_chassis_ultrasonic_radar1_distance',
        '_chassis_ultrasonic_radar2_distance',
        '_chassis_ultrasonic_radar3_distance',
        '_chassis_ultrasonic_radar4_distance',
        '_chassis_ultrasonic_radar5_distance',
        '_chassis_ultrasonic_radar6_distance',
        '_chassis_ultrasonic_radar7_distance',
        '_chassis_ultrasonic_radar1_fault_state',
        '_chassis_ultrasonic_radar2_fault_state',
        '_chassis_ultrasonic_radar3_fault_state',
        '_chassis_ultrasonic_radar4_fault_state',
        '_chassis_ultrasonic_radar5_fault_state',
        '_chassis_ultrasonic_radar6_fault_state',
        '_chassis_ultrasonic_radar7_fault_state',
    ]

    _fields_and_field_types = {
        'header': 'std_msgs/Header',
        'chassis_ultrasonic_radar1_distance': 'uint32',
        'chassis_ultrasonic_radar2_distance': 'uint32',
        'chassis_ultrasonic_radar3_distance': 'uint32',
        'chassis_ultrasonic_radar4_distance': 'uint32',
        'chassis_ultrasonic_radar5_distance': 'uint32',
        'chassis_ultrasonic_radar6_distance': 'uint32',
        'chassis_ultrasonic_radar7_distance': 'uint32',
        'chassis_ultrasonic_radar1_fault_state': 'uint8',
        'chassis_ultrasonic_radar2_fault_state': 'uint8',
        'chassis_ultrasonic_radar3_fault_state': 'uint8',
        'chassis_ultrasonic_radar4_fault_state': 'uint8',
        'chassis_ultrasonic_radar5_fault_state': 'uint8',
        'chassis_ultrasonic_radar6_fault_state': 'uint8',
        'chassis_ultrasonic_radar7_fault_state': 'uint8',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.NamespacedType(['std_msgs', 'msg'], 'Header'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint32'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint32'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint32'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint32'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint32'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint32'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint32'),  # noqa: E501
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
        self.chassis_ultrasonic_radar1_distance = kwargs.get('chassis_ultrasonic_radar1_distance', int())
        self.chassis_ultrasonic_radar2_distance = kwargs.get('chassis_ultrasonic_radar2_distance', int())
        self.chassis_ultrasonic_radar3_distance = kwargs.get('chassis_ultrasonic_radar3_distance', int())
        self.chassis_ultrasonic_radar4_distance = kwargs.get('chassis_ultrasonic_radar4_distance', int())
        self.chassis_ultrasonic_radar5_distance = kwargs.get('chassis_ultrasonic_radar5_distance', int())
        self.chassis_ultrasonic_radar6_distance = kwargs.get('chassis_ultrasonic_radar6_distance', int())
        self.chassis_ultrasonic_radar7_distance = kwargs.get('chassis_ultrasonic_radar7_distance', int())
        self.chassis_ultrasonic_radar1_fault_state = kwargs.get('chassis_ultrasonic_radar1_fault_state', int())
        self.chassis_ultrasonic_radar2_fault_state = kwargs.get('chassis_ultrasonic_radar2_fault_state', int())
        self.chassis_ultrasonic_radar3_fault_state = kwargs.get('chassis_ultrasonic_radar3_fault_state', int())
        self.chassis_ultrasonic_radar4_fault_state = kwargs.get('chassis_ultrasonic_radar4_fault_state', int())
        self.chassis_ultrasonic_radar5_fault_state = kwargs.get('chassis_ultrasonic_radar5_fault_state', int())
        self.chassis_ultrasonic_radar6_fault_state = kwargs.get('chassis_ultrasonic_radar6_fault_state', int())
        self.chassis_ultrasonic_radar7_fault_state = kwargs.get('chassis_ultrasonic_radar7_fault_state', int())

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
        if self.chassis_ultrasonic_radar1_distance != other.chassis_ultrasonic_radar1_distance:
            return False
        if self.chassis_ultrasonic_radar2_distance != other.chassis_ultrasonic_radar2_distance:
            return False
        if self.chassis_ultrasonic_radar3_distance != other.chassis_ultrasonic_radar3_distance:
            return False
        if self.chassis_ultrasonic_radar4_distance != other.chassis_ultrasonic_radar4_distance:
            return False
        if self.chassis_ultrasonic_radar5_distance != other.chassis_ultrasonic_radar5_distance:
            return False
        if self.chassis_ultrasonic_radar6_distance != other.chassis_ultrasonic_radar6_distance:
            return False
        if self.chassis_ultrasonic_radar7_distance != other.chassis_ultrasonic_radar7_distance:
            return False
        if self.chassis_ultrasonic_radar1_fault_state != other.chassis_ultrasonic_radar1_fault_state:
            return False
        if self.chassis_ultrasonic_radar2_fault_state != other.chassis_ultrasonic_radar2_fault_state:
            return False
        if self.chassis_ultrasonic_radar3_fault_state != other.chassis_ultrasonic_radar3_fault_state:
            return False
        if self.chassis_ultrasonic_radar4_fault_state != other.chassis_ultrasonic_radar4_fault_state:
            return False
        if self.chassis_ultrasonic_radar5_fault_state != other.chassis_ultrasonic_radar5_fault_state:
            return False
        if self.chassis_ultrasonic_radar6_fault_state != other.chassis_ultrasonic_radar6_fault_state:
            return False
        if self.chassis_ultrasonic_radar7_fault_state != other.chassis_ultrasonic_radar7_fault_state:
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
    def chassis_ultrasonic_radar1_distance(self):
        """Message field 'chassis_ultrasonic_radar1_distance'."""
        return self._chassis_ultrasonic_radar1_distance

    @chassis_ultrasonic_radar1_distance.setter
    def chassis_ultrasonic_radar1_distance(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'chassis_ultrasonic_radar1_distance' field must be of type 'int'"
            assert value >= 0 and value < 4294967296, \
                "The 'chassis_ultrasonic_radar1_distance' field must be an unsigned integer in [0, 4294967295]"
        self._chassis_ultrasonic_radar1_distance = value

    @builtins.property
    def chassis_ultrasonic_radar2_distance(self):
        """Message field 'chassis_ultrasonic_radar2_distance'."""
        return self._chassis_ultrasonic_radar2_distance

    @chassis_ultrasonic_radar2_distance.setter
    def chassis_ultrasonic_radar2_distance(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'chassis_ultrasonic_radar2_distance' field must be of type 'int'"
            assert value >= 0 and value < 4294967296, \
                "The 'chassis_ultrasonic_radar2_distance' field must be an unsigned integer in [0, 4294967295]"
        self._chassis_ultrasonic_radar2_distance = value

    @builtins.property
    def chassis_ultrasonic_radar3_distance(self):
        """Message field 'chassis_ultrasonic_radar3_distance'."""
        return self._chassis_ultrasonic_radar3_distance

    @chassis_ultrasonic_radar3_distance.setter
    def chassis_ultrasonic_radar3_distance(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'chassis_ultrasonic_radar3_distance' field must be of type 'int'"
            assert value >= 0 and value < 4294967296, \
                "The 'chassis_ultrasonic_radar3_distance' field must be an unsigned integer in [0, 4294967295]"
        self._chassis_ultrasonic_radar3_distance = value

    @builtins.property
    def chassis_ultrasonic_radar4_distance(self):
        """Message field 'chassis_ultrasonic_radar4_distance'."""
        return self._chassis_ultrasonic_radar4_distance

    @chassis_ultrasonic_radar4_distance.setter
    def chassis_ultrasonic_radar4_distance(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'chassis_ultrasonic_radar4_distance' field must be of type 'int'"
            assert value >= 0 and value < 4294967296, \
                "The 'chassis_ultrasonic_radar4_distance' field must be an unsigned integer in [0, 4294967295]"
        self._chassis_ultrasonic_radar4_distance = value

    @builtins.property
    def chassis_ultrasonic_radar5_distance(self):
        """Message field 'chassis_ultrasonic_radar5_distance'."""
        return self._chassis_ultrasonic_radar5_distance

    @chassis_ultrasonic_radar5_distance.setter
    def chassis_ultrasonic_radar5_distance(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'chassis_ultrasonic_radar5_distance' field must be of type 'int'"
            assert value >= 0 and value < 4294967296, \
                "The 'chassis_ultrasonic_radar5_distance' field must be an unsigned integer in [0, 4294967295]"
        self._chassis_ultrasonic_radar5_distance = value

    @builtins.property
    def chassis_ultrasonic_radar6_distance(self):
        """Message field 'chassis_ultrasonic_radar6_distance'."""
        return self._chassis_ultrasonic_radar6_distance

    @chassis_ultrasonic_radar6_distance.setter
    def chassis_ultrasonic_radar6_distance(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'chassis_ultrasonic_radar6_distance' field must be of type 'int'"
            assert value >= 0 and value < 4294967296, \
                "The 'chassis_ultrasonic_radar6_distance' field must be an unsigned integer in [0, 4294967295]"
        self._chassis_ultrasonic_radar6_distance = value

    @builtins.property
    def chassis_ultrasonic_radar7_distance(self):
        """Message field 'chassis_ultrasonic_radar7_distance'."""
        return self._chassis_ultrasonic_radar7_distance

    @chassis_ultrasonic_radar7_distance.setter
    def chassis_ultrasonic_radar7_distance(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'chassis_ultrasonic_radar7_distance' field must be of type 'int'"
            assert value >= 0 and value < 4294967296, \
                "The 'chassis_ultrasonic_radar7_distance' field must be an unsigned integer in [0, 4294967295]"
        self._chassis_ultrasonic_radar7_distance = value

    @builtins.property
    def chassis_ultrasonic_radar1_fault_state(self):
        """Message field 'chassis_ultrasonic_radar1_fault_state'."""
        return self._chassis_ultrasonic_radar1_fault_state

    @chassis_ultrasonic_radar1_fault_state.setter
    def chassis_ultrasonic_radar1_fault_state(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'chassis_ultrasonic_radar1_fault_state' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'chassis_ultrasonic_radar1_fault_state' field must be an unsigned integer in [0, 255]"
        self._chassis_ultrasonic_radar1_fault_state = value

    @builtins.property
    def chassis_ultrasonic_radar2_fault_state(self):
        """Message field 'chassis_ultrasonic_radar2_fault_state'."""
        return self._chassis_ultrasonic_radar2_fault_state

    @chassis_ultrasonic_radar2_fault_state.setter
    def chassis_ultrasonic_radar2_fault_state(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'chassis_ultrasonic_radar2_fault_state' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'chassis_ultrasonic_radar2_fault_state' field must be an unsigned integer in [0, 255]"
        self._chassis_ultrasonic_radar2_fault_state = value

    @builtins.property
    def chassis_ultrasonic_radar3_fault_state(self):
        """Message field 'chassis_ultrasonic_radar3_fault_state'."""
        return self._chassis_ultrasonic_radar3_fault_state

    @chassis_ultrasonic_radar3_fault_state.setter
    def chassis_ultrasonic_radar3_fault_state(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'chassis_ultrasonic_radar3_fault_state' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'chassis_ultrasonic_radar3_fault_state' field must be an unsigned integer in [0, 255]"
        self._chassis_ultrasonic_radar3_fault_state = value

    @builtins.property
    def chassis_ultrasonic_radar4_fault_state(self):
        """Message field 'chassis_ultrasonic_radar4_fault_state'."""
        return self._chassis_ultrasonic_radar4_fault_state

    @chassis_ultrasonic_radar4_fault_state.setter
    def chassis_ultrasonic_radar4_fault_state(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'chassis_ultrasonic_radar4_fault_state' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'chassis_ultrasonic_radar4_fault_state' field must be an unsigned integer in [0, 255]"
        self._chassis_ultrasonic_radar4_fault_state = value

    @builtins.property
    def chassis_ultrasonic_radar5_fault_state(self):
        """Message field 'chassis_ultrasonic_radar5_fault_state'."""
        return self._chassis_ultrasonic_radar5_fault_state

    @chassis_ultrasonic_radar5_fault_state.setter
    def chassis_ultrasonic_radar5_fault_state(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'chassis_ultrasonic_radar5_fault_state' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'chassis_ultrasonic_radar5_fault_state' field must be an unsigned integer in [0, 255]"
        self._chassis_ultrasonic_radar5_fault_state = value

    @builtins.property
    def chassis_ultrasonic_radar6_fault_state(self):
        """Message field 'chassis_ultrasonic_radar6_fault_state'."""
        return self._chassis_ultrasonic_radar6_fault_state

    @chassis_ultrasonic_radar6_fault_state.setter
    def chassis_ultrasonic_radar6_fault_state(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'chassis_ultrasonic_radar6_fault_state' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'chassis_ultrasonic_radar6_fault_state' field must be an unsigned integer in [0, 255]"
        self._chassis_ultrasonic_radar6_fault_state = value

    @builtins.property
    def chassis_ultrasonic_radar7_fault_state(self):
        """Message field 'chassis_ultrasonic_radar7_fault_state'."""
        return self._chassis_ultrasonic_radar7_fault_state

    @chassis_ultrasonic_radar7_fault_state.setter
    def chassis_ultrasonic_radar7_fault_state(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'chassis_ultrasonic_radar7_fault_state' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'chassis_ultrasonic_radar7_fault_state' field must be an unsigned integer in [0, 255]"
        self._chassis_ultrasonic_radar7_fault_state = value
