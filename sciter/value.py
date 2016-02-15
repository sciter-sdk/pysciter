"""Python interface to sciter::value."""

from .scvalue import *
from .scapi import SciterAPI

import ctypes
byref = ctypes.byref

_api = SciterAPI()

_python_types = {VALUE_TYPE.T_UNDEFINED: type(None),
                                VALUE_TYPE.T_NULL: type(None),
                                VALUE_TYPE.T_BOOL: bool,
                                VALUE_TYPE.T_INT: int,
                                VALUE_TYPE.T_FLOAT: float,
                                VALUE_TYPE.T_STRING: str,
                                VALUE_TYPE.T_ARRAY: list,
                                VALUE_TYPE.T_MAP: dict,
                                VALUE_TYPE.T_BYTES: bytes,
                                }
_value_type_names = [name.lower()[2:] for name, val in VALUE_TYPE.__members__.items()]


class value():
    """sciter::value pythonic wrapper."""

    def __init__(self, val=None):
        """Return a new sciter value wrapped object."""
        self.data = SCITER_VALUE()
        self.ptr = ctypes.pointer(self.data)
        self._as_parameter_ = self.ptr
        ok = _api.ValueInit(self.ptr)
        if val is not None:
            self.set_value(val)
        pass

    def __del__(self):
        """Destroy pointed value."""
        self.clear()
        pass

    def __repr__(self):
        """Machine-like value visualization."""
        t = VALUE_TYPE(self.data.t)
        tname = _value_type_names[self.data.t]
        if t in (VALUE_TYPE.T_UNDEFINED, VALUE_TYPE.T_NULL):
            return "<%s>" % (tname)
        return "<%s: %s>" % (tname, str(self))

    def __str__(self):
        """Human-like value representation."""
        copy = self.copy()
        ok = _api.ValueToString(copy, VALUE_STRING_CVT_TYPE.CVT_JSON_LITERAL)
        p = ctypes.c_wchar_p()
        n = ctypes.c_uint32()
        ok = _api.ValueStringData(copy, byref(p), byref(n))
        return p.value

    def __bool__(self):
        """Value to bool conversion."""
        # None, False, 0, "", (), [], {}
        return bool(self.get_value())

    def __bytes__(self):
        """Value to bytes conversion."""
        p = ctypes.c_char_p()
        n = ctypes.c_uint32()
        ok = _api.ValueBinaryData(self, byref(p), byref(n))
        return ctypes.string_at(p, n)

    def __eq__(self, other):
        """Value comparison."""
        if not isinstance(other, value):
            return NotImplemented
        ok = _api.ValueCompare(self, other)
        if ok == VALUE_RESULT.HV_OK_TRUE:
            return True
        elif ok == VALUE_RESULT.HV_OK:
            return False
        return False


    ## @name Container-like support:

    def __len__(self):
        """Items count for array, map and function."""
        return self.length()

    def __getitem__(self, key):
        """Get item for array and map type."""
        if self.get_type() == VALUE_TYPE.T_ARRAY and isinstance(key, int):
            # array elements can be retrieved only by index
            key = len(self) + key if key < 0 else key
            if key < 0 or key >= len(self):
                raise IndexError
            r = value()
            ok = _api.ValueNthElementValue(self, key, r)
            return r
        elif self.get_type() == VALUE_TYPE.T_MAP:
            # map elements can be retrieved by sciter::value's key
            xkey = value(key)
            r = value()
            ok = _api.ValueGetValueOfKey(self, xkey, r)
            if ok != VALUE_RESULT.HV_OK:
                raise KeyError
            return r
        else:
            # unsupported type of ``self`` or ``key``
            raise TypeError
        pass

    def __setitem__(self, key, val):
        """Set item for array and map type."""
        if isinstance(key, int):
            # set array element by index
            xval = value(val)
            key = len(self) + key if key < 0 else key
            ok = _api.ValueNthElementValueSet(self, key, xval)
            if ok != VALUE_RESULT.HV_OK:
                raise TypeError
        else:
            # set map element by key
            xkey = value(key)
            xval = value(val)
            ok = _api.ValueSetValueToKey(self, xkey, xval)
            if ok != VALUE_RESULT.HV_OK:
                raise TypeError
        pass

    def __delitem__(self, key):
        """Delete item from map object."""
        # only map objects are supported currently
        if self.get_type() == VALUE_TYPE.T_MAP:
            xkey = value(key)
            xval = value() # undefined
            ok = _api.ValueSetValueToKey(self, xkey, xval)
            if ok != VALUE_RESULT.HV_OK:
                raise TypeError
        else:
            raise TypeError
        pass

    def __contains__(self, item):
        """Check whether item exists at array or map object."""
        xvals = self.values() if self.get_type() == VALUE_TYPE.T_ARRAY else self.keys()
        xitem = value(item)
        return xitem in xvals


    ## @name Sequence operations:

    def copy(self):
        """Return a shallow copy of the sciter::value."""
        copy = value()
        ok = _api.ValueCopy(copy, self)
        return copy

    def clear(self):
        """Clear the VALUE and deallocates all assosiated structures that are not used anywhere else."""
        ok = _api.ValueClear(self)
        pass

    def length(self) -> int:
        """Return the number of items in the T_ARRAY, T_MAP, T_FUNCTION and T_OBJECT sciter::value."""
        if not self.get_type() in (VALUE_TYPE.T_ARRAY, VALUE_TYPE.T_MAP, VALUE_TYPE.T_FUNCTION, VALUE_TYPE.T_OBJECT):
            raise AttributeError("'%s' has no attribute '%s'" % (self.get_type(), 'length'))
        n = ctypes.c_int32()
        ok = _api.ValueElementsCount(self, byref(n))
        return n.value

    def values(self):
        """Return a list of values of the of T_ARRAY, T_MAP, T_FUNCTION and T_OBJECT sciter::value."""
        if not self.get_type() in (VALUE_TYPE.T_ARRAY, VALUE_TYPE.T_MAP, VALUE_TYPE.T_FUNCTION, VALUE_TYPE.T_OBJECT):
            raise AttributeError("'%s' has no attribute '%s'" % (self.get_type(), 'values'))
        r = []
        xlen = self.length()
        for n in range(self.length()):
            xval = value()
            ok = _api.ValueNthElementValue(self, n, xval)
            r.append(xval)
        assert(len(r) == xlen)
        return list(r)

    def append(self, val):
        """Append value to the end of T_ARRAY sciter::value."""
        xval = value(val)
        ok = _api.ValueNthElementSet(self.length(), xval)
        pass

    def insert(self, i, val):
        """Insert or set value at given index of T_ARRAY, T_MAP, T_FUNCTION and T_OBJECT sciter::value."""
        xval = value(val)
        ok = _api.ValueNthElementSet(i, xval)
        pass


    ## @name Mapping sequence operations:

    def keys(self):
        """Return a new list with keys of the of T_MAP, T_FUNCTION and T_OBJECT sciter::value."""
        if not self.get_type() in (VALUE_TYPE.T_MAP, VALUE_TYPE.T_FUNCTION, VALUE_TYPE.T_OBJECT):
            raise AttributeError("'%s' has no attribute '%s'" % (self.get_type(), 'keys'))
        r = []
        for n in range(self.length()):
            xval = value()
            ok = _api.ValueNthElementKey(self, n, xval)
            r.append(xval)
        return tuple(r)

    def items(self):
        """Return a new list of (key,value) pairs of the of T_MAP, T_FUNCTION and T_OBJECT sciter::value."""
        if not self.get_type() in (VALUE_TYPE.T_MAP, VALUE_TYPE.T_FUNCTION, VALUE_TYPE.T_OBJECT):
            raise AttributeError("'%s' has no attribute '%s'" % (self.get_type(), 'items'))
        r = []
        for n in range(self.length()):
            xkey = value()
            xval = value()
            ok = _api.ValueNthElementKey(self, n, xkey)
            ok = _api.ValueNthElementValue(self, n, xval)
            r.append((xkey, xval))
        return tuple(r)


    ## @name Underlaying value operations

    def get_type(self, py=False, with_unit=False):
        """Return python type or sciter type with (optionally) unit subtype of sciter::value."""
        t = VALUE_TYPE(self.data.t)
        if py:
            # return Python type equivalent if supported
            if t in _python_types:
                return _python_types[t]
            return NotImplemented
        # return sciter::value underlaying type
        if not with_unit:
            return t
        else:
            return (t, VALUE_UNIT_TYPE(self.data.u))
        pass

    def get_value(self):
        """Get Python object of the sciter::value."""
        t = self.get_type()
        if t == VALUE_TYPE.T_UNDEFINED or t == VALUE_TYPE.T_NULL:
            return None
        elif t == VALUE_TYPE.T_BOOL:
            v = ctypes.c_int32()
            ok = _api.ValueIntData(self, byref(v))
            return v.value != 0
        elif t == VALUE_TYPE.T_INT:
            v = ctypes.c_int32()
            ok = _api.ValueIntData(self, byref(v))
            return int(v.value)
        elif t == VALUE_TYPE.T_FLOAT:
            v = ctypes.c_double()
            ok = _api.ValueFloatData(self, byref(v))
            return float(v.value)
        elif t == VALUE_TYPE.T_STRING:
            v = ctypes.c_wchar_p()
            n = ctypes.c_uint32()
            ok = _api.ValueStringData(self, byref(v), byref(n))
            return v.value
        elif t == VALUE_TYPE.T_BYTES:
            v = ctypes.c_char_p()
            n = ctypes.c_uint32()
            ok = _api.ValueBinaryData(self, byref(v), byref(n))
            return v.value
        elif t == VALUE_TYPE.T_ARRAY:
            return self._get_list()
        elif t == VALUE_TYPE.T_MAP:
            return self._get_dict()
        else:
            raise TypeError(str(t) + " is unsupported python type")
        pass

    def set_value(self, val):
        """Set Python object to the sciter::value.

        sciter <=> python types:
          null
          boolean
          int
          float
          bytes
          string
          array
          map

        """
        if val is None:
            self.data.t = VALUE_TYPE.T_NULL
        elif isinstance(val, bool):
            ok = _api.ValueIntDataSet(self, int(val), VALUE_TYPE.T_BOOL, 0)
        elif isinstance(val, int):
            ok = _api.ValueIntDataSet(self, val, VALUE_TYPE.T_INT, 0)
        elif isinstance(val, float):
            ok = _api.ValueFloatDataSet(self, val, VALUE_TYPE.T_FLOAT, 0)
        elif isinstance(val, str):
            ok = _api.ValueStringDataSet(self, val, len(val), 0)
        elif isinstance(val, (bytes, bytearray)):
            ok = _api.ValueBinaryDataSet(self, ctypes.c_char_p(val), len(val), VALUE_TYPE.T_BYTES, 0)
        elif isinstance(val, (list, tuple)):
            ok = self._assign_list(val)
        elif isinstance(val, dict):
            ok = self._assign_dict(val)
        elif isinstance(val, (value, SCITER_VALUE)):
            ok = _api.ValueCopy(self, val)
        else:
            raise TypeError(str(type(val)) + " is unsupported sciter type")
        pass

    def _assign_list(self, val):
        for i, v in enumerate(val):
            self[i] = v
        pass

    def _assign_dict(self, val):
        for k, v in val.items():
            self[k] = v
        pass

    def _get_list(self):
        # convert sciter array to python list
        r = []
        for item in self.values():
            r.append(item.get_value())
        return list(r)

    def _get_dict(self):
        # convert sciter map/object to python dict
        r = {}
        for key, item in self.items():
            r[key.get_value()] = item.get_value()
        return r

# end
