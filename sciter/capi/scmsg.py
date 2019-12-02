"""Message definitions to be passed to the SciterProcX function.

"""
import enum

from ctypes import Structure, Union, c_void_p
from sciter.capi.sctypes import UINT, BOOL, HDC, POINT
from sciter.capi.scdef import ELEMENT_BITMAP_RECEIVER
from sciter.capi.scdom import HELEMENT
from sciter.capi.scbehavior import MOUSE_BUTTONS, MOUSE_EVENTS, KEYBOARD_STATES

class SCITER_X_MSG_CODE(enum.IntEnum):
    """SCITER_X_MSG message/function identifier."""
    SXM_CREATE = 0
    SXM_DESTROY = 1
    SXM_SIZE = 2
    SXM_PAINT = 3
    SXM_RESOLUTION = 4
    SXM_HEARTBIT = 5
    SXM_MOUSE = 6
    SXM_KEY = 7
    SXM_FOCUS = 8
# end


class SCITER_X_MSG(Structure):
    """Common header of message structures passed to SciterProcX."""
    _fields_ = [
        ("msg", UINT),  # SCITER_X_MSG_CODE
    ]


class SCITER_X_MSG_CREATE(Structure):
    """Create event passed to Sciter."""
    _fields_ = [
        ("header", SCITER_X_MSG),
        ("backend", UINT),
        ("transparent", BOOL),
    ]


class SCITER_X_MSG_DESTROY(Structure):
    """Destroy event passed to Sciter."""
    _fields_ = [
        ("header", SCITER_X_MSG),
    ]


class SCITER_X_MSG_SIZE(Structure):
    _fields_ = [
        ("header", SCITER_X_MSG),
        ("width", UINT),
        ("height", UINT),
    ]

class SCITER_X_MSG_RESOLUTION(Structure):
    _fields_ = [
        ("header", SCITER_X_MSG),
        ("pixelsPerInch", UINT),
    ]

class SCITER_X_MSG_MOUSE(Structure):
    _fields_ = [
        ("header", SCITER_X_MSG),
        #("button", UINT),      # this field has been reordered in 4.4.0.3
        ("event", UINT),        # MOUSE_EVENTS
        ("button", UINT),       # MOUSE_BUTTONS
        ("modifiers", UINT),    # KEYBOARD_STATES
        ("pos", POINT),
    ]

class SCITER_X_MSG_KEY(Structure):
    _fields_ = [
        ("header", SCITER_X_MSG),
        #("button", UINT),      # this field has been reordered in 4.4.0.3
        ("event", UINT),        # MOUSE_EVENTS
        ("code", UINT),         # key scan code
        ("modifiers", UINT),    # KEYBOARD_STATES
    ]

class SCITER_X_MSG_FOCUS(Structure):
    _fields_ = [
        ("header", SCITER_X_MSG),
        ("got", BOOL),
    ]

class SCITER_X_MSG_HEARTBIT(Structure):
    _fields_ = [
        ("header", SCITER_X_MSG),
        ("time", UINT),

    ]

class SCITER_PAINT_TARGET_TYPE(enum.IntEnum):
    SPT_DEFAULT = 0     # default rendering target - window surface
    SPT_RECEIVER = 1    # target::receiver fields are valid
    SPT_DC = 2          # target::hdc is valid
    SPT_OPENGL = 3      # target is not used - caller shall set current context on its side
    SPT_OPENGLES = 4    # target is not used - caller shall set current context on its side


class SCITER_X_MSG_PAINT_RECEIVER(Structure):
    _fields_ = [
        ("param", c_void_p),
        ("callback", ELEMENT_BITMAP_RECEIVER),
    ]


class SCITER_X_MSG_PAINT_TARGET(Union):
    _fields_ = [
        ("hdc", HDC),
        ("receiver", SCITER_X_MSG_PAINT_RECEIVER),
    ]


class SCITER_X_MSG_PAINT(Structure):
    _fields_ = [
        ("header", SCITER_X_MSG),
        ("element", HELEMENT),          # layer #HELEMENT, can be NULL if whole tree (document) needs to be rendered.
        ("isFore", BOOL),               # if element is not null tells if that element is fore-layer.
        ("targetType", UINT),           # one of SCITER_PAINT_TARGET_TYPE values.
        ("target", SCITER_X_MSG_PAINT_TARGET)
    ]
