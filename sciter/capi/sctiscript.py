"""TIScript Virtual Machine Runtime.

Incomplete.
"""
import ctypes

HVM = ctypes.c_void_p
value = ctypes.c_uint64


class tiscript_native_interface(ctypes.Structure):
    """."""
    _fields_ = [
        ("create_vm", ctypes.c_void_p),
        # TODO: rest of TIScript API
        ]
