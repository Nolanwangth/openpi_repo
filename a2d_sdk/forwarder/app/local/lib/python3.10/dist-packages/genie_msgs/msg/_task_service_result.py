# generated from rosidl_generator_py/resource/_idl.py.em
# with input from genie_msgs:msg/TaskServiceResult.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_TaskServiceResult(type):
    """Metaclass of message 'TaskServiceResult'."""

    _CREATE_ROS_MESSAGE = None
    _CONVERT_FROM_PY = None
    _CONVERT_TO_PY = None
    _DESTROY_ROS_MESSAGE = None
    _TYPE_SUPPORT = None

    __constants = {
        'TASK_SERVICE_RESULT_SUCCESS': 0,
        'TASK_SERVICE_RESULT_FAIL': 1,
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
                'genie_msgs.msg.TaskServiceResult')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__task_service_result
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__task_service_result
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__task_service_result
            cls._TYPE_SUPPORT = module.type_support_msg__msg__task_service_result
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__task_service_result

            from genie_msgs.msg import TaskState
            if TaskState.__class__._TYPE_SUPPORT is None:
                TaskState.__class__.__import_type_support__()

    @classmethod
    def __prepare__(cls, name, bases, **kwargs):
        # list constant names here so that they appear in the help text of
        # the message class under "Data and other attributes defined here:"
        # as well as populate each message instance
        return {
            'TASK_SERVICE_RESULT_SUCCESS': cls.__constants['TASK_SERVICE_RESULT_SUCCESS'],
            'TASK_SERVICE_RESULT_FAIL': cls.__constants['TASK_SERVICE_RESULT_FAIL'],
        }

    @property
    def TASK_SERVICE_RESULT_SUCCESS(self):
        """Message constant 'TASK_SERVICE_RESULT_SUCCESS'."""
        return Metaclass_TaskServiceResult.__constants['TASK_SERVICE_RESULT_SUCCESS']

    @property
    def TASK_SERVICE_RESULT_FAIL(self):
        """Message constant 'TASK_SERVICE_RESULT_FAIL'."""
        return Metaclass_TaskServiceResult.__constants['TASK_SERVICE_RESULT_FAIL']


class TaskServiceResult(metaclass=Metaclass_TaskServiceResult):
    """
    Message class 'TaskServiceResult'.

    Constants:
      TASK_SERVICE_RESULT_SUCCESS
      TASK_SERVICE_RESULT_FAIL
    """

    __slots__ = [
        '_result',
        '_id',
        '_task_state',
        '_error_code',
        '_state',
        '_message',
    ]

    _fields_and_field_types = {
        'result': 'uint8',
        'id': 'uint32',
        'task_state': 'genie_msgs/TaskState',
        'error_code': 'uint32',
        'state': 'genie_msgs/TaskState',
        'message': 'string',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint32'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['genie_msgs', 'msg'], 'TaskState'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint32'),  # noqa: E501
        rosidl_parser.definition.NamespacedType(['genie_msgs', 'msg'], 'TaskState'),  # noqa: E501
        rosidl_parser.definition.UnboundedString(),  # noqa: E501
    )

    def __init__(self, **kwargs):
        assert all('_' + key in self.__slots__ for key in kwargs.keys()), \
            'Invalid arguments passed to constructor: %s' % \
            ', '.join(sorted(k for k in kwargs.keys() if '_' + k not in self.__slots__))
        self.result = kwargs.get('result', int())
        self.id = kwargs.get('id', int())
        from genie_msgs.msg import TaskState
        self.task_state = kwargs.get('task_state', TaskState())
        self.error_code = kwargs.get('error_code', int())
        from genie_msgs.msg import TaskState
        self.state = kwargs.get('state', TaskState())
        self.message = kwargs.get('message', str())

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
        if self.result != other.result:
            return False
        if self.id != other.id:
            return False
        if self.task_state != other.task_state:
            return False
        if self.error_code != other.error_code:
            return False
        if self.state != other.state:
            return False
        if self.message != other.message:
            return False
        return True

    @classmethod
    def get_fields_and_field_types(cls):
        from copy import copy
        return copy(cls._fields_and_field_types)

    @builtins.property
    def result(self):
        """Message field 'result'."""
        return self._result

    @result.setter
    def result(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'result' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'result' field must be an unsigned integer in [0, 255]"
        self._result = value

    @builtins.property  # noqa: A003
    def id(self):  # noqa: A003
        """Message field 'id'."""
        return self._id

    @id.setter  # noqa: A003
    def id(self, value):  # noqa: A003
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'id' field must be of type 'int'"
            assert value >= 0 and value < 4294967296, \
                "The 'id' field must be an unsigned integer in [0, 4294967295]"
        self._id = value

    @builtins.property
    def task_state(self):
        """Message field 'task_state'."""
        return self._task_state

    @task_state.setter
    def task_state(self, value):
        if __debug__:
            from genie_msgs.msg import TaskState
            assert \
                isinstance(value, TaskState), \
                "The 'task_state' field must be a sub message of type 'TaskState'"
        self._task_state = value

    @builtins.property
    def error_code(self):
        """Message field 'error_code'."""
        return self._error_code

    @error_code.setter
    def error_code(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'error_code' field must be of type 'int'"
            assert value >= 0 and value < 4294967296, \
                "The 'error_code' field must be an unsigned integer in [0, 4294967295]"
        self._error_code = value

    @builtins.property
    def state(self):
        """Message field 'state'."""
        return self._state

    @state.setter
    def state(self, value):
        if __debug__:
            from genie_msgs.msg import TaskState
            assert \
                isinstance(value, TaskState), \
                "The 'state' field must be a sub message of type 'TaskState'"
        self._state = value

    @builtins.property
    def message(self):
        """Message field 'message'."""
        return self._message

    @message.setter
    def message(self, value):
        if __debug__:
            assert \
                isinstance(value, str), \
                "The 'message' field must be of type 'str'"
        self._message = value
