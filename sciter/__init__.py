"""Sciter bindings for Python.

Read about library at github: https://github.com/sciter-sdk/pysciter.

This component uses Sciter Engine,
copyright Terra Informatica Software, Inc.
(http://terrainformatica.com/).

:license: MIT

Bindings library licensed under [MIT license](https://opensource.org/licenses/MIT).
Sciter Engine has the [own license terms](https://sciter.com/prices/)
and [end used license agreement](https://github.com/c-smile/sciter-sdk/blob/master/license.htm)
for SDK usage.

"""

from .capi.scapi import SciterAPI
from .capi.sctypes import SCITER_WIN, SCITER_OSX, SCITER_LNX
from .capi.scdef import SCITER_RT_OPTIONS

from .value import value as Value
from .window import Window
from .dom import Element
from .event import EventHandler
from .error import SciterError, ScriptError, ScriptException

sapi = api = SciterAPI()
gapi = sapi.GetSciterGraphicsAPI if sapi else None
rapi = sapi.GetSciterRequestAPI if sapi else None


def version(as_str=False):
    """Return version of Sciter engine as (3,3,1,7) tuple or '3.3.1.7' string."""
    high = api.SciterVersion(True)
    low = api.SciterVersion(False)
    ver = (high >> 16, high & 0xFFFF, low >> 16, low & 0xFFFF)
    return ".".join(map(str, ver)) if as_str else ver


def version_num():
    """Return version of Sciter engine as 0x03030107 number."""
    # However, `4.0.2.5257` can't be represented as a 32-bit number, we return `0x04_00_02_00` instead.
    a, b, c, _ = version()
    return (a << 24) | (b << 16) | (c << 8) | (0)

def api_version():
    """Return Sciter API version number, since 4.4.0.3."""
    # `0x0000_0001` in regular builds
    # `0x0001_0001` in windowless versions.
    return api.version

def is_windowless():
    """Returns True for windowless builds."""
    return api_version() >= 0x00010001

def set_option(option, value):
    """Set various sciter engine global options, see the SCITER_RT_OPTIONS."""
    ok = api.SciterSetOption(None, option, value)
    if not ok:
        raise SciterError("Could not set option " + str(option) + "=" + str(value))
    return True

def runtime_features(file_io=True, socket_io=True, allow_eval=True, allow_sysinfo=True):
    """Set runtime features that have been disabled by default since 4.2.5.0"""
    from .capi.scdef import SCRIPT_RUNTIME_FEATURES
    flags = 0
    if file_io:
        flags += SCRIPT_RUNTIME_FEATURES.ALLOW_FILE_IO
    if socket_io:
        flags += SCRIPT_RUNTIME_FEATURES.ALLOW_SOCKET_IO
    if allow_eval:
        flags += SCRIPT_RUNTIME_FEATURES.ALLOW_EVAL
    if allow_sysinfo:
        flags += SCRIPT_RUNTIME_FEATURES.ALLOW_SYSINFO
    return set_option(SCITER_RT_OPTIONS.SCITER_SET_SCRIPT_RUNTIME_FEATURES, flags)

def script(name=None, convert=True, safe=True):
    """Annotation decorator for the functions that called from script."""
    # @script def -> script(def)
    # @script('name') def -> script(name)(def)

    # `convert`: Convert Sciter values to Python types
    # `safe`: Pass exceptions to Sciter or ignore them

    def decorator(func):
        attr = True if name is None else name
        func._from_sciter = attr
        func._sciter_cfg = dict(name=name, convert=convert, safe=safe)
        return func

    # script('name')
    if name is None or isinstance(name, str):
        return decorator

    # script(def)
    func = name
    name = None
    return decorator(func)
