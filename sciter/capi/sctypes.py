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


def utf16tostr(addr, size=-1):
    """Read UTF-16 string from memory and encode as python string."""
    cb = size if size > 0 else 32
    bstr = ctypes.string_at(addr, cb)
    if size >= 0:
        return bstr.decode('utf-16le')

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
        chunks.append(bstr[0:found].decode('utf-16le'))
        if found != cb:
            break
        addr = addr + cb
        bstr = ctypes.string_at(addr, cb)
        continue
    return "".join(chunks)


class c_utf16_p(ctypes.c_char_p):
    """A ctypes wrapper for UTF-16 string pointer."""
    # Taken from http://stackoverflow.com/a/35507014/736762, thanks to @eryksun.
    def __init__(self, value=None):
        super(c_utf16_p, self).__init__()
        if value is not None:
            self.value = value

    @property
    def value(self,
              c_void_p=ctypes.c_void_p):
        addr = c_void_p.from_buffer(self).value
        return utf16tostr(addr)

    @value.setter
    def value(self, value,
              c_char_p=ctypes.c_char_p):
        value = value.encode('utf-16le') + b'\x00'
        c_char_p.value.__set__(self, value)

    @classmethod
    def from_param(cls, obj):
        if isinstance(obj, str):
            obj = obj.encode('utf-16le') + b'\x00'
        return super(c_utf16_p, cls).from_param(obj)

    @classmethod
    def _check_retval_(cls, result):
        return result.value
    pass


class UTF16LEField(object):
    """Structure member wrapper for UTF-16 string pointers."""
    # Taken from http://stackoverflow.com/a/35507014/736762, thanks to @eryksun.
    def __init__(self, name):
        self.name = name

    def __get__(self, obj, cls,
                c_void_p=ctypes.c_void_p,
                addressof=ctypes.addressof):
        field_addr = addressof(obj) + getattr(cls, self.name).offset
        addr = c_void_p.from_address(field_addr).value
        return utf16tostr(addr)

    def __set__(self, obj, value):
        value = value.encode('utf-16le') + b'\x00'
        setattr(obj, self.name, value)
    pass


if SCITER_WIN:
    SCITER_DLL_NAME = "sciter64" if sys.maxsize > 2**32 else "sciter32"
    SCITER_DLL_EXT = ".dll"

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
    # sciter-osx-32 since 3.3.1.8
    SCITER_DLL_NAME = "sciter-osx-64" if sys.maxsize > 2**32 else "sciter-osx-32"
    SCITER_DLL_EXT = ".dylib"

    SCFN = ctypes.CFUNCTYPE
    SC_CALLBACK = ctypes.CFUNCTYPE

    HWINDOW = c_void_p  # NSView*

    BOOL = c_byte
    LPCWSTR = LPWSTR = c_utf16_p

elif SCITER_LNX:
    assert sys.maxsize > 2**32, "Only 64-bit build supported."
    SCITER_DLL_NAME = "libsciter-gtk-64" if sys.maxsize > 2**32 else "libsciter-gtk-32"
    SCITER_DLL_EXT = ".so"

    SCFN = ctypes.CFUNCTYPE
    SC_CALLBACK = ctypes.CFUNCTYPE

    HWINDOW = c_void_p  # GtkWidget*

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
    """Rectangle coordinates structure."""
    _fields_ = [("left", c_int32),
                ("top", c_int32),
                ("right", c_int32),
                ("bottom", c_int32)]
tagRECT = _RECTL = RECTL = RECT
PRECT = LPRECT = POINTER(RECT)


class POINT(ctypes.Structure):
    """Point coordinates structure."""
    _fields_ = [("x", c_int32),
                ("y", c_int32)]
tagPOINT = _POINTL = POINTL = POINT
PPOINT = LPPOINT = POINTER(POINT)


class SIZE(ctypes.Structure):
    """SIZE structure for width and height."""
    _fields_ = [("cx", c_int32),
                ("cy", c_int32)]
tagSIZE = SIZEL = SIZE
PSIZE = LPSIZE = POINTER(SIZE)


class MSG(ctypes.Structure):
    """MSG structure for windows message queue."""
    _fields_ = [("hWnd", HWINDOW),
                ("message", c_uint32),
                ("wParam", WPARAM),
                ("lParam", LPARAM),
                ("time", c_uint32),
                ("pt", POINT)]

PMSG = LPMSG = POINTER(MSG)
