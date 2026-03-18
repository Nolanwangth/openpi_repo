# generated from rosidl_generator_py/resource/_idl.py.em
# with input from genie_msgs:msg/InteractiveSettingRequest.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_InteractiveSettingRequest(type):
    """Metaclass of message 'InteractiveSettingRequest'."""

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
                'genie_msgs.msg.InteractiveSettingRequest')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__interactive_setting_request
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__interactive_setting_request
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__interactive_setting_request
            cls._TYPE_SUPPORT = module.type_support_msg__msg__interactive_setting_request
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__interactive_setting_request

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


class InteractiveSettingRequest(metaclass=Metaclass_InteractiveSettingRequest):
    """Message class 'InteractiveSettingRequest'."""

    __slots__ = [
        '_header',
        '_voice_output_switch',
        '_volume',
        '_voice_control_switch',
        '_voice_language',
        '_voice_style',
        '_audio_alarm_switch',
        '_interactive_screen_switch',
        '_brightness',
        '_uuid',
        '_detail',
    ]

    _fields_and_field_types = {
        'header': 'std_msgs/Header',
        'voice_output_switch': 'boolean',
        'volume': 'uint8',
        'voice_control_switch': 'boolean',
        'voice_language': 'string',
        'voice_style': 'string',
        'audio_alarm_switch': 'boolean',
        'interactive_screen_switch': 'boolean',
        'brightness': 'uint8',
        'uuid': 'string',
        'detail': 'string',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.NamespacedType(['std_msgs', 'msg'], 'Header'),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.BasicType('boolean'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        from std_msgs.msg import Header
        self.header = kwargs.get('header', Header())
        self.voice_output_switch = kwargs.get('voice_output_switch', bool())
        self.volume = kwargs.get('volume', int())
        self.voice_control_switch = kwargs.get('voice_control_switch', bool())
        self.voice_language = kwargs.get('voice_language', str())
        self.voice_style = kwargs.get('voice_style', str())
        self.audio_alarm_switch = kwargs.get('audio_alarm_switch', bool())
        self.interactive_screen_switch = kwargs.get('interactive_screen_switch', bool())
        self.brightness = kwargs.get('brightness', int())
        self.uuid = kwargs.get('uuid', str())
        self.detail = kwargs.get('detail', str())

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
        if self.voice_output_switch != other.voice_output_switch:
            return False
        if self.volume != other.volume:
            return False
        if self.voice_control_switch != other.voice_control_switch:
            return False
        if self.voice_language != other.voice_language:
            return False
        if self.voice_style != other.voice_style:
            return False
        if self.audio_alarm_switch != other.audio_alarm_switch:
            return False
        if self.interactive_screen_switch != other.interactive_screen_switch:
            return False
        if self.brightness != other.brightness:
            return False
        if self.uuid != other.uuid:
            return False
        if self.detail != other.detail:
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
    def voice_output_switch(self):
        """Message field 'voice_output_switch'."""
        return self._voice_output_switch

    @voice_output_switch.setter
    def voice_output_switch(self, value):
        if __debug__:
            assert \
                isinstance(value, bool), \
                "The 'voice_output_switch' field must be of type 'bool'"
        self._voice_output_switch = value

    @builtins.property
    def volume(self):
        """Message field 'volume'."""
        return self._volume

    @volume.setter
    def volume(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'volume' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'volume' field must be an unsigned integer in [0, 255]"
        self._volume = value

    @builtins.property
    def voice_control_switch(self):
        """Message field 'voice_control_switch'."""
        return self._voice_control_switch

    @voice_control_switch.setter
    def voice_control_switch(self, value):
        if __debug__:
            assert \
                isinstance(value, bool), \
                "The 'voice_control_switch' field must be of type 'bool'"
        self._voice_control_switch = value

    @builtins.property
    def voice_language(self):
        """Message field 'voice_language'."""
        return self._voice_language

    @voice_language.setter
    def voice_language(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'voice_language' field must be of type 'str'"
        self._voice_language = value

    @builtins.property
    def voice_style(self):
        """Message field 'voice_style'."""
        return self._voice_style

    @voice_style.setter
    def voice_style(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'voice_style' field must be of type 'str'"
        self._voice_style = value

    @builtins.property
    def audio_alarm_switch(self):
        """Message field 'audio_alarm_switch'."""
        return self._audio_alarm_switch

    @audio_alarm_switch.setter
    def audio_alarm_switch(self, value):
        if __debug__:
            assert \
                isinstance(value, bool), \
                "The 'audio_alarm_switch' field must be of type 'bool'"
        self._audio_alarm_switch = value

    @builtins.property
    def interactive_screen_switch(self):
        """Message field 'interactive_screen_switch'."""
        return self._interactive_screen_switch

    @interactive_screen_switch.setter
    def interactive_screen_switch(self, value):
        if __debug__:
            assert \
                isinstance(value, bool), \
                "The 'interactive_screen_switch' field must be of type 'bool'"
        self._interactive_screen_switch = value

    @builtins.property
    def brightness(self):
        """Message field 'brightness'."""
        return self._brightness

    @brightness.setter
    def brightness(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'brightness' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'brightness' field must be an unsigned integer in [0, 255]"
        self._brightness = value

    @builtins.property
    def uuid(self):
        """Message field 'uuid'."""
        return self._uuid

    @uuid.setter
    def uuid(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'uuid' field must be of type 'str'"
        self._uuid = value

    @builtins.property
    def detail(self):
        """Message field 'detail'."""
        return self._detail

    @detail.setter
    def detail(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'detail' field must be of type 'str'"
        self._detail = value
