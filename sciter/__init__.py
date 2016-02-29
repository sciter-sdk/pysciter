from .scapi import SciterAPI
from .window import Window
from .dom import Element
from .event import EventHandler
from .value import value as Value
from .error import SciterError, ScriptError, ScriptException, ValueError
from .sctypes import SCITER_WIN, SCITER_OSX, SCITER_LNX

sapi = api = SciterAPI()
gapi = sapi.GetSciterGraphicsAPI if sapi else None
rapi = sapi.GetSciterRequestAPI if sapi else None


def version():
    """Return version of Sciter engine as (3,3,1,7)."""
    high = api.SciterVersion(True)
    low = api.SciterVersion(False)
    return (high >> 16, high & 0xFFFF, low >> 16, low & 0xFFFF)
