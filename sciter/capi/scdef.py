"""Common Sciter declarations."""

import enum

from ctypes import *

from sciter.capi.sctypes import *
from sciter.capi.scdom import HELEMENT
from sciter.capi.screquest import HREQUEST
from sciter.capi.scvalue import PSCITER_VALUE


class LOAD_RESULT(enum.IntEnum):
    """."""
    LOAD_OK = 0       # do default loading if data not set
    LOAD_DISCARD = 1  # discard request completely
    LOAD_DELAYED = 2  # data will be delivered later by the host application.

    LOAD_MYSELF = 3   # Use sciter-x-request.h[pp] API functions with SCN_LOAD_DATA::requestId handle.


class SciterNotification(enum.IntEnum):
    """."""
    SC_LOAD_DATA = 0x01
    SC_DATA_LOADED = 0x02
    SC_ATTACH_BEHAVIOR = 0x04
    SC_ENGINE_DESTROYED = 0x05
    SC_POSTED_NOTIFICATION = 0x06
    SC_GRAPHICS_CRITICAL_FAILURE = 0x07
    SC_KEYBOARD_REQUEST = 0x08
    SC_INVALIDATE_RECT = 0x09


class SCITER_RT_OPTIONS(enum.IntEnum):
    """Sciter engine options (global or per-window)."""
    SCITER_SMOOTH_SCROLL = 1       # value: TRUE - enable, value: FALSE - disable, enabled by default
    SCITER_CONNECTION_TIMEOUT = 2  # global; value: milliseconds, connection timeout of http client
    SCITER_HTTPS_ERROR = 3         # global; value: 0 - drop connection, 1 - use builtin dialog, 2 - accept connection silently
    SCITER_FONT_SMOOTHING = 4      # value: 0 - system default, 1 - no smoothing, 2 - std smoothing, 3 - clear type

    SCITER_TRANSPARENT_WINDOW = 6  # Windows Aero support, value:
                                   # 0 - normal drawing,
                                   # 1 - window has transparent background after calls DwmExtendFrameIntoClientArea() or DwmEnableBlurBehindWindow().
    SCITER_SET_GPU_BLACKLIST  = 7  # global;
                                   # value = LPCBYTE, json - GPU black list, see: gpu-blacklist.json resource.
    SCITER_SET_SCRIPT_RUNTIME_FEATURES = 8,  # global or window; value - combination of SCRIPT_RUNTIME_FEATURES flags.
    SCITER_SET_GFX_LAYER = 9       # global; value - GFX_LAYER
    SCITER_SET_DEBUG_MODE = 10     # global or window; value - TRUE/FALSE
    SCITER_SET_UX_THEMING = 11     # global; value - BOOL, TRUE - the engine will use "unisex" theme that is common for all platforms.
                                   # That UX theme is not using OS primitives for rendering input elements. Use it if you want exactly
                                   # the same (modulo fonts) look-n-feel on all platforms.
    SCITER_ALPHA_WINDOW  = 12      # hWnd, value - TRUE/FALSE - window uses per pixel alpha (e.g. WS_EX_LAYERED/UpdateLayeredWindow() window)
    SCITER_SET_INIT_SCRIPT = 13    # hWnd - N/A , value LPCSTR - UTF-8 encoded script source to be loaded into each view before any other script execution.


class SCRIPT_RUNTIME_FEATURES(enum.IntEnum):
    ALLOW_FILE_IO = 0x00000001
    ALLOW_SOCKET_IO = 0x00000002
    ALLOW_EVAL = 0x00000004
    ALLOW_SYSINFO = 0x00000008


class GFX_LAYER(enum.IntEnum):
    AUTO          = 0xFFFF
    CPU           = 1

    if SCITER_WIN:
        GDI       = 1
    elif SCITER_LNX:
        CG        = 1
    elif SCITER_OSX:
        CAIRO     = 1

    if SCITER_WIN:
        WARP      = 2
        D2D       = 3

    SKIA_CPU      = 4
    SKIA_OPENGL   = 5


class OUTPUT_SUBSYTEMS(enum.IntEnum):
    DOM = 0       # html parser & runtime
    CSSS = 1      # csss! parser & runtime
    CSS = 2       # css parser
    TIS = 3       # TIS parser & runtime


class OUTPUT_SEVERITY(enum.IntEnum):
    INFO = 0
    WARNING = 1
    ERROR = 2


class SCITER_CREATE_WINDOW_FLAGS(enum.IntEnum):
    SW_CHILD      = (1 << 0)    # child window only, if this flag is set all other flags ignored
    SW_TITLEBAR   = (1 << 1)    # toplevel window, has titlebar
    SW_RESIZEABLE = (1 << 2)    # has resizeable frame
    SW_TOOL       = (1 << 3)    # is tool window
    SW_CONTROLS   = (1 << 4)    # has minimize / maximize buttons
    SW_GLASSY     = (1 << 5)    # glassy window - supports "Acrylic" on Windows and "Vibrant" on MacOS.
    SW_ALPHA      = (1 << 6)    # transparent window ( e.g. WS_EX_LAYERED on Windows )
    SW_MAIN       = (1 << 7)    # main window of the app, will terminate the app on close
    SW_POPUP      = (1 << 8)    # the window is created as topmost window.
    SW_ENABLE_DEBUG = (1 << 9)  # make this window inspector ready
    SW_OWNS_VM    = (1 << 10)   # it has its own script VM


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
        ("_uri", LPCWSTR),
        ("outData", LPCBYTE),
        ("outDataSize", UINT),
        ("dataType", UINT),
        ("requestId", HREQUEST),
        ("principal", HELEMENT),
        ("initiator", HELEMENT),
        ]
    uri = UTF16LEField('_uri')


class SCN_DATA_LOADED(Structure):
    """."""
    _fields_ = [
        ("code", c_uint),
        ("hwnd", HWINDOW),
        ("_uri", LPCWSTR),
        ("data", LPCBYTE),
        ("dataSize", UINT),
        ("dataType", UINT),
        ("status", UINT),
        ]
    uri = UTF16LEField('_uri')


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

class SCN_KEYBOARD_REQUEST(Structure):
    """."""
    _fields_ = [
        ("code", c_uint),
        ("hwnd", HWINDOW),
        ("keyboardMode", c_uint)
    ]

class SCN_INVALIDATE_RECT(Structure):
    """."""
    _fields_ = [
        ("code", c_uint),
        ("hwnd", HWINDOW),
        ("invalidRect", RECT)
    ]


LPSCITER_CALLBACK_NOTIFICATION = POINTER(SCITER_CALLBACK_NOTIFICATION)
SciterHostCallback = SC_CALLBACK(UINT, LPSCITER_CALLBACK_NOTIFICATION, LPVOID)

if SCITER_WIN:
    SciterWindowDelegate = SC_CALLBACK(LRESULT, HWINDOW, UINT, WPARAM, LPARAM, LPVOID, PBOOL)
else:
    SciterWindowDelegate = c_void_p

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

ELEMENT_BITMAP_RECEIVER = SC_CALLBACK(VOID, LPCBYTE, INT, INT, UINT, UINT, LPVOID)


class StringReceiver():
    """LPCWSTR_RECEIVER wrapper."""

    def __init__(self, string_type: str):
        """Construct callback by one of 'char', 'wchar' or 'byte' string type."""
        self.text = None
        if string_type == 'char':
            self.cb = LPCSTR_RECEIVER(self._a2s)
        elif string_type == 'byte':
            self.cb = LPCBYTE_RECEIVER(self._b2s)
        elif string_type == 'wchar':
            self.cb = LPCWSTR_RECEIVER(self._w2s)
        else:
            raise ValueError("Unknown callback type. Use one of 'char', 'byte' or 'wchar'.")
        self._as_parameter_ = self.cb
        pass

    def _w2s(self, sz, n, ctx):
        # wchar_t
        self.text = sz if SCITER_WIN else sz.value
        pass

    def _a2s(self, sz, n, ctx):
        # char
        self.text = sz.decode('utf-8')
        pass

    def _b2s(self, sz, n, ctx):
        # byte
        self.text = sz.decode('utf-8')
        pass
    pass
