"""Behaviors support (a.k.a windowless controls)."""

import enum
from ctypes import Structure
from ctypes.wintypes import *

from .scdom import HELEMENT
from .sctypes import *
from .scvalue import SCITER_VALUE


class BEHAVIOR_EVENT_PARAMS(Structure):
    """Event params for event_handler::proc."""

    _fields_ = [
        ("cmd", UINT),
        ("heTarget", HELEMENT),
        ("he", HELEMENT),
        ("reason", UINT_PTR),
        ("data", SCITER_VALUE),
        ]


class EVENT_GROUPS(enum.IntEnum):
    """event groups."""

    HANDLE_INITIALIZATION = 0x0000  # attached/detached */
    HANDLE_MOUSE = 0x0001           # mouse events */
    HANDLE_KEY = 0x0002             # key events */
    HANDLE_FOCUS = 0x0004           # focus events  if this flag is set it also means that element it attached to is focusable */
    HANDLE_SCROLL = 0x0008          # scroll events */
    HANDLE_TIMER = 0x0010           # timer event */
    HANDLE_SIZE = 0x0020            # size changed event */
    HANDLE_DRAW = 0x0040            # drawing request (event) */
    HANDLE_DATA_ARRIVED = 0x080     # requested data () has been delivered */
    HANDLE_BEHAVIOR_EVENT = 0x0100  # logical, synthetic events: BUTTON_CLICK, HYPERLINK_CLICK, etc., a.k.a. notifications from intrinsic behaviors */
    HANDLE_METHOD_CALL = 0x0200     # behavior specific methods */
    HANDLE_SCRIPTING_METHOD_CALL = 0x0400  # behavior specific methods */
    HANDLE_TISCRIPT_METHOD_CALL = 0x0800   # behavior specific methods using direct tiscript::value's */

    HANDLE_EXCHANGE = 0x1000  # system drag-n-drop */
    HANDLE_GESTURE = 0x2000  # touch input events */

    HANDLE_ALL = 0xFFFF  # all of them */

    SUBSCRIPTIONS_REQUEST = 0xFFFFFFFF  # special value for getting subscription flags */
