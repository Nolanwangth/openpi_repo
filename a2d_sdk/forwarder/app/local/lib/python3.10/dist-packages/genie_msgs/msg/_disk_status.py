# generated from rosidl_generator_py/resource/_idl.py.em
# with input from genie_msgs:msg/DiskStatus.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import math  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_DiskStatus(type):
    """Metaclass of message 'DiskStatus'."""

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
                'genie_msgs.msg.DiskStatus')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__disk_status
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__disk_status
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__disk_status
            cls._TYPE_SUPPORT = module.type_support_msg__msg__disk_status
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__disk_status

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


class DiskStatus(metaclass=Metaclass_DiskStatus):
    """Message class 'DiskStatus'."""

    __slots__ = [
        '_header',
        '_name',
        '_total_capacity_mb',
        '_used_capacity_mb',
        '_available_capacity_mb',
        '_usage_ratio',
        '_mounted',
        '_mount_point',
    ]

    _fields_and_field_types = {
        'header': 'std_msgs/Header',
        'name': 'string',
        'total_capacity_mb': 'uint64',
        'used_capacity_mb': 'uint64',
        'available_capacity_mb': 'uint64',
        'usage_ratio': 'float',
        'mounted': 'boolean',
        'mount_point': 'string',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.NamespacedType(['std_msgs', 'msg'], 'Header'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.BasicType('uint64'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint64'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint64'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        from std_msgs.msg import Header
        self.header = kwargs.get('header', Header())
        self.name = kwargs.get('name', str())
        self.total_capacity_mb = kwargs.get('total_capacity_mb', int())
        self.used_capacity_mb = kwargs.get('used_capacity_mb', int())
        self.available_capacity_mb = kwargs.get('available_capacity_mb', int())
        self.usage_ratio = kwargs.get('usage_ratio', float())
        self.mounted = kwargs.get('mounted', bool())
        self.mount_point = kwargs.get('mount_point', str())

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
        if self.name != other.name:
            return False
        if self.total_capacity_mb != other.total_capacity_mb:
            return False
        if self.used_capacity_mb != other.used_capacity_mb:
            return False
        if self.available_capacity_mb != other.available_capacity_mb:
            return False
        if self.usage_ratio != other.usage_ratio:
            return False
        if self.mounted != other.mounted:
            return False
        if self.mount_point != other.mount_point:
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
    def name(self):
        """Message field 'name'."""
        return self._name

    @name.setter
    def name(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'name' field must be of type 'str'"
        self._name = value

    @builtins.property
    def total_capacity_mb(self):
        """Message field 'total_capacity_mb'."""
        return self._total_capacity_mb

    @total_capacity_mb.setter
    def total_capacity_mb(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'total_capacity_mb' field must be of type 'int'"
            assert value >= 0 and value < 18446744073709551616, \
                "The 'total_capacity_mb' field must be an unsigned integer in [0, 18446744073709551615]"
        self._total_capacity_mb = value

    @builtins.property
    def used_capacity_mb(self):
        """Message field 'used_capacity_mb'."""
        return self._used_capacity_mb

    @used_capacity_mb.setter
    def used_capacity_mb(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'used_capacity_mb' field must be of type 'int'"
            assert value >= 0 and value < 18446744073709551616, \
                "The 'used_capacity_mb' field must be an unsigned integer in [0, 18446744073709551615]"
        self._used_capacity_mb = value

    @builtins.property
    def available_capacity_mb(self):
        """Message field 'available_capacity_mb'."""
        return self._available_capacity_mb

    @available_capacity_mb.setter
    def available_capacity_mb(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'available_capacity_mb' field must be of type 'int'"
            assert value >= 0 and value < 18446744073709551616, \
                "The 'available_capacity_mb' field must be an unsigned integer in [0, 18446744073709551615]"
        self._available_capacity_mb = value

    @builtins.property
    def usage_ratio(self):
        """Message field 'usage_ratio'."""
        return self._usage_ratio

    @usage_ratio.setter
    def usage_ratio(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'usage_ratio' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'usage_ratio' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._usage_ratio = value

    @builtins.property
    def mounted(self):
        """Message field 'mounted'."""
        return self._mounted

    @mounted.setter
    def mounted(self, value):
        if __debug__:
            assert \
                isinstance(value, bool), \
                "The 'mounted' field must be of type 'bool'"
        self._mounted = value

    @builtins.property
    def mount_point(self):
        """Message field 'mount_point'."""
        return self._mount_point

    @mount_point.setter
    def mount_point(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'mount_point' field must be of type 'str'"
        self._mount_point = value
