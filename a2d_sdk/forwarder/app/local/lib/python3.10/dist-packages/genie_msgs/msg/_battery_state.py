# generated from rosidl_generator_py/resource/_idl.py.em
# with input from genie_msgs:msg/BatteryState.idl
# generated code does not contain a copyright notice


# Import statements for member types

import builtins  # noqa: E402, I100

import math  # noqa: E402, I100

import rosidl_parser.definition  # noqa: E402, I100


class Metaclass_BatteryState(type):
    """Metaclass of message 'BatteryState'."""

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
                'genie_msgs.msg.BatteryState')
            logger.debug(
                'Failed to import needed modules for type support:\n' +
                traceback.format_exc())
        else:
            cls._CREATE_ROS_MESSAGE = module.create_ros_message_msg__msg__battery_state
            cls._CONVERT_FROM_PY = module.convert_from_py_msg__msg__battery_state
            cls._CONVERT_TO_PY = module.convert_to_py_msg__msg__battery_state
            cls._TYPE_SUPPORT = module.type_support_msg__msg__battery_state
            cls._DESTROY_ROS_MESSAGE = module.destroy_ros_message_msg__msg__battery_state

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


class BatteryState(metaclass=Metaclass_BatteryState):
    """Message class 'BatteryState'."""

    __slots__ = [
        '_header',
        '_battery1_bms_charge_or_discharge',
        '_battery2_bms_charge_or_discharge',
        '_battery1_bms_output_voltage',
        '_battery2_bms_output_voltage',
        '_battery1_bms_output_current',
        '_battery2_bms_output_current',
        '_battery1_bms_charge_current',
        '_battery2_bms_charge_current',
        '_battery1_bms_temperature',
        '_battery2_bms_temperature',
        '_battery1_bms_soc',
        '_battery2_bms_soc',
        '_battery1_bms_soh',
        '_battery2_bms_soh',
        '_battery1_bms_short_circuit_fault_state',
        '_battery2_bms_short_circuit_fault_state',
        '_battery1_bms_open_circuit_fault_state',
        '_battery2_bms_open_circuit_fault_state',
        '_battery1_bms_other_fault_state',
        '_battery2_bms_other_fault_state',
        '_battery1_outside_output_voltage',
        '_battery2_outside_output_voltage',
        '_battery1_outside_connection',
        '_battery1_outside_open_circuit_fault_state',
        '_battery2_outside_connection',
        '_battery2_outside_open_circuit_fault_state',
        '_charge_plug_input_voltage',
        '_charge_plug_input_current',
        '_charge_plug_input_short_circuit_fault_state',
        '_charge_plug_input_open_circuit_fault_state',
        '_chassis_power_board_fault_state',
        '_power_board_software_version',
        '_power_board_hardware_version',
        '_power_board_serial_number',
    ]

    _fields_and_field_types = {
        'header': 'std_msgs/Header',
        'battery1_bms_charge_or_discharge': 'uint8',
        'battery2_bms_charge_or_discharge': 'uint8',
        'battery1_bms_output_voltage': 'float',
        'battery2_bms_output_voltage': 'float',
        'battery1_bms_output_current': 'float',
        'battery2_bms_output_current': 'float',
        'battery1_bms_charge_current': 'float',
        'battery2_bms_charge_current': 'float',
        'battery1_bms_temperature': 'float',
        'battery2_bms_temperature': 'float',
        'battery1_bms_soc': 'float',
        'battery2_bms_soc': 'float',
        'battery1_bms_soh': 'uint8',
        'battery2_bms_soh': 'uint8',
        'battery1_bms_short_circuit_fault_state': 'uint8',
        'battery2_bms_short_circuit_fault_state': 'uint8',
        'battery1_bms_open_circuit_fault_state': 'uint8',
        'battery2_bms_open_circuit_fault_state': 'uint8',
        'battery1_bms_other_fault_state': 'uint32',
        'battery2_bms_other_fault_state': 'uint32',
        'battery1_outside_output_voltage': 'float',
        'battery2_outside_output_voltage': 'float',
        'battery1_outside_connection': 'uint8',
        'battery1_outside_open_circuit_fault_state': 'uint8',
        'battery2_outside_connection': 'uint8',
        'battery2_outside_open_circuit_fault_state': 'uint8',
        'charge_plug_input_voltage': 'float',
        'charge_plug_input_current': 'float',
        'charge_plug_input_short_circuit_fault_state': 'uint8',
        'charge_plug_input_open_circuit_fault_state': 'uint8',
        'chassis_power_board_fault_state': 'uint8',
        'power_board_software_version': 'string',
        'power_board_hardware_version': 'string',
        'power_board_serial_number': 'string',
    }

    SLOT_TYPES = (
        rosidl_parser.definition.NamespacedType(['std_msgs', 'msg'], 'Header'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint32'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint32'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('float'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
        rosidl_parser.definition.BasicType('uint8'),  # noqa: E501
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
        self.battery1_bms_charge_or_discharge = kwargs.get('battery1_bms_charge_or_discharge', int())
        self.battery2_bms_charge_or_discharge = kwargs.get('battery2_bms_charge_or_discharge', int())
        self.battery1_bms_output_voltage = kwargs.get('battery1_bms_output_voltage', float())
        self.battery2_bms_output_voltage = kwargs.get('battery2_bms_output_voltage', float())
        self.battery1_bms_output_current = kwargs.get('battery1_bms_output_current', float())
        self.battery2_bms_output_current = kwargs.get('battery2_bms_output_current', float())
        self.battery1_bms_charge_current = kwargs.get('battery1_bms_charge_current', float())
        self.battery2_bms_charge_current = kwargs.get('battery2_bms_charge_current', float())
        self.battery1_bms_temperature = kwargs.get('battery1_bms_temperature', float())
        self.battery2_bms_temperature = kwargs.get('battery2_bms_temperature', float())
        self.battery1_bms_soc = kwargs.get('battery1_bms_soc', float())
        self.battery2_bms_soc = kwargs.get('battery2_bms_soc', float())
        self.battery1_bms_soh = kwargs.get('battery1_bms_soh', int())
        self.battery2_bms_soh = kwargs.get('battery2_bms_soh', int())
        self.battery1_bms_short_circuit_fault_state = kwargs.get('battery1_bms_short_circuit_fault_state', int())
        self.battery2_bms_short_circuit_fault_state = kwargs.get('battery2_bms_short_circuit_fault_state', int())
        self.battery1_bms_open_circuit_fault_state = kwargs.get('battery1_bms_open_circuit_fault_state', int())
        self.battery2_bms_open_circuit_fault_state = kwargs.get('battery2_bms_open_circuit_fault_state', int())
        self.battery1_bms_other_fault_state = kwargs.get('battery1_bms_other_fault_state', int())
        self.battery2_bms_other_fault_state = kwargs.get('battery2_bms_other_fault_state', int())
        self.battery1_outside_output_voltage = kwargs.get('battery1_outside_output_voltage', float())
        self.battery2_outside_output_voltage = kwargs.get('battery2_outside_output_voltage', float())
        self.battery1_outside_connection = kwargs.get('battery1_outside_connection', int())
        self.battery1_outside_open_circuit_fault_state = kwargs.get('battery1_outside_open_circuit_fault_state', int())
        self.battery2_outside_connection = kwargs.get('battery2_outside_connection', int())
        self.battery2_outside_open_circuit_fault_state = kwargs.get('battery2_outside_open_circuit_fault_state', int())
        self.charge_plug_input_voltage = kwargs.get('charge_plug_input_voltage', float())
        self.charge_plug_input_current = kwargs.get('charge_plug_input_current', float())
        self.charge_plug_input_short_circuit_fault_state = kwargs.get('charge_plug_input_short_circuit_fault_state', int())
        self.charge_plug_input_open_circuit_fault_state = kwargs.get('charge_plug_input_open_circuit_fault_state', int())
        self.chassis_power_board_fault_state = kwargs.get('chassis_power_board_fault_state', int())
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
        if self.battery1_bms_charge_or_discharge != other.battery1_bms_charge_or_discharge:
            return False
        if self.battery2_bms_charge_or_discharge != other.battery2_bms_charge_or_discharge:
            return False
        if self.battery1_bms_output_voltage != other.battery1_bms_output_voltage:
            return False
        if self.battery2_bms_output_voltage != other.battery2_bms_output_voltage:
            return False
        if self.battery1_bms_output_current != other.battery1_bms_output_current:
            return False
        if self.battery2_bms_output_current != other.battery2_bms_output_current:
            return False
        if self.battery1_bms_charge_current != other.battery1_bms_charge_current:
            return False
        if self.battery2_bms_charge_current != other.battery2_bms_charge_current:
            return False
        if self.battery1_bms_temperature != other.battery1_bms_temperature:
            return False
        if self.battery2_bms_temperature != other.battery2_bms_temperature:
            return False
        if self.battery1_bms_soc != other.battery1_bms_soc:
            return False
        if self.battery2_bms_soc != other.battery2_bms_soc:
            return False
        if self.battery1_bms_soh != other.battery1_bms_soh:
            return False
        if self.battery2_bms_soh != other.battery2_bms_soh:
            return False
        if self.battery1_bms_short_circuit_fault_state != other.battery1_bms_short_circuit_fault_state:
            return False
        if self.battery2_bms_short_circuit_fault_state != other.battery2_bms_short_circuit_fault_state:
            return False
        if self.battery1_bms_open_circuit_fault_state != other.battery1_bms_open_circuit_fault_state:
            return False
        if self.battery2_bms_open_circuit_fault_state != other.battery2_bms_open_circuit_fault_state:
            return False
        if self.battery1_bms_other_fault_state != other.battery1_bms_other_fault_state:
            return False
        if self.battery2_bms_other_fault_state != other.battery2_bms_other_fault_state:
            return False
        if self.battery1_outside_output_voltage != other.battery1_outside_output_voltage:
            return False
        if self.battery2_outside_output_voltage != other.battery2_outside_output_voltage:
            return False
        if self.battery1_outside_connection != other.battery1_outside_connection:
            return False
        if self.battery1_outside_open_circuit_fault_state != other.battery1_outside_open_circuit_fault_state:
            return False
        if self.battery2_outside_connection != other.battery2_outside_connection:
            return False
        if self.battery2_outside_open_circuit_fault_state != other.battery2_outside_open_circuit_fault_state:
            return False
        if self.charge_plug_input_voltage != other.charge_plug_input_voltage:
            return False
        if self.charge_plug_input_current != other.charge_plug_input_current:
            return False
        if self.charge_plug_input_short_circuit_fault_state != other.charge_plug_input_short_circuit_fault_state:
            return False
        if self.charge_plug_input_open_circuit_fault_state != other.charge_plug_input_open_circuit_fault_state:
            return False
        if self.chassis_power_board_fault_state != other.chassis_power_board_fault_state:
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
    def battery1_bms_charge_or_discharge(self):
        """Message field 'battery1_bms_charge_or_discharge'."""
        return self._battery1_bms_charge_or_discharge

    @battery1_bms_charge_or_discharge.setter
    def battery1_bms_charge_or_discharge(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'battery1_bms_charge_or_discharge' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'battery1_bms_charge_or_discharge' field must be an unsigned integer in [0, 255]"
        self._battery1_bms_charge_or_discharge = value

    @builtins.property
    def battery2_bms_charge_or_discharge(self):
        """Message field 'battery2_bms_charge_or_discharge'."""
        return self._battery2_bms_charge_or_discharge

    @battery2_bms_charge_or_discharge.setter
    def battery2_bms_charge_or_discharge(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'battery2_bms_charge_or_discharge' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'battery2_bms_charge_or_discharge' field must be an unsigned integer in [0, 255]"
        self._battery2_bms_charge_or_discharge = value

    @builtins.property
    def battery1_bms_output_voltage(self):
        """Message field 'battery1_bms_output_voltage'."""
        return self._battery1_bms_output_voltage

    @battery1_bms_output_voltage.setter
    def battery1_bms_output_voltage(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'battery1_bms_output_voltage' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'battery1_bms_output_voltage' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._battery1_bms_output_voltage = value

    @builtins.property
    def battery2_bms_output_voltage(self):
        """Message field 'battery2_bms_output_voltage'."""
        return self._battery2_bms_output_voltage

    @battery2_bms_output_voltage.setter
    def battery2_bms_output_voltage(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'battery2_bms_output_voltage' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'battery2_bms_output_voltage' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._battery2_bms_output_voltage = value

    @builtins.property
    def battery1_bms_output_current(self):
        """Message field 'battery1_bms_output_current'."""
        return self._battery1_bms_output_current

    @battery1_bms_output_current.setter
    def battery1_bms_output_current(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'battery1_bms_output_current' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'battery1_bms_output_current' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._battery1_bms_output_current = value

    @builtins.property
    def battery2_bms_output_current(self):
        """Message field 'battery2_bms_output_current'."""
        return self._battery2_bms_output_current

    @battery2_bms_output_current.setter
    def battery2_bms_output_current(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'battery2_bms_output_current' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'battery2_bms_output_current' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._battery2_bms_output_current = value

    @builtins.property
    def battery1_bms_charge_current(self):
        """Message field 'battery1_bms_charge_current'."""
        return self._battery1_bms_charge_current

    @battery1_bms_charge_current.setter
    def battery1_bms_charge_current(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'battery1_bms_charge_current' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'battery1_bms_charge_current' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._battery1_bms_charge_current = value

    @builtins.property
    def battery2_bms_charge_current(self):
        """Message field 'battery2_bms_charge_current'."""
        return self._battery2_bms_charge_current

    @battery2_bms_charge_current.setter
    def battery2_bms_charge_current(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'battery2_bms_charge_current' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'battery2_bms_charge_current' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._battery2_bms_charge_current = value

    @builtins.property
    def battery1_bms_temperature(self):
        """Message field 'battery1_bms_temperature'."""
        return self._battery1_bms_temperature

    @battery1_bms_temperature.setter
    def battery1_bms_temperature(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'battery1_bms_temperature' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'battery1_bms_temperature' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._battery1_bms_temperature = value

    @builtins.property
    def battery2_bms_temperature(self):
        """Message field 'battery2_bms_temperature'."""
        return self._battery2_bms_temperature

    @battery2_bms_temperature.setter
    def battery2_bms_temperature(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'battery2_bms_temperature' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'battery2_bms_temperature' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._battery2_bms_temperature = value

    @builtins.property
    def battery1_bms_soc(self):
        """Message field 'battery1_bms_soc'."""
        return self._battery1_bms_soc

    @battery1_bms_soc.setter
    def battery1_bms_soc(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'battery1_bms_soc' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'battery1_bms_soc' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._battery1_bms_soc = value

    @builtins.property
    def battery2_bms_soc(self):
        """Message field 'battery2_bms_soc'."""
        return self._battery2_bms_soc

    @battery2_bms_soc.setter
    def battery2_bms_soc(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'battery2_bms_soc' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'battery2_bms_soc' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._battery2_bms_soc = value

    @builtins.property
    def battery1_bms_soh(self):
        """Message field 'battery1_bms_soh'."""
        return self._battery1_bms_soh

    @battery1_bms_soh.setter
    def battery1_bms_soh(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'battery1_bms_soh' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'battery1_bms_soh' field must be an unsigned integer in [0, 255]"
        self._battery1_bms_soh = value

    @builtins.property
    def battery2_bms_soh(self):
        """Message field 'battery2_bms_soh'."""
        return self._battery2_bms_soh

    @battery2_bms_soh.setter
    def battery2_bms_soh(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'battery2_bms_soh' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'battery2_bms_soh' field must be an unsigned integer in [0, 255]"
        self._battery2_bms_soh = value

    @builtins.property
    def battery1_bms_short_circuit_fault_state(self):
        """Message field 'battery1_bms_short_circuit_fault_state'."""
        return self._battery1_bms_short_circuit_fault_state

    @battery1_bms_short_circuit_fault_state.setter
    def battery1_bms_short_circuit_fault_state(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'battery1_bms_short_circuit_fault_state' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'battery1_bms_short_circuit_fault_state' field must be an unsigned integer in [0, 255]"
        self._battery1_bms_short_circuit_fault_state = value

    @builtins.property
    def battery2_bms_short_circuit_fault_state(self):
        """Message field 'battery2_bms_short_circuit_fault_state'."""
        return self._battery2_bms_short_circuit_fault_state

    @battery2_bms_short_circuit_fault_state.setter
    def battery2_bms_short_circuit_fault_state(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'battery2_bms_short_circuit_fault_state' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'battery2_bms_short_circuit_fault_state' field must be an unsigned integer in [0, 255]"
        self._battery2_bms_short_circuit_fault_state = value

    @builtins.property
    def battery1_bms_open_circuit_fault_state(self):
        """Message field 'battery1_bms_open_circuit_fault_state'."""
        return self._battery1_bms_open_circuit_fault_state

    @battery1_bms_open_circuit_fault_state.setter
    def battery1_bms_open_circuit_fault_state(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'battery1_bms_open_circuit_fault_state' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'battery1_bms_open_circuit_fault_state' field must be an unsigned integer in [0, 255]"
        self._battery1_bms_open_circuit_fault_state = value

    @builtins.property
    def battery2_bms_open_circuit_fault_state(self):
        """Message field 'battery2_bms_open_circuit_fault_state'."""
        return self._battery2_bms_open_circuit_fault_state

    @battery2_bms_open_circuit_fault_state.setter
    def battery2_bms_open_circuit_fault_state(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'battery2_bms_open_circuit_fault_state' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'battery2_bms_open_circuit_fault_state' field must be an unsigned integer in [0, 255]"
        self._battery2_bms_open_circuit_fault_state = value

    @builtins.property
    def battery1_bms_other_fault_state(self):
        """Message field 'battery1_bms_other_fault_state'."""
        return self._battery1_bms_other_fault_state

    @battery1_bms_other_fault_state.setter
    def battery1_bms_other_fault_state(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'battery1_bms_other_fault_state' field must be of type 'int'"
            assert value >= 0 and value < 4294967296, \
                "The 'battery1_bms_other_fault_state' field must be an unsigned integer in [0, 4294967295]"
        self._battery1_bms_other_fault_state = value

    @builtins.property
    def battery2_bms_other_fault_state(self):
        """Message field 'battery2_bms_other_fault_state'."""
        return self._battery2_bms_other_fault_state

    @battery2_bms_other_fault_state.setter
    def battery2_bms_other_fault_state(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'battery2_bms_other_fault_state' field must be of type 'int'"
            assert value >= 0 and value < 4294967296, \
                "The 'battery2_bms_other_fault_state' field must be an unsigned integer in [0, 4294967295]"
        self._battery2_bms_other_fault_state = value

    @builtins.property
    def battery1_outside_output_voltage(self):
        """Message field 'battery1_outside_output_voltage'."""
        return self._battery1_outside_output_voltage

    @battery1_outside_output_voltage.setter
    def battery1_outside_output_voltage(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'battery1_outside_output_voltage' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'battery1_outside_output_voltage' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._battery1_outside_output_voltage = value

    @builtins.property
    def battery2_outside_output_voltage(self):
        """Message field 'battery2_outside_output_voltage'."""
        return self._battery2_outside_output_voltage

    @battery2_outside_output_voltage.setter
    def battery2_outside_output_voltage(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'battery2_outside_output_voltage' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'battery2_outside_output_voltage' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._battery2_outside_output_voltage = value

    @builtins.property
    def battery1_outside_connection(self):
        """Message field 'battery1_outside_connection'."""
        return self._battery1_outside_connection

    @battery1_outside_connection.setter
    def battery1_outside_connection(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'battery1_outside_connection' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'battery1_outside_connection' field must be an unsigned integer in [0, 255]"
        self._battery1_outside_connection = value

    @builtins.property
    def battery1_outside_open_circuit_fault_state(self):
        """Message field 'battery1_outside_open_circuit_fault_state'."""
        return self._battery1_outside_open_circuit_fault_state

    @battery1_outside_open_circuit_fault_state.setter
    def battery1_outside_open_circuit_fault_state(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'battery1_outside_open_circuit_fault_state' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'battery1_outside_open_circuit_fault_state' field must be an unsigned integer in [0, 255]"
        self._battery1_outside_open_circuit_fault_state = value

    @builtins.property
    def battery2_outside_connection(self):
        """Message field 'battery2_outside_connection'."""
        return self._battery2_outside_connection

    @battery2_outside_connection.setter
    def battery2_outside_connection(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'battery2_outside_connection' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'battery2_outside_connection' field must be an unsigned integer in [0, 255]"
        self._battery2_outside_connection = value

    @builtins.property
    def battery2_outside_open_circuit_fault_state(self):
        """Message field 'battery2_outside_open_circuit_fault_state'."""
        return self._battery2_outside_open_circuit_fault_state

    @battery2_outside_open_circuit_fault_state.setter
    def battery2_outside_open_circuit_fault_state(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'battery2_outside_open_circuit_fault_state' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'battery2_outside_open_circuit_fault_state' field must be an unsigned integer in [0, 255]"
        self._battery2_outside_open_circuit_fault_state = value

    @builtins.property
    def charge_plug_input_voltage(self):
        """Message field 'charge_plug_input_voltage'."""
        return self._charge_plug_input_voltage

    @charge_plug_input_voltage.setter
    def charge_plug_input_voltage(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'charge_plug_input_voltage' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'charge_plug_input_voltage' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._charge_plug_input_voltage = value

    @builtins.property
    def charge_plug_input_current(self):
        """Message field 'charge_plug_input_current'."""
        return self._charge_plug_input_current

    @charge_plug_input_current.setter
    def charge_plug_input_current(self, value):
        if __debug__:
            assert \
                isinstance(value, float), \
                "The 'charge_plug_input_current' field must be of type 'float'"
            assert not (value < -3.402823466e+38 or value > 3.402823466e+38) or math.isinf(value), \
                "The 'charge_plug_input_current' field must be a float in [-3.402823466e+38, 3.402823466e+38]"
        self._charge_plug_input_current = value

    @builtins.property
    def charge_plug_input_short_circuit_fault_state(self):
        """Message field 'charge_plug_input_short_circuit_fault_state'."""
        return self._charge_plug_input_short_circuit_fault_state

    @charge_plug_input_short_circuit_fault_state.setter
    def charge_plug_input_short_circuit_fault_state(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'charge_plug_input_short_circuit_fault_state' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'charge_plug_input_short_circuit_fault_state' field must be an unsigned integer in [0, 255]"
        self._charge_plug_input_short_circuit_fault_state = value

    @builtins.property
    def charge_plug_input_open_circuit_fault_state(self):
        """Message field 'charge_plug_input_open_circuit_fault_state'."""
        return self._charge_plug_input_open_circuit_fault_state

    @charge_plug_input_open_circuit_fault_state.setter
    def charge_plug_input_open_circuit_fault_state(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'charge_plug_input_open_circuit_fault_state' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'charge_plug_input_open_circuit_fault_state' field must be an unsigned integer in [0, 255]"
        self._charge_plug_input_open_circuit_fault_state = value

    @builtins.property
    def chassis_power_board_fault_state(self):
        """Message field 'chassis_power_board_fault_state'."""
        return self._chassis_power_board_fault_state

    @chassis_power_board_fault_state.setter
    def chassis_power_board_fault_state(self, value):
        if __debug__:
            assert \
                isinstance(value, int), \
                "The 'chassis_power_board_fault_state' field must be of type 'int'"
            assert value >= 0 and value < 256, \
                "The 'chassis_power_board_fault_state' field must be an unsigned integer in [0, 255]"
        self._chassis_power_board_fault_state = value

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
