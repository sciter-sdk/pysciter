from .scapi import SciterAPI
from .window import Window
from .value import value as Value
from .error import SciterError, ScriptError, ScriptException, ValueError

sapi = api = SciterAPI()
gapi = sapi.GetSciterGraphicsAPI if sapi else None
rapi = sapi.GetSciterRequestAPI if sapi else None
