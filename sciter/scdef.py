"""Common Sciter declarations."""

from enum import IntEnum

from ctypes import *
from ctypes.wintypes import *

from .sctypes import *
from .scdom import HELEMENT
from .screquest import HREQUEST
from .scvalue import PSCITER_VALUE


class LOAD_RESULT(IntEnum):
    """."""
    LOAD_OK = 0       # do default loading if data not set
    LOAD_DISCARD = 1  # discard request completely
    LOAD_DELAYED = 2  # data will be delivered later by the host application.

    LOAD_MYSELF = 3   # Use sciter-x-request.h[pp] API functions with SCN_LOAD_DATA::requestId handle .


class SciterNotification(IntEnum):
    """."""
    SC_LOAD_DATA = 0x01
    SC_DATA_LOADED = 0x02
    SC_ATTACH_BEHAVIOR = 0x04
    SC_ENGINE_DESTROYED = 0x05
    SC_POSTED_NOTIFICATION = 0x06
    SC_GRAPHICS_CRITICAL_FAILURE = 0x07


class SCITER_CALLBACK_NOTIFICATION(Structure):
    """."""
    _fields_ = [
        ("code", c_uint),
        ("hwnd", HWINDOW),
    ]


class SCN_LOAD_DATA(Structure):
    """."""
    _fields_ = [
        ("code", c_uint),
        ("hwnd", HWINDOW),
        ("uri", LPCWSTR),
        ("outData", LPCBYTE),
        ("outDataSize", UINT),
        ("dataType", UINT),
        ("requestId", HREQUEST),
        ("principal", HELEMENT),
        ("initiator", HELEMENT),
        ]


class SCN_ATTACH_BEHAVIOR(Structure):
    """."""
    _fields_ = [
        ("code", c_uint),
        ("hwnd", HWINDOW),
        ("element", HELEMENT),
        ("behaviorName", LPCSTR),
        ("elementProc", c_void_p),
        ("elementTag", LPVOID),
    ]


LPSCITER_CALLBACK_NOTIFICATION = POINTER(SCITER_CALLBACK_NOTIFICATION)
SciterHostCallback = SC_CALLBACK(UINT, LPSCITER_CALLBACK_NOTIFICATION, LPVOID)

SciterWindowDelegate = SC_CALLBACK(LRESULT, HWINDOW, UINT, WPARAM, LPARAM, LPVOID, PBOOL)

DEBUG_OUTPUT_PROC = SC_CALLBACK(VOID, LPVOID, UINT, UINT, LPCWSTR, UINT)

LPCSTR_RECEIVER = SC_CALLBACK(VOID, LPCSTR, UINT, LPVOID)
LPCWSTR_RECEIVER = SC_CALLBACK(VOID, LPCWSTR, UINT, LPVOID)
LPCBYTE_RECEIVER = SC_CALLBACK(VOID, LPCBYTE, UINT, LPVOID)

SciterElementCallback = SC_CALLBACK(BOOL, HELEMENT, LPVOID)

ElementEventProc = SC_CALLBACK(BOOL, LPVOID, HELEMENT, UINT, LPVOID)

ELEMENT_COMPARATOR = SC_CALLBACK(INT, HELEMENT, HELEMENT, LPVOID)

KeyValueCallback = SC_CALLBACK(BOOL, LPVOID, PSCITER_VALUE, PSCITER_VALUE)

NATIVE_FUNCTOR_INVOKE = CFUNCTYPE(VOID, LPVOID, UINT, PSCITER_VALUE, PSCITER_VALUE)
NATIVE_FUNCTOR_RELEASE = CFUNCTYPE(VOID, LPVOID)
