"""Sciter bindings for Python.

Read about library at github: https://github.com/pravic/pysciter.

This component uses Sciter Engine,
copyright Terra Informatica Software, Inc.
(http://terrainformatica.com/).

:license: MIT

Bindings library licensed under [MIT license](http://opensource.org/licenses/MIT).
Sciter Engine has the [own license terms](http://sciter.com/prices/)
and [end used license agreement](https://github.com/c-smile/sciter-sdk/blob/master/license.htm)
for SDK usage.

"""

from .capi.scapi import SciterAPI
from .capi.sctypes import SCITER_WIN, SCITER_OSX, SCITER_LNX

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


def script(name=None):
    """Annotation decorator for the functions that called from script."""
    # @script def -> script(def)
    # @script('name') def -> script(name)(def)
    def decorator(func):
        attr = True if name is None else name
        func._from_sciter = attr
        return func
    if isinstance(name, str):
        return decorator
    func = name
    name = None
    return decorator(func)
