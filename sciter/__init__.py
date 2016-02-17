from .scapi import SciterAPI
from .window import Window
from .value import value as Value
from .error import SciterError, ScriptError

sapi = api = SciterAPI()
gapi = sapi.GetSciterGraphicsAPI
rapi = sapi.GetSciterRequestAPI
