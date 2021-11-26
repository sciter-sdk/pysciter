"""Platform-dependent code."""
import ctypes

import sciter
import sciter.capi.scdef

from sciter.capi.sctypes import *

_api = sciter.SciterAPI()

if SCITER_WIN:

    class WindowsWindow:
        """Win32 window."""

        _initialized = False

        def __init__(self):
            super().__init__()
            self.hwnd = None
            pass

        def _create(self, flags, rect, parent):
            if not WindowsWindow._initialized:
                ctypes.windll.ole32.OleInitialize(None)
                WindowsWindow._initialized = True
            if rect is None:
                rect = sciter.capi.sctypes.RECT()
            self._msg_delegate = sciter.capi.scdef.SciterWindowDelegate(self._on_msg_delegate)
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

        def set_title(self, title: str):
            """Set native window title."""
            ctypes.windll.user32.SetWindowTextW(self.hwnd, title)
            return self

        def get_title(self):
            """Get native window title."""
            cb = ctypes.windll.user32.GetWindowTextLengthW(self.hwnd) + 1
            title = ctypes.create_unicode_buffer(cb)
            ctypes.windll.user32.GetWindowTextW(self.hwnd, title, cb)
            return title

        def minimal_menu(self):
            pass

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

        def on_message(self, hwnd, msg, wparam, lparam):
            """Window message processing."""
            pass

        def _on_msg_delegate(self, hwnd, msg, wparam, lparam, pparam, phandled):
            # pylint: disable=assignment-from-none,assignment-from-no-return
            # because the `self.on_` methods can be overloaded
            rv = self.on_message(hwnd, msg, wparam, lparam)
            if rv is not None:
                phandled.contents = 1  # True
                return rv
            return 0

        pass

    BaseWindow = WindowsWindow


elif SCITER_OSX:

    class OsxWindow:
        """Mac OS X Window (Cocoa backend)."""

        def __init__(self):
            super().__init__()
            self.objc = ObjC()
            self.nsApp = None
            self.hwnd = None
            self.window_flags = None

            NSApplication = self.objc.getClass('NSApplication')
            self.nsApp = self.objc(NSApplication, 'sharedApplication')
            pass

        def _create(self, flags, rect, parent):
            # no delegate, no param
            wnd = _api.SciterCreateWindow(flags, ctypes.byref(rect) if rect else None, None, None, parent)
            return wnd

        def _window(self, hwnd=None):
            if hwnd is None:
                hwnd = self.hwnd
            wnd = self.objc(hwnd, 'window')
            return wnd

        def collapse(self, hide=False):
            """Minimize or hide window."""
            wnd = self._window()
            if hide:
                self.objc(wnd, 'orderOut:', None)
            else:
                self.objc(wnd, 'performMiniaturize:', self.hwnd)
            return self

        def expand(self, maximize=False):
            """Show or maximize window."""
            wnd = self._window()
            if self.window_flags & sciter.capi.scdef.SCITER_CREATE_WINDOW_FLAGS.SW_TITLEBAR:
                # bring the main window foreground
                self.objc(self.nsApp, 'activateIgnoringOtherApps:', True)
            self.objc(wnd, 'makeKeyAndOrderFront:', None)
            if maximize:
                self.objc(wnd, 'performZoom:', None)
            return self

        def dismiss(self):
            """Close window."""
            self.objc(self._window(), 'close')
            return self

        def set_title(self, title: str):
            """Set native window title."""
            self.objc(self._window(), 'setTitle:', self.objc.toNSString(title))
            return self

        def get_title(self):
            """Get native window title."""
            nstitle = self.objc(self._window(), 'title')
            return self.objc.fromNSString(nstitle)

        def minimal_menu(self):
            NSMenu = self.objc.getClass('NSMenu')
            NSMenuItem = self.objc.getClass('NSMenuItem')

            menubar = self.objc.alloc(NSMenu)
            menubar_item = self.objc.alloc(NSMenuItem)

            self.objc(menubar, 'addItem:', menubar_item)
            self.objc(self.nsApp, 'setMainMenu:', menubar)

            title = self.objc.toNSString('Quit')
            key = self.objc.toNSString('q')
            action = ctypes.c_void_p(self.objc.getSEL('terminate:'))

            quit = self.objc(self.objc(NSMenuItem, 'alloc'), 'initWithTitle:action:keyEquivalent:', title, action, key)
            self.objc(quit, 'autorelease')

            appmenu = self.objc.alloc(NSMenu)
            self.objc(appmenu, 'addItem:', quit)
            self.objc(menubar_item, 'setSubmenu:', appmenu)

            pass

        def run_app(self):
            """Run the main app message loop until window been closed."""
            self.objc(self.nsApp, 'run')
            return 0

        def quit_app(self, code=0):
            """Post quit message."""
            if self.nsApp:
                self.objc(self.nsApp, 'terminate:', self.nsApp)
            return self

        pass

    BaseWindow = OsxWindow

    # objc interop
    class ObjC():
        """."""

        def __init__(self):
            import ctypes.util

            objc = ctypes.cdll.LoadLibrary(ctypes.util.find_library('objc'))

            self.appkit = ctypes.cdll.LoadLibrary(ctypes.util.find_library('AppKit'))
            self.cf = ctypes.cdll.LoadLibrary(ctypes.util.find_library('CoreFoundation'))

            # struct objc_object *id;
            # struct objc_selector *SEL;
            # struct objc_class *Class;

            # ABI:
            # const char *object_getClassName(id obj)
            objc.objc_getClass.restype = ctypes.c_void_p
            objc.objc_getClass.argtypes = [ctypes.c_char_p]

            # SEL sel_registerName(const char *str)
            objc.sel_registerName.restype = ctypes.c_void_p
            objc.sel_registerName.argtypes = [ctypes.c_char_p]

            # BOOL class_respondsToSelector(Class cls, SEL sel)
            objc.class_respondsToSelector.restype = ctypes.c_bool
            objc.class_respondsToSelector.argtypes = [ctypes.c_void_p, ctypes.c_void_p]

            # id objc_msgSend(id self, SEL op, ...)
            objc.objc_msgSend.restype = ctypes.c_void_p
            objc.objc_msgSend.argtypes = [ctypes.c_void_p, ctypes.c_void_p]

            self.dll = objc

            #  const char * CFStringGetCStringPtr ( CFStringRef theString, CFStringEncoding encoding );
            self.cf.CFStringGetCStringPtr.restype = ctypes.c_char_p
            self.cf.CFStringGetCStringPtr.argtypes = [ctypes.c_void_p, ctypes.c_uint]

            #  const UniChar * CFStringGetCharactersPtr ( CFStringRef theString );
            self.cf.CFStringGetCharactersPtr.restype = ctypes.c_char_p
            self.cf.CFStringGetCharactersPtr.argtypes = [ctypes.c_void_p]

            # CFStringGetLength
            self.cf.CFStringGetLength.restype = ctypes.c_int
            self.cf.CFStringGetLength.argtypes = [ctypes.c_void_p]

            # Boolean CFStringGetCString ( CFStringRef theString, char *buffer, CFIndex bufferSize, CFStringEncoding encoding );
            self.cf.CFStringGetCString.restype = ctypes.c_bool
            self.cf.CFStringGetCString.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_int, ctypes.c_uint]

            #  CFStringRef CFStringCreateWithCString ( CFAllocatorRef alloc, const char *cStr, CFStringEncoding encoding );
            self.cf.CFStringCreateWithCString.restype = ctypes.c_void_p
            self.cf.CFStringCreateWithCString.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_uint32]
            pass

        def fromNSString(self, nsString):
            if not nsString:
                return '<nil>'

            kCFStringEncodingUTF8 = 0x08000100

            n = self.cf.CFStringGetLength(nsString)
            buf = ctypes.create_string_buffer(n * 4 + 4)
            ok = self.cf.CFStringGetCString(nsString, buf, n * 4, kCFStringEncodingUTF8)
            return buf.value.decode('utf-8') if ok else None

        def toNSString(self, string: str):
            kCFStringEncodingUTF8 = 0x08000100
            return ctypes.c_void_p(self.cf.CFStringCreateWithCString(None, string.encode('utf-8'), kCFStringEncodingUTF8))

        def getClass(self, name):
            # NSSound = objc.getClass('NSSound')
            return ctypes.c_void_p(self.dll.objc_getClass(name.encode('utf-8')))

        def new(self, cls):
            # sound = objc.new(NSSound)
            return self.call(self.call(cls, 'alloc'), 'init')

        def alloc(self, cls):
            # sound = objc.alloc(NSSound)
            return self.call(self.call(cls, 'new'), 'autorelease')

        def getSEL(self, name):
            return self.dll.sel_registerName(name.encode('utf-8'))

        def hasSEL(self, name, className):
            sel = self.getSEL(name) if isinstance(name, str) else name
            cls = self.getClass(className) if isinstance(className, str) else className
            return self.dll.class_respondsToSelector(cls, sel)

        def __call__(self, obj, method, *args, **kwargs):
            return self.call(obj, method, *args, **kwargs)

        def call(self, obj, method, *args, **kwargs):
            # objc.call(NSSound, 'alloc')
            # NB: `objc_msgSend.argtypes` has only 2 arguments specified.
            # Extra args should be `c_void_p`!

            restype = kwargs.get('cast', ctypes.c_void_p)
            typename = kwargs.get('type')
            if typename is not None and hasattr(ctypes, typename):
                restype = getattr(ctypes, typename)
            sel = self.getSEL(method)
            r = self.dll.objc_msgSend(obj, sel, *args)
            return ctypes.cast(r, restype)

        pass


elif SCITER_LNX:

    def _init_lib():
        if hasattr(_init_lib, '_dll'):
            return _init_lib._dll

        import ctypes.util
        lib = ctypes.cdll.LoadLibrary(ctypes.util.find_library('gtk-3'))
        _init_lib._dll = lib

        lib.gtk_widget_get_toplevel.restype = LPCVOID
        lib.gtk_widget_get_toplevel.argtypes = [LPCVOID]

        lib.gtk_init.argtypes = [LPCVOID, LPCVOID]
        lib.gtk_widget_get_toplevel.argtypes = [LPCVOID]
        lib.gtk_widget_hide.argtypes = [LPCVOID]
        lib.gtk_window_iconify.argtypes = [LPCVOID]
        lib.gtk_window_maximize.argtypes = [LPCVOID]
        lib.gtk_window_present.argtypes = [LPCVOID]
        lib.gtk_window_close.argtypes = [LPCVOID]
        lib.gtk_window_get_title.argtypes = [LPCVOID]
        lib.gtk_window_set_title.argtypes = [LPCVOID, LPCSTR]
        lib.gtk_main.argtypes = []
        lib.gtk_main_quit.argtypes = []

        lib.gtk_init(None, None)
        return lib

    #
    class LinuxWindow:
        """Linux window (GTK3 backend)."""

        def __init__(self):
            super().__init__()
            self.hwnd = None
            self._gtk = _init_lib()
            pass

        def _create(self, flags, rect, parent):
            # no delegate, no param
            wnd = _api.SciterCreateWindow(flags, ctypes.byref(rect) if rect else None, None, None, parent)
            return wnd

        def _window(self, hwnd=None):
            if hwnd is None:
                hwnd = self.hwnd
            wnd = self._gtk.gtk_widget_get_toplevel(hwnd)
            return wnd

        def collapse(self, hide=False):
            """Minimize or hide window."""
            if hide:
                self._gtk.gtk_widget_hide(self.hwnd)
            else:
                self._gtk.gtk_window_iconify(self._window())
            return self

        def expand(self, maximize=False):
            """Show or maximize window."""
            wnd = self._window()
            if maximize:
                self._gtk.gtk_window_maximize(wnd)
            else:
                self._gtk.gtk_window_present(wnd)
            return self

        def dismiss(self):
            """Close window."""
            self._gtk.gtk_window_close(self._window())
            return self

        def set_title(self, title: str):
            """Set native window title."""
            self._gtk.gtk_window_set_title(self._window(), title.encode('utf-8'))
            return self

        def get_title(self):
            """Get native window title."""
            self._gtk.gtk_window_get_title.restype = ctypes.c_char_p
            return self._gtk.gtk_window_get_title(self._window()).decode('utf-8')

        def minimal_menu(self):
            pass

        def run_app(self):
            """Run the main app message loop until window been closed."""
            self._gtk.gtk_main()
            return 0

        def quit_app(self, code=0):
            """Post quit message."""
            self._gtk.gtk_main_quit()
            return self

        pass

    BaseWindow = LinuxWindow

pass
