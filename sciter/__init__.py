from .scapi import SciterAPI
from .window import Window
from .value import value as Value
from .error import SciterError, ScriptError, ScriptException, ValueError
from .sctypes import SCITER_WIN, SCITER_OSX, SCITER_LNX

sapi = api = SciterAPI()
gapi = sapi.GetSciterGraphicsAPI if sapi else None
rapi = sapi.GetSciterRequestAPI if sapi else None
