"""Python interface to sciter::value."""

# TODO: Date support.

import inspect
import ctypes

import sciter
import sciter.error
import sciter.capi.scdef
import sciter.capi.sctypes

from sciter.capi.scvalue import *

_api = sciter.SciterAPI()
byref = ctypes.byref


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


def _subtype_name(subtype):
    return [name.split('_')[-1].lower() for name, val in subtype.__members__.items()]

_value_subtypes = {VALUE_TYPE.T_LENGTH: _subtype_name(VALUE_UNIT_TYPE),
                   VALUE_TYPE.T_DATE: _subtype_name(VALUE_UNIT_TYPE_DATE),
                   VALUE_TYPE.T_OBJECT: _subtype_name(VALUE_UNIT_TYPE_OBJECT),
                   VALUE_TYPE.T_STRING: _subtype_name(VALUE_UNIT_TYPE_STRING),
                   }


# TODO: Rename it.
class ValueError(sciter.error.SciterError):
    """Raised by sciter.Value operations."""

    def __init__(self, hv_code, script=None):
        """."""
        msg = "Incompatible type" if hv_code == 2 else "Bad parameter"
        if script:
            msg = msg + " at " + script
        super().__init__(msg)
    pass


# sciter.value
class value():
    """sciter::value pythonic wrapper."""

    ## @name Value constructors:

    @classmethod
    def parse(cls, json: str, how=VALUE_STRING_CVT_TYPE.CVT_JSON_LITERAL, throw=True):
        """Parse json string into value."""
        rv = value()
        ok = _api.ValueFromString(rv, json, len(json), how)
        if ok != 0 and throw:
            raise sciter.value.ValueError(VALUE_RESULT.HV_BAD_PARAMETER, "value.parse")
        return rv

    @classmethod
    def null(cls):
        """Make explicit json null value."""
        rv = value()
        rv.data.t = VALUE_TYPE.T_NULL
        return rv

    @classmethod
    def symbol(cls, name):
        """Make sciter symbol value."""
        rv = value()
        rv._assign_str(name, VALUE_UNIT_TYPE_STRING.UT_STRING_SYMBOL)
        return rv

    @classmethod
    def secure_string(cls, val):
        """Make sciter secure string value."""
        rv = value()
        rv._assign_str(val, VALUE_UNIT_TYPE_STRING.UT_STRING_SECURE)
        return rv


    ## @name Value methods:

    def __init__(self, val=None):
        """Return a new sciter value wrapped object."""
        super().__init__()
        self.data = SCITER_VALUE()
        self.ptr = ctypes.pointer(self.data)
        self._as_parameter_ = self.ptr
        _api.ValueInit(self.ptr)
        if val is not None:
            self.set_value(val)
        pass

    def __del__(self):
        """Destroy pointed value."""
        self.clear()
        pass

    def __call__(self, *args, **kwargs):
        """Alias for self.call()."""
        return self.call(*args, **kwargs)

    def __repr__(self):
        """Machine-like value visualization."""
        t = VALUE_TYPE(self.data.t)
        tname = _value_type_names[self.data.t]
        if t in (VALUE_TYPE.T_UNDEFINED, VALUE_TYPE.T_NULL):
            return "<%s>" % (tname)

        if self.data.u != 0:
            subtypes = _value_subtypes.get(t)
            if subtypes:
                tname = tname + ':' + subtypes[self.data.u]

        return "<%s: %s>" % (tname, str(self))

    def __str__(self):
        """Human-like value representation."""
        copy = self.copy()
        ok = _api.ValueToString(copy, VALUE_STRING_CVT_TYPE.CVT_JSON_LITERAL)
        return copy.get_value()

    def __bool__(self):
        """Value to bool conversion."""
        # None, False, 0, "", (), [], {}
        return bool(self.get_value())

    def __bytes__(self):
        """Value to bytes conversion."""
        if not self.is_bytes():
            raise TypeError(repr(self))
        p = ctypes.c_char_p()
        n = ctypes.c_uint32()
        ok = _api.ValueBinaryData(self, byref(p), byref(n))
        self._throw_if(ok)
        return p.value

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
        """Item count for array, map and function."""
        return self.length()

    def __getitem__(self, key):
        """Get item for array and map type."""
        if self.is_array() and isinstance(key, int):
            # array elements can be retrieved only by index
            key = len(self) + key if key < 0 else key
            if key < 0 or key >= len(self):
                raise IndexError
            r = value()
            ok = _api.ValueNthElementValue(self, key, r)
            return r
        elif self.is_map():
            # map elements can be retrieved by sciter::value's key
            xkey = value(key)
            r = value()
            ok = _api.ValueGetValueOfKey(self, xkey, r)
            if ok != VALUE_RESULT.HV_OK or r.is_undefined():
                raise KeyError
            return r
        else:
            # unsupported type of ``self`` or ``key``
            raise TypeError
        pass

    def __setitem__(self, key, val):
        """Set item for array and map type."""
        if self.is_array() or (self.is_undefined() and isinstance(key, int)):
            # set array element by index
            if not isinstance(key, int):
                raise KeyError
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

    def __contains__(self, item):
        """Check whether item exists at array or map object."""
        xvals = self.values() if self.is_array() else self.keys()
        xitem = value(item)
        return xitem in xvals


    ## @name Sequence operations:

    def isolate(self):
        """Convert T_OBJECT value types to T_MAP or T_ARRAY.

        It will convert all object-arrays to plain JSON arrays – removing all references of script objects.
        """
        ok = _api.ValueIsolate(self)
        self._throw_if(ok)
        return self

    def copy(self):
        """Return a shallow copy of the sciter::value."""
        copy = value()
        ok = _api.ValueCopy(copy, self)
        self._throw_if(ok)
        return copy

    def copy_to(self, other):
        """Copy value to external SCITER_VALUE."""
        ok = _api.ValueCopy(other, self)
        self._throw_if(ok)
        return self

    def clear(self):
        """Clear the VALUE and deallocates all assosiated structures that are not used anywhere else."""
        ok = _api.ValueClear(self)
        self._throw_if(ok)
        return self

    def length(self) -> int:
        """Return the number of items in the T_ARRAY, T_MAP, T_FUNCTION and T_OBJECT sciter::value."""
        if not self.get_type() in (VALUE_TYPE.T_ARRAY, VALUE_TYPE.T_MAP, VALUE_TYPE.T_FUNCTION, VALUE_TYPE.T_OBJECT):
            raise AttributeError("'%s' has no attribute '%s'" % (self.get_type(), 'length'))
        n = ctypes.c_int32()
        ok = _api.ValueElementsCount(self, byref(n))
        self._throw_if(ok)
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
            self._throw_if(ok)
            r.append(xval)
        assert(len(r) == xlen)
        return list(r)

    def append(self, val):
        """Append value to the end of T_ARRAY sciter::value."""
        xval = value(val)
        ok = _api.ValueNthElementValueSet(self.length(), xval)
        self._throw_if(ok)
        return self

    def insert(self, i, val):
        """Insert or set value at given index of T_ARRAY, T_MAP, T_FUNCTION and T_OBJECT sciter::value."""
        xval = value(val)
        ok = _api.ValueNthElementValueSet(i, xval)
        self._throw_if(ok)
        return self


    ## @name Mapping sequence operations:

    def keys(self):
        """Return a new list with keys of the of T_MAP, T_FUNCTION and T_OBJECT sciter::value."""
        if not self.get_type() in (VALUE_TYPE.T_MAP, VALUE_TYPE.T_FUNCTION, VALUE_TYPE.T_OBJECT):
            raise AttributeError("'%s' has no attribute '%s'" % (self.get_type(), 'keys'))
        r = []
        for n in range(self.length()):
            xval = value()
            ok = _api.ValueNthElementKey(self, n, xval)
            self._throw_if(ok)
            r.append(xval)
        return tuple(r)

    def items(self):
        """Return a new list of (key,value) pairs of the of T_MAP, T_FUNCTION and T_OBJECT sciter::value."""
        if not self.get_type() in (VALUE_TYPE.T_MAP, VALUE_TYPE.T_FUNCTION, VALUE_TYPE.T_OBJECT):
            raise AttributeError("'%s' has no attribute '%s'" % (self.get_type(), 'items'))
        r = []
        def on_element(param, key, val):
            r.append((value(key.contents), value(val.contents)))
            return True
        scfunc = sciter.capi.scdef.KeyValueCallback(on_element)
        ok = _api.ValueEnumElements(self, scfunc, None)
        return tuple(r)


    ## @name Underlaying value operations
    def call(self, *args, **kwargs):
        """Function invokation for T_OBJECT/UT_OBJECT_FUNCTION.

        args: arguments passed to
        kwargs:
            name (str): url or name of the script - used for error reporting in the script.
            this (value): object that will be known as 'this' inside that function.
        """
        rv = value()
        argc, argv, this = sciter.Value.pack_args(*args, **kwargs)
        name = kwargs.get('name')
        ok = _api.ValueInvoke(self, this, argc, argv, rv, name)
        sciter.Value.raise_from(rv, ok <= VALUE_RESULT.HV_OK, name)
        self._throw_if(ok)
        return rv.get_value()

    def is_undefined(self):
        """."""
        t = self.get_type()
        return t == VALUE_TYPE.T_UNDEFINED

    def is_null(self):
        """."""
        t = self.get_type()
        return t == VALUE_TYPE.T_NULL

    def is_bool(self):
        """."""
        t = self.get_type()
        return t == VALUE_TYPE.T_BOOL

    def is_int(self):
        """."""
        t = self.get_type()
        return t == VALUE_TYPE.T_INT

    def is_float(self):
        """."""
        t = self.get_type()
        return t == VALUE_TYPE.T_FLOAT

    def is_bytes(self):
        """."""
        t = self.get_type()
        return t == VALUE_TYPE.T_BYTES

    def is_string(self):
        """."""
        t, u = self.get_type(with_unit=True)
        return t == VALUE_TYPE.T_STRING

    def is_error_string(self):
        """."""
        t, u = self.get_type(with_unit=True)
        return t == VALUE_TYPE.T_STRING and u == VALUE_UNIT_TYPE_STRING.UT_STRING_ERROR

    def is_symbol(self):
        """."""
        t, u = self.get_type(with_unit=True)
        return t == VALUE_TYPE.T_STRING and u == VALUE_UNIT_TYPE_STRING.UT_STRING_SYMBOL

    def is_array(self):
        """."""
        t = self.get_type()
        return t == VALUE_TYPE.T_ARRAY

    def is_map(self):
        """."""
        t = self.get_type()
        return t == VALUE_TYPE.T_MAP

    def is_function(self):
        """."""
        t = self.get_type()
        return t == VALUE_TYPE.T_FUNCTION

    def is_native_function(self):
        """."""
        return _api.ValueIsNativeFunctor(self) != 0

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
            subtypes = {VALUE_TYPE.T_LENGTH: VALUE_UNIT_TYPE,
                        VALUE_TYPE.T_STRING: VALUE_UNIT_TYPE_STRING,
                        VALUE_TYPE.T_DATE:   VALUE_UNIT_TYPE_DATE,
                        VALUE_TYPE.T_OBJECT: VALUE_UNIT_TYPE_OBJECT,
                        }
            unit_type = subtypes.get(t, None)
            unit = unit_type(self.data.u) if unit_type else self.data.u
            return (t, unit)
        pass

    def get_value(self):
        """Get Python object of the sciter::value."""
        t = self.get_type()
        if t == VALUE_TYPE.T_UNDEFINED or t == VALUE_TYPE.T_NULL:
            return None
        elif t == VALUE_TYPE.T_BOOL:
            v = ctypes.c_int32()
            ok = _api.ValueIntData(self, byref(v))
            self._throw_if(ok)
            return v.value != 0
        elif t == VALUE_TYPE.T_INT:
            v = ctypes.c_int32()
            ok = _api.ValueIntData(self, byref(v))
            self._throw_if(ok)
            return int(v.value)
        elif t == VALUE_TYPE.T_FLOAT:
            v = ctypes.c_double()
            ok = _api.ValueFloatData(self, byref(v))
            self._throw_if(ok)
            return float(v.value)
        elif t == VALUE_TYPE.T_STRING:
            if not sciter.SCITER_WIN:
                v = sciter.capi.sctypes.c_utf16_p()
                n = ctypes.c_uint32()
                ok = _api.ValueStringData(self, byref(v), byref(n))
                self._throw_if(ok)
                return v.value
            else:
                v = ctypes.c_wchar_p()
                n = ctypes.c_uint32()
                ok = _api.ValueStringData(self, byref(v), byref(n))
                self._throw_if(ok)
                # if self.data.u == VALUE_UNIT_TYPE_STRING.UT_STRING_ERROR:
                #    raise ScriptError(v.value)
                return v.value
        elif t == VALUE_TYPE.T_BYTES:
            v = ctypes.c_char_p()
            n = ctypes.c_uint32()
            ok = _api.ValueBinaryData(self, byref(v), byref(n))
            self._throw_if(ok)
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
            self._throw_if(ok)
        elif isinstance(val, int):
            ok = _api.ValueIntDataSet(self, val, VALUE_TYPE.T_INT, 0)
            self._throw_if(ok)
        elif isinstance(val, float):
            ok = _api.ValueFloatDataSet(self, val, VALUE_TYPE.T_FLOAT, 0)
            self._throw_if(ok)
        elif isinstance(val, str):
            ok = self._assign_str(val, VALUE_UNIT_TYPE_STRING.UT_STRING_STRING)
        elif isinstance(val, (bytes, bytearray)):
            ok = _api.ValueBinaryDataSet(self, ctypes.c_char_p(val), len(val), VALUE_TYPE.T_BYTES, 0)
            self._throw_if(ok)
        elif isinstance(val, (list, tuple)):
            ok = self._assign_list(val)
            self._throw_if(ok)
        elif isinstance(val, dict):
            ok = self._assign_dict(val)
            self._throw_if(ok)
        elif isinstance(val, Exception):
            ok = self._assign_str(str(val), VALUE_UNIT_TYPE_STRING.UT_STRING_ERROR)
        elif isinstance(val, (value, SCITER_VALUE)):
            ok = _api.ValueCopy(self, val)
            self._throw_if(ok)
        elif inspect.isroutine(val):
            ok = self._assign_function(val)
            self._throw_if(ok)
        else:
            raise TypeError(str(type(val)) + " is unsupported sciter type")
        pass

    def _assign_list(self, val):
        # explicit array creation since 3.3.2.6
        ok = _api.ValueIntDataSet(self, len(val), VALUE_TYPE.T_ARRAY, 0)
        for i, v in enumerate(val):
            self[i] = v
        return ok

    def _assign_dict(self, val):
        # explicit map creation since 3.3.2.6
        ok = _api.ValueIntDataSet(self, 0, VALUE_TYPE.T_MAP, 0)
        for k, v in val.items():
            self[k] = v
        return ok

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

    def _assign_function(self, callable):
        fc = _NativeFunctor(callable)
        return fc.store(self)

    def _assign_str(self, val: str, units: int):
        val = str(val)
        if not sciter.SCITER_WIN:
            bval = val.encode('utf-16le')
            n = len(bval) >> 1
            ok = _api.ValueStringDataSet(self, bval, n, units)
        else:
            ok = _api.ValueStringDataSet(self, val, len(val), units)
        self._throw_if(ok)
        return ok

    @staticmethod
    def _throw_if(code):
        if code <= 0:
            return
        import inspect
        context = inspect.stack()[1][3]
        raise sciter.value.ValueError(code, "value." + context)

    # utility methods
    @staticmethod
    def unpack_from(args, count):
        """Unpack sciter values to python types."""
        return [value(args[i]).get_value() for i in range(count)]

    @staticmethod
    def pack_to(scval, val):
        """Pack python value to SCITER_VALUE."""
        v = value(val)
        v.copy_to(scval)
        pass

    @staticmethod
    def pack_args(*args, **kwargs):
        """Pack arguments tuple as SCITER_VALUE array."""
        argc = len(args)
        args_type = SCITER_VALUE * argc
        argv = args_type()
        for i, v in enumerate(args):
            sv = sciter.Value(v)
            sv.copy_to(argv[i])
        this = value(kwargs.get('this'))
        return (argc, argv, this)

    @staticmethod
    def raise_from(error_val, success: bool, name: str):
        """Raise ScriptError or ScriptException from script error value."""
        is_error = error_val.is_error_string()
        if not success and is_error:
            raise sciter.ScriptError(error_val.get_value(), name)
        elif is_error:
            raise sciter.ScriptException(error_val.get_value(), name)
        pass

    pass
# end


_native_cache = []


class _NativeFunctor():
    """sciter::native_function wrapper."""
    def __init__(self, func):
        super().__init__()
        self.func = func
        self.scinvoke = sciter.capi.scdef.NATIVE_FUNCTOR_INVOKE(self.invoke)
        self.screlease = sciter.capi.scdef.NATIVE_FUNCTOR_RELEASE(self.release)
        pass

    def store(self, svalue):
        ok = _api.ValueNativeFunctorSet(svalue, self.scinvoke, self.screlease, None)
        _native_cache.append(self)
        return ok

    def invoke(self, tag, argc, argv, retv):
        args = value.unpack_from(argv, argc)
        try:
            rv = self.func(*args)
        except Exception as e:
            rv = e
        value.pack_to(retv, rv)
        pass

    def release(self, tag):
        _native_cache.remove(self)
        pass

    pass
