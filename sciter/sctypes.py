"""Sciter platform-dependent types."""

import sys
import ctypes

from ctypes import (POINTER, 
                    c_char, c_byte, c_ubyte,
                    c_void_p, c_char_p,
                    c_int32, c_uint32, c_int64, c_uint64,
                    c_longlong, c_ulonglong, c_double,
                    sizeof, c_size_t, c_ssize_t)


# 'win32', 'darwin', 'linux'
SCITER_OS = sys.platform
SCITER_WIN = SCITER_OS == 'win32'
SCITER_OSX = SCITER_OS == 'darwin'
SCITER_LNX = SCITER_OS == 'linux'


import _ctypes

def utf16tostr(addr, size=-1):
    cb = size if size > 0 else 32
    bstr = ctypes.string_at(addr, cb)
    if size > 0:
        return bstr.decode('utf-16')
    
    # lookup zero char
    chunks = []
    while True:
        found = cb
        for i in range(0, cb, 2):
            c = bstr[i]
            if c == 0x00:
                found = i
                break
            pass
        assert found % 2 == 0, "truncated string with len " + str(found)
        chunks.append(bstr[0:found].decode('utf-16'))
        if found != cb:
            break
        bstr = ctypes.string_at(addr + cb, cb)
        continue
    return "".join(chunks)

class c_utf16_lp(_ctypes._SimpleCData):
    #
    # Used as API return
    #
    _type_ = 'P'  # pointer
    def _check_retval_(cval):
        return utf16tostr(cval)
    pass

class c_utf16_p():
    #
    # API return: _SimpleCData + _check_retval_
    # API arg: ctor from string to pointer
    # API immediate value - non simple data
    #
    _type_ = 'P'  # pointer

    def __str__(self):
        return self.sval or ""

    def __init__(self, obj=None):
        self.sval = None
        # print("init", type(obj), obj)
        if isinstance(obj, str):
            # string -> pointer
            p = c_char_p(obj.encode('utf-16'))
            pv = ctypes.cast(p, c_void_p)
            self.sval = obj
            self.vval = pv
            self.value = pv.value
        elif isinstance(obj, int):
            # pointer -> string
            # print("init %d" % obj)
            pass
        pass

    def from_param(obj):
        # native from python
        # print("+++from param", obj)
        if isinstance(obj, str):
            return obj.encode('utf-16') + b'\x00\x00'
        elif isinstance(obj, c_utf16_p):
            return obj.value
        return obj

    def _check_retval_(cval):
        return utf16tostr(cval)
    pass

if SCITER_WIN:
    SCITER_DLL_NAME = "sciter64" if sys.maxsize > 2**32 else "sciter32"

    SCFN = ctypes.WINFUNCTYPE
    SC_CALLBACK = ctypes.WINFUNCTYPE

    HWINDOW = c_void_p  # HWND

    BOOL = c_int32
    LPCWSTR = LPWSTR = ctypes.c_wchar_p

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
    LPCWSTR = LPWSTR = c_utf16_p


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
