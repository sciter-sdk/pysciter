"""Sciter value, native C interface."""

import ctypes
import enum

FLOAT_VALUE = ctypes.c_double


class SCITER_VALUE(ctypes.Structure):
    """Sciter value descriptor."""
    _fields_ = [
        ("t", ctypes.c_uint32),
        ("u", ctypes.c_uint32),
        ("d", ctypes.c_uint64),
        ]

PSCITER_VALUE = ctypes.POINTER(SCITER_VALUE)


class VALUE_RESULT(enum.IntEnum):
    """Value functions result codes."""
    HV_OK_TRUE = -1
    HV_OK = 0
    HV_BAD_PARAMETER = 1
    HV_INCOMPATIBLE_TYPE = 2


class VALUE_TYPE(enum.IntEnum):
    """Sciter value types."""
    T_UNDEFINED = 0
    T_NULL = 1
    T_BOOL = 2
    T_INT = 3
    T_FLOAT = 4
    T_STRING = 5
    T_DATE = 6      # INT64 - contains a 64-bit value representing the number of 100-nanosecond intervals since January 1, 1601 (UTC), a.k.a. FILETIME on Windows
    T_CURRENCY = 7  # INT64 - 14.4 fixed number. E.g. dollars = int64 / 10000;
    T_LENGTH = 8    # length units, value is int or float, units are VALUE_UNIT_TYPE
    T_ARRAY = 9
    T_MAP = 10
    T_FUNCTION = 11
    T_BYTES = 12       # sequence of bytes - e.g. image data
    T_OBJECT = 13      # scripting object proxy (TISCRIPT/SCITER)
    T_DOM_OBJECT = 14  # DOM object (CSSS!), use get_object_data to get HELEMENT
    T_RESOURCE = 15    #
    T_RANGE = 16       # integer range N..M
    T_DURATION = 17    # time duration in seconds, stored as float
    T_ANGLE = 18       # angle value in radians, stored as float
    T_COLOR = 19       # color value, stored as 0xAABBGGRR integer


class VALUE_UNIT_TYPE(enum.IntEnum):
    """Sciter length value subtype."""
    UT_NONE = 0
    UT_EM = 1               # height of the element's font.
    UT_EX = 2               # height of letter 'x'
    UT_PR = 3               # %
    UT_SP = 4               # %% "springs", a.k.a. flex units
    reserved1 = 5
    reserved2 = 6
    UT_PX = 7               # pixels
    UT_IN = 8               # inches (1 inch = 2.54 centimeters).
    UT_CM = 9               # centimeters.
    UT_MM = 10              # millimeters.
    UT_PT = 11              # points (1 point = 1/72 inches).
    UT_PC = 12              # picas (1 pica = 12 points).
    UT_DIP = 13
    reserved3 = 14
    reserved4 = 15
    UT_URL = 22             # url in string


class VALUE_UNIT_TYPE_DATE(enum.IntEnum):
    """Sciter date subtype."""
    DT_HAS_DATE         = 0x01  # date contains date portion
    DT_HAS_TIME         = 0x02  # date contains time portion HH:MM
    DT_HAS_SECONDS      = 0x04  # date contains time and seconds HH:MM:SS
    DT_UTC              = 0x10  # T_DATE is known to be UTC. Otherwise it is local date/time


class VALUE_UNIT_TYPE_OBJECT(enum.IntEnum):
    """Sciter object subtype."""
    UT_OBJECT_ARRAY  = 0  # type T_OBJECT of type Array
    UT_OBJECT_OBJECT = 1  # type T_OBJECT of type Object
    UT_OBJECT_CLASS  = 2  # type T_OBJECT of type Class (class or namespace)
    UT_OBJECT_NATIVE = 3  # type T_OBJECT of native Type with data slot (LPVOID)
    UT_OBJECT_FUNCTION= 4 # type T_OBJECT of type Function
    UT_OBJECT_ERROR = 5   # type T_OBJECT of type Error


class VALUE_UNIT_TYPE_STRING(enum.IntEnum):
    """Sciter string subtype."""
    UT_STRING_STRING = 0       # string
    UT_STRING_ERROR = 1        # is an error string
    UT_STRING_SECURE = 2       # secure string ("wiped" on destroy)
    UT_STRING_FILE = 0xfffe    #
    UT_STRING_SYMBOL = 0xffff  # symbol in tiscript sense


class VALUE_STRING_CVT_TYPE(enum.IntEnum):
    """Value to string conversion method."""
    CVT_SIMPLE = 0         # simple conversion of terminal values
    CVT_JSON_LITERAL = 1   # json literal parsing/emission
    CVT_JSON_MAP = 2       # json parsing/emission, it parses as if token '{' already recognized
    CVT_XJSON_LITERAL = 3  # x-json parsing/emission, date is emitted as ISO8601 date literal, currency is emitted in the form DDDD$CCC
