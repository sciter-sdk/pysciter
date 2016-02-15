"""Sciter platform-dependent types."""

# TODO: Linux, OSX.

from ctypes import WINFUNCTYPE, POINTER, c_void_p, c_char_p, c_int, c_int64, c_uint64
from ctypes.wintypes import HWND, WPARAM, LPARAM

import platform

SCITER_OS = platform.system()
SCITER_DLL_NAME = "sciter64" if platform.architecture()[0] == "64bit" else "sciter32"

SCFN = WINFUNCTYPE
SC_CALLBACK = WINFUNCTYPE

VOID = None
HWINDOW = HWND

INT64 = c_int64
tiscript_value = c_uint64

# must be pointer-wide
# WPARAM is defined as UINT_PTR (unsigned type)
# LPARAM is defined as LONG_PTR (signed type)
UINT_PTR = WPARAM
LRESULT = LPARAM

nullptr = POINTER(c_int)()
LPCBYTE = c_char_p
# already defined in fact
# LPUINT = c_void_p
# LPRECT = c_void_p


ID2D1RenderTarget = c_void_p
ID2D1Factory = c_void_p
IDWriteFactory = c_void_p

IDXGISwapChain = c_void_p
IDXGISurface = c_void_p
