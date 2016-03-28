"""High level window wrapper."""

import sciter.capi.scdef
import sciter.capi.sctypes
import sciter.host
import sciter.event
import sciter.platform

_api = sciter.SciterAPI()


class Window(sciter.platform.BaseWindow, sciter.host.Host, sciter.event.EventHandler):
    """Basic Sciter window."""

    def __init__(self, ismain=False, ispopup=False, ischild=False, resizeable=True, parent=None, uni_theme=False, debug=True):
        """Create a new window and setup the sciter and dom callbacks."""
        super().__init__()
        from sciter.capi.scdef import SCITER_CREATE_WINDOW_FLAGS

        flags = SCITER_CREATE_WINDOW_FLAGS.SW_CONTROLS
        if resizeable:
            flags = flags | SCITER_CREATE_WINDOW_FLAGS.SW_RESIZEABLE
        if ismain:
            flags = flags | SCITER_CREATE_WINDOW_FLAGS.SW_MAIN | SCITER_CREATE_WINDOW_FLAGS.SW_TITLEBAR
        elif ispopup:
            flags = flags | SCITER_CREATE_WINDOW_FLAGS.SW_POPUP
        elif ischild:
            flags = flags | SCITER_CREATE_WINDOW_FLAGS.SW_CHILD

        if uni_theme:
            _api.SciterSetOption(None, sciter.capi.scdef.SCITER_RT_OPTIONS.SCITER_SET_UX_THEMING, True)

        if debug:
            flags = flags | SCITER_CREATE_WINDOW_FLAGS.SW_ENABLE_DEBUG
            self.setup_debug()
        self.window_flags = flags
        self._title_changed = False
        self.hwnd = self._create(flags, rect=None, parent=None)
        if not self.hwnd:
            raise sciter.SciterError("Could not create window")

        self.setup_callback(self.hwnd)
        self.attach(window=self.hwnd)
        pass

    def collapse(self, hide=False):
        """Minimize or hide window."""
        return super().collapse(hide)

    def expand(self, maximize=False):
        """Show or maximize window."""
        return super().expand(maximize)

    def dismiss(self):
        """Close window."""
        return super().dismiss()

    def set_title(self, title: str):
        """Set native window title."""
        self._title_changed = True
        return super().set_title(title)

    def get_title(self):
        """Get native window title."""
        return super().get_title()

    def run_app(self, show=True):
        """Show window and run the main app message loop until window been closed."""
        if show:
            self.expand()
        ret = super().run_app()
        return ret

    def quit_app(self, code=0):
        """Post quit message."""
        return super().quit_app(code)

    # overrideable
    def _document_ready(self, target):
        # Set window title based on <title> content, if any
        if self._title_changed:
            return
        root = sciter.Element(target)
        title = root.find_first('html > head > title')
        if title:
            self.set_title(title.get_text())
        pass

    pass
