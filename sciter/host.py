"""Sciter host application helpers."""

import ctypes
import os.path

from sciter.capi.scdef import *
from sciter.capi.sctypes import HWINDOW

import sciter
import sciter.dom

_api = sciter.SciterAPI()


class Host():
    """Standard implementation of SCITER_CALLBACK_NOTIFY handler."""

    def __init__(self):
        """."""
        super().__init__()
        self.hwnd = None
        self.root = None
        pass

    def __call__(self, name, *args):
        """Alias for self.call_function()."""
        return self.call_function(name, *args)

    def setup_callback(self, hwnd):
        """Set callback for sciter engine events."""
        if not hwnd:
            raise ValueError("Invalid window handle provided.")
        self.hwnd = hwnd
        self.root = self.get_root()  # if called on existing document
        self._sciter_handler_proc = SciterHostCallback(self.handle_notification)
        _api.SciterSetCallback(hwnd, self._sciter_handler_proc, ctypes.c_void_p(0))
        pass

    def setup_debug(self, hwnd=None):
        """Setup debug output function for specific window or globally."""
        ok = _api.SciterSetOption(hwnd, SCITER_RT_OPTIONS.SCITER_SET_DEBUG_MODE, True)
        self._sciter_debug_proc = DEBUG_OUTPUT_PROC(self.on_debug_output)
        _api.SciterSetupDebugOutput(hwnd, None, self._sciter_debug_proc)
        pass

    def set_option(self, option, value):
        """Set various sciter engine options, see the SCITER_RT_OPTIONS."""
        hwnd = self.hwnd
        if option in (SCITER_RT_OPTIONS.SCITER_SET_GPU_BLACKLIST, SCITER_RT_OPTIONS.SCITER_SET_GFX_LAYER, SCITER_RT_OPTIONS.SCITER_SET_UX_THEMING):
            hwnd = None
        ok = _api.SciterSetOption(hwnd, option, value)
        if not ok:
            raise sciter.SciterError("Could not set option " + str(option) + "=" + str(value))
        return self

    def set_home_url(self, url: str):
        """Set sciter window home url."""
        ok = _api.SciterSetHomeURL(self.hwnd, url)
        if not ok:
            raise sciter.SciterError("Could not home url " + str(url))
        return self

    def set_media_type(self, media_type: str):
        """Set media type of this sciter instance."""
        ok = _api.SciterSetMediaType(self.hwnd, media_type)
        if not ok:
            raise sciter.SciterError("Could not set media type " + str(media_type))
        return self

    def set_media_vars(self, media: dict):
        """Set media variables of this sciter instance."""
        v = sciter.Value(media)
        ok = _api.SciterSetMediaVars(self.hwnd, v)
        if not ok:
            raise sciter.SciterError("Could not set media vars " + str(media))
        return self

    def set_master_css(self, css_str: str, append: bool):
        """Set Master style sheet."""
        utf = css_str.encode('utf-8')
        if append:
            ok = _api.SciterAppendMasterCSS(utf, len(utf))
        else:
            ok = _api.SciterSetMasterCSS(utf, len(utf))
        if not ok:
            raise sciter.SciterError("Could not set master CSS")
        return self

    def set_css(self, css_str: str, base_url: str, media_type: str):
        """Set (reset) style sheet of current document."""
        utf = css_str.encode('utf-8')
        ok = _api.SciterSetCSS(self.hwnd, utf, len(utf), base_url, media_type)
        if not ok:
            raise sciter.SciterError("Could not set CSS")
        return self

    def get_hwnd(self) -> HWINDOW:
        """Get window handle."""
        return self.hwnd

    def load_file(self, uri: str, normalize=True):
        """Load HTML document from file."""
        if normalize and "://" not in uri:
            uri = "file://" + os.path.abspath(uri).replace("\\", "/")
        ok = _api.SciterLoadFile(self.hwnd, uri)
        if not ok:
            raise sciter.SciterError("Unable to load file " + uri)
        self.root = self.get_root()
        return self

    def load_html(self, html: bytes, uri=None):
        """Load HTML document from memory."""
        if not isinstance(html, bytes):
            raise TypeError("html must be a bytes type")
        cb = len(html)
        pb = ctypes.c_char_p(html)
        ok = _api.SciterLoadHtml(self.hwnd, pb, cb, uri)
        if not ok:
            raise sciter.SciterError("Unable to load html " + str(uri))
        self.root = self.get_root()
        return self

    def get_root(self):
        """Get window root DOM element."""
        he = sciter.dom.HELEMENT()
        ok = _api.SciterGetRootElement(self.hwnd, ctypes.byref(he))
        return sciter.dom.Element(he) if he else None

    def eval_script(self, script: str, name=None):
        """Evaluate script in context of current document."""
        rv = sciter.Value()
        ok = _api.SciterEval(self.hwnd, script, len(script), rv)
        sciter.Value.raise_from(rv, ok != False, name if name else 'Host.eval')
        return rv

    def call_function(self, name: str, *args):
        """Call scripting function defined in the global namespace."""
        rv = sciter.Value()
        argc, argv, this = sciter.Value.pack_args(*args)
        ok = _api.SciterCall(self.hwnd, name.encode('utf-8'), argc, argv, rv)
        sciter.Value.raise_from(rv, ok != False, name)
        return rv

    def data_ready(self, uri: str, data: bytes, request_id=None, hwnd=None):
        """This function is used as response to SCN_LOAD_DATA request."""
        if not hwnd:
            hwnd = self.hwnd
        if request_id is not None:
            ok = _api.SciterDataReadyAsync(hwnd, uri, data, len(data), request_id)
        else:
            ok = _api.SciterDataReady(hwnd, uri, data, len(data))
        if not ok:
            raise sciter.SciterError("Unable to pass data for " + uri)
        pass


    ## @name following functions can be overloaded
    def on_load_data(self, nm: SCN_LOAD_DATA):
        """Notifies that Sciter is about to download a referred resource."""
        pass

    def on_data_loaded(self, nm: SCN_DATA_LOADED):
        """This notification indicates that external data (for example image) download process completed."""
        pass

    def on_attach_behavior(self, nm: SCN_ATTACH_BEHAVIOR):
        """This notification is sent on parsing the document and while processing elements having non empty `style.behavior` attribute value."""
        pass

    def on_debug_output(self, tag, subsystem, severity, text, text_len):
        """This output function will be used for reprting problems found while loading html and css documents."""
        sysname = OUTPUT_SUBSYTEMS(subsystem).name.lower()
        sevname = OUTPUT_SEVERITY(severity).name.lower()
        if not sciter.SCITER_WIN:
            text = text.value
        message = text.replace("\r", "\n").rstrip()
        if message:
            print("{}:{}: {}".format(sevname, sysname, message))
        pass

    def handle_notification(self, pnm, param):
        """Sciter notification handler."""
        rv = 0
        nm = pnm.contents
        if nm.code == SciterNotification.SC_LOAD_DATA:
            rv = self.on_load_data(ctypes.cast(pnm, ctypes.POINTER(SCN_LOAD_DATA)).contents)
        elif nm.code == SciterNotification.SC_DATA_LOADED:
            rv = self.on_data_loaded(ctypes.cast(pnm, ctypes.POINTER(SCN_DATA_LOADED)).contents)
        elif nm.code == SciterNotification.SC_ATTACH_BEHAVIOR:
            rv = self.on_attach_behavior(ctypes.cast(pnm, ctypes.POINTER(SCN_ATTACH_BEHAVIOR)).contents)
        assert(rv is None or isinstance(rv, int))
        return 0 if rv is None else rv
    pass
