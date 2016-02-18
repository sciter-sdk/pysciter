"""High level window wrapper."""

import ctypes
import sciter.scdef
import sciter.host
import sciter.behavior
import sciter.sctypes

_api = sciter.SciterAPI()


class Window(sciter.host.Host, sciter.behavior.EventHandler):
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

        rect = sciter.sctypes.RECT()
        self._wnd_handler_proc = sciter.scdef.SciterWindowDelegate(self._msg_delegate)
        self.hwnd = _api.SciterCreateWindow(flags, ctypes.byref(rect), self._wnd_handler_proc, None, parent)
        if not self.hwnd:
            raise sciter.SciterError("Could not create window")
        if debug:
            self.setup_debug()
        self.setup_callback(self.hwnd)
        self.attach(wnd=self.hwnd)
        pass

    def collapse(self, hide=False):
        """Minimize window."""
        ctypes.windll.user32.ShowWindow(self.hwnd, 0 if hide else 6)  # SW_HIDE or SW_MINIMIZE
        return self

    def expand(self, maximize=False):
        """Show or maximize window."""
        sw = 3 if maximize else 1  # SW_MAXIMIZE or SW_NORMAL
        ctypes.windll.user32.ShowWindow(self.hwnd, sw)
        return self

    def dismiss(self):
        """Close window."""
        ctypes.windll.user32.PostMessageW(self.hwnd, 0x0010, 0, 0)  # WM_CLOSE
        return self

    def run_app(self) -> int:
        """Run the main app message loop until window been closed."""
        msg = ctypes.wintypes.MSG()
        lpmsg = ctypes.pointer(msg)
        while ctypes.windll.user32.GetMessageW(lpmsg, 0, 0, 0) != 0:
            ctypes.windll.user32.TranslateMessage(lpmsg)
            ctypes.windll.user32.DispatchMessageW(lpmsg)
        return int(msg.wParam)

    # overrideable
    def document_close(self):
        # Quit application if main window was closed
        if self.window_flags & sciter.scdef.SCITER_CREATE_WINDOW_FLAGS.SW_TITLEBAR:
            ctypes.windll.user32.PostQuitMessage(0)
        super().document_close()
        pass

    def on_message(self, hwnd, msg, wparam, lparam):
        """Window message processing."""
        pass

    def _msg_delegate(self, hwnd, msg, wparam, lparam, pparam, phandled):
        rv = self.on_message(hwnd, msg, wparam, lparam)
        if rv is not None:
            phandled.contents = 1  # True
            return rv
        return 0

    pass
