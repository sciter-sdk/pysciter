"""Sciter platform-dependent types."""

import sys
import ctypes

from ctypes import (POINTER, 
                    c_char, c_byte, c_ubyte,
                    c_void_p, c_char_p, c_wchar_p,
                    c_int32, c_uint32, c_int64, c_uint64,
                    c_longlong, c_ulonglong, c_double,
                    sizeof, c_size_t, c_ssize_t)


# 'win32', 'darwin', 'linux'
SCITER_OS = sys.platform
SCITER_WIN = SCITER_OS == 'win32'
SCITER_OSX = SCITER_OS == 'darwin'
SCITER_LNX = SCITER_OS == 'linux'

if SCITER_WIN:
    SCITER_DLL_NAME = "sciter64" if sys.maxsize > 2**32 else "sciter32"

    SCFN = ctypes.WINFUNCTYPE
    SC_CALLBACK = ctypes.WINFUNCTYPE

    HWINDOW = c_void_p  # HWND

    BOOL = c_int32

    ID2D1RenderTarget = c_void_p
    ID2D1Factory = c_void_p
    IDWriteFactory = c_void_p

    IDXGISwapChain = c_void_p
    IDXGISurface = c_void_p

elif SCITER_OSX:
    assert sys.maxsize > 2**32, "Only 64-bit supported."

    SCITER_DLL_NAME = "sciter-osx-64" if sys.maxsize > 2**32 else "sciter-osx-32"

    SCFN = ctypes.CFUNCTYPE
    SC_CALLBACK = ctypes.CFUNCTYPE

    HWINDOW = c_void_p  # NSView*

    BOOL = c_byte


# Common types

VOID = None
nullptr = POINTER(c_int32)()

BYTE = c_byte
INT = c_int32
UINT = c_uint32
INT64 = c_int64
tiscript_value = c_uint64

# must be pointer-wide
# WPARAM is defined as UINT_PTR (unsigned type)
# LPARAM is defined as LONG_PTR (signed type)
WPARAM = c_size_t
LPARAM = c_ssize_t

UINT_PTR = c_size_t
LRESULT = c_ssize_t

PBOOL = LPBOOL = POINTER(BOOL)
LPCBYTE = c_char_p
LPCSTR = LPSTR = c_char_p
LPCWSTR = LPWSTR = c_wchar_p
LPCVOID = LPVOID = c_void_p
LPUINT = POINTER(UINT)

class RECT(ctypes.Structure):
    _fields_ = [("left", c_int32),
                ("top", c_int32),
                ("right", c_int32),
                ("bottom", c_int32)]
tagRECT = _RECTL = RECTL = RECT
PRECT = LPRECT = POINTER(RECT)

class POINT(ctypes.Structure):
    _fields_ = [("x", c_int32),
                ("y", c_int32)]
tagPOINT = _POINTL = POINTL = POINT
PPOINT = LPPOINT = POINTER(POINT)

class SIZE(ctypes.Structure):
    _fields_ = [("cx", c_int32),
                ("cy", c_int32)]
tagSIZE = SIZEL = SIZE
PSIZE = LPSIZE = POINTER(SIZE)

class MSG(ctypes.Structure):
    _fields_ = [("hWnd", HWINDOW),
                ("message", c_uint32),
                ("wParam", WPARAM),
                ("lParam", LPARAM),
                ("time", c_uint32),
                ("pt", POINT)]

PMSG = LPMSG = POINTER(MSG)
