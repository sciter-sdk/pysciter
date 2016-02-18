"""Platform-dependent code."""
import ctypes

import sciter
import sciter.scdef

from sciter.sctypes import *

_api = sciter.SciterAPI()

if SCITER_OS == 'win32':

    class WindowsWindow:
        """Win32 window."""

        def __init__(self):
            pass

        def _create(self, flags, rect, parent):
            if rect is None:
                rect = sciter.sctypes.RECT()
            self._msg_delegate = sciter.scdef.SciterWindowDelegate(self._on_msg_delegate)
            return _api.SciterCreateWindow(flags, ctypes.byref(rect), self._msg_delegate, None, parent)

        def collapse(self, hide=False):
            """Minimize or hide window."""
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

        def run_app(self):
            """Run the main app message loop until window been closed."""
            msg = MSG()
            pmsg = ctypes.pointer(msg)
            while ctypes.windll.user32.GetMessageW(pmsg, 0, 0, 0) != 0:
                ctypes.windll.user32.TranslateMessage(pmsg)
                ctypes.windll.user32.DispatchMessageW(pmsg)
            return int(msg.wParam)

        def quit_app(self, code=0):
            """Post quit message."""
            ctypes.windll.user32.PostQuitMessage(0)
            return self

        # overrideable
        def document_close(self):
            # Quit application if main window was closed
            if self.window_flags & sciter.scdef.SCITER_CREATE_WINDOW_FLAGS.SW_TITLEBAR:
                self.quit_app()
            super().document_close()
            pass

        def on_message(self, hwnd, msg, wparam, lparam):
            """Window message processing."""
            pass

        def _on_msg_delegate(self, hwnd, msg, wparam, lparam, pparam, phandled):
            rv = self.on_message(hwnd, msg, wparam, lparam)
            if rv is not None:
                phandled.contents = 1  # True
                return rv
            return 0

        pass

    BaseWindow = WindowsWindow


elif SCITER_OS == 'darwin':

    class OsxWindow:
        """."""

        def __init__(self):
            self._msg_delegate = None
            pass

        def _create(self, flags, rect, parent):
            # no delegate, no param
            return _api.SciterCreateWindow(flags, ctypes.byref(rect) if rect else None, None, None, parent)

        def collapse(self, hide=False):
            """Minimize or hide window."""
            return self

        def expand(self, maximize=False):
            """Show or maximize window."""
            return self

        def dismiss(self):
            """Close window."""
            return self

        def run_app(self):
            """Run the main app message loop until window been closed."""
            return 0

        def quit_app(self, code=0):
            """Post quit message."""
            return self

        pass

    BaseWindow = OsxWindow

elif SCITER_OS == 'linux':

    class LinuxWindow:
        """."""
        pass

    BaseWindow = LinuxWindow

pass
