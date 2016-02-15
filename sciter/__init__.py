from .scapi import SciterAPI

sapi = api = SciterAPI()
gapi = sapi.GetSciterGraphicsAPI
rapi = sapi.GetSciterRequestAPI
