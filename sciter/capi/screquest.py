"""Sciter's get resource request object - represents requests made by Element/View.request() functions.

Incomplete.
"""

import enum
from ctypes import Structure, POINTER, c_void_p

from sciter.capi.sctypes import SCFN

HREQUEST = c_void_p


class REQUEST_RESULT(enum.IntEnum):
    """."""
    REQUEST_PANIC = -1        # e.g. not enough memory
    REQUEST_OK = 0
    REQUEST_BAD_PARAM = 1     # bad parameter
    REQUEST_FAILURE = 2       # operation failed, e.g. index out of bounds
    REQUEST_NOTSUPPORTED = 3  # the platform does not support requested feature


class REQUEST_RQ_TYPE(enum.IntEnum):
    """."""
    RRT_GET = 1
    RRT_POST = 2
    RRT_PUT = 3
    RRT_DELETE = 4


class REQUEST_STATE(enum.IntEnum):
    """."""
    RS_PENDING = 0
    RS_SUCCESS = 1
    RS_FAILURE = 2


class SciterResourceType(enum.IntEnum):
    """."""
    RT_DATA_HTML = 0
    RT_DATA_IMAGE = 1
    RT_DATA_STYLE = 2
    RT_DATA_CURSOR = 3
    RT_DATA_SCRIPT = 4
    RT_DATA_RAW = 5
    RT_DATA_FONT = 6
    RT_DATA_SOUND = 7


RequestUse = SCFN(REQUEST_RESULT, HREQUEST)
RequestUnUse = SCFN(REQUEST_RESULT, HREQUEST)


class SciterRequestAPI(Structure):
    """Sciter Request ABI."""
    _fields_ = [
        ("RequestUse", RequestUse),
        ("RequestUnUse", RequestUnUse),
    ]

LPSciterRequestAPI = POINTER(SciterRequestAPI)
