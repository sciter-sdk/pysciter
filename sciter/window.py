"""High level window wrapper."""

import ctypes

import sciter.scdef
import sciter.host
import sciter.behavior
import sciter.sctypes
import sciter.scplatform

_api = sciter.SciterAPI()


class Window(sciter.scplatform.BaseWindow, sciter.host.Host, sciter.behavior.EventHandler):
    """Basic Sciter window."""

    def __init__(self, ismain=False, ispopup=False, ischild=False, resizeable=True, parent=None, uni_theme=False, debug=True):
        """Create a new window and setup the sciter and dom callbacks."""
        super().__init__()

        flags = sciter.scdef.SCITER_CREATE_WINDOW_FLAGS.SW_CONTROLS
        if resizeable:
            flags = flags | sciter.scdef.SCITER_CREATE_WINDOW_FLAGS.SW_RESIZEABLE
        if ismain:
            flags = flags | sciter.scdef.SCITER_CREATE_WINDOW_FLAGS.SW_TITLEBAR
        elif ispopup:
            flags = flags | sciter.scdef.SCITER_CREATE_WINDOW_FLAGS.SW_POPUP
        elif ischild:
            flags = flags | sciter.scdef.SCITER_CREATE_WINDOW_FLAGS.SW_CHILD

        if uni_theme:
            _api.SciterSetOption(None, sciter.scdef.SCITER_RT_OPTIONS.SCITER_SET_UX_THEMING, True)

        if debug:
            flags = flags | sciter.scdef.SCITER_CREATE_WINDOW_FLAGS.SW_ENABLE_DEBUG

        self.window_flags = flags

        self.hwnd = self._create(flags, rect=None, parent=None)
        if not self.hwnd:
            raise sciter.SciterError("Could not create window")

        if debug:
            self.setup_debug()
        self.setup_callback(self.hwnd)
        self.attach(wnd=self.hwnd)
        pass

    pass
