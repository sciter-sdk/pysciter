"""Sciter's platform independent graphics interface.

Incomplete.
"""
import enum
from ctypes import *

from sciter.capi.sctypes import SCFN, UINT, BOOL

HGFX = c_void_p
HIMG = c_void_p
HPATH = c_void_p
HTEXT = c_void_p


class GRAPHIN_RESULT(enum.IntEnum):
    """Result value for Sciter Graphics functions."""
    GRAPHIN_PANIC = -1
    GRAPHIN_OK = 0
    GRAPHIN_BAD_PARAM = 1
    GRAPHIN_FAILURE = 2
    GRAPHIN_NOTSUPPORTED = 3
# end

imageCreate = SCFN(GRAPHIN_RESULT, POINTER(HIMG), UINT, UINT, BOOL)


class SciterGraphicsAPI(Structure):
    """Sciter Graphics ABI."""
    _fields_ = [
        ("imageCreate", imageCreate),
    ]


LPSciterGraphicsAPI = POINTER(SciterGraphicsAPI)
