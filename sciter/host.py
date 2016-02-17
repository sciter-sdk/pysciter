"""Sciter host application helpers."""

import ctypes
import sciter.value

from sciter.scdef import *
from sciter.scdom import HELEMENT, SCDOM_RESULT
from sciter.sctypes import HWINDOW

_api = sciter.SciterAPI()


class Host():
    """Standard implementation of SCITER_CALLBACK_NOTIFY handler."""

    def __init(self):
        self.hwnd = None
        self.root = None
        pass

    def __call__(self, name, *args):
        """Alias for self.call_function()."""
        return self.call_function(name, *args)

    def setup_callback(self, hwnd):
        """Set callback for sciter engine events."""
        self.hwnd = hwnd
        self.root = self.get_root() # if called on existing document
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
        ok = _api.SciterSetOption(self.hwnd, option, value)
        return ok != 0

    def set_home_url(self, url: str):
        """Set sciter home url."""
        ok = _api.SciterSetHomeURL(self.hwnd, url)
        return ok != 0

    def set_media_type(self, media_type: str):
        """Set media type of this sciter instance."""
        ok = _api.SciterSetMediaType(self.hwnd, media_type)
        return ok != 0

    def set_media_vars(self, media: dict):
        """Set media variables of this sciter instance."""
        v = sciter.Value(media)
        ok = _api.SciterSetMediaVars(self.hwnd, v)
        return ok != 0

    def set_master_css(self, css_str: str, append: bool):
        """Set Master style sheet."""
        utf = css_str.encode('utf-8')
        if append:
            ok = _api.SciterAppendMasterCSS(utf, len(utf))
        else:
            ok = _api.SciterSetMasterCSS(utf, len(utf))
        return ok != 0

    def set_css(self, css_str: str, base_url: str, media_type: str):
        """Set (reset) style sheet of current document."""
        utf = css_str.encode('utf-8')
        ok = _api.SciterSetCSS(self.hwnd, utf, len(utf), base_url, media_type)
        return ok != 0

    def get_hwnd(self) -> HWINDOW:
        """Get window handle."""
        return self.hwnd

    def load_file(self, uri: str):
        """Load HTML document from file."""
        ok = _api.SciterLoadFile(self.hwnd, uri)
        if ok:
            self.root = self.get_root()
        return ok != 0

    def load_html(self, html: bytes, uri=None):
        """Load HTML document from memory."""
        cb = len(html)
        pb = ctypes.c_char_p(html)
        ok = _api.SciterLoadHtml(self.hwnd, pb, cb, uri)
        if ok:
            self.root = self.get_root()
        return ok != 0

    def get_root(self) -> HELEMENT:
        """Get window root DOM element."""
        he = HELEMENT()
        ok = _api.SciterGetRootElement(self.hwnd, ctypes.byref(he))
        return he

    def eval_script(self, script: str):
        """Evaluate script in context of current document."""
        rv = sciter.Value()
        ok = _api.SciterEval(self.hwnd, script, len(script), rv)
        if not ok and rv.is_error_string():
            raise ScriptError(rv.get_value(), name)
        return rv

    def call_function(self, name: str, *args):
        """Call scripting function defined in the global namespace."""
        rv = sciter.Value()
        argc = len(args)
        args_type = sciter.value.SCITER_VALUE * argc
        argv = args_type()
        for i, v in enumerate(args):
            sv = sciter.Value(v)
            sv.copy_to(argv[i])
        cname = name.encode('utf-8')
        ok = _api.SciterCall(self.hwnd, cname, argc, argv, rv)
        if not ok and rv.is_error_string():
            raise ScriptError(rv.get_value(), name)
        return rv

    ## @name following functions can be overloaded
    def on_load_data(self, nm):
        """Notifies that Sciter is about to download a referred resource."""
        pass

    def on_data_loaded(self, nm):
        """This notification indicates that external data (for example image) download process completed."""
        pass

    def on_attach_behavior(self, nm):
        """This notification is sent on parsing the document and while processing elements having non empty `style.behavior` attribute value."""
        pass

    def on_debug_output(self, tag, subsystem, severity, text, text_len):
        """This output function will be used for reprting problems found while loading html and css documents."""
        sysname = OUTPUT_SUBSYTEMS(subsystem).name.lower()
        sevname = OUTPUT_SEVERITY(severity).name.lower()
        message = text[0:text_len].replace("\r", "\n").rstrip()
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
