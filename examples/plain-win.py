"""Sciter sample for Win32 API."""

# sciter import
from sciter import sapi
from sciter.scdef import *

# ctypes import
from ctypes import *
from ctypes.wintypes import *

# defs
WS_EX_APPWINDOW = 0x40000
WS_OVERLAPPEDWINDOW = 0xcf0000
WS_CAPTION = 0xc00000

SW_SHOWNORMAL = 1
SW_SHOW = 5

CS_HREDRAW = 2
CS_VREDRAW = 1

CW_USEDEFAULT = 0x80000000

WM_DESTROY = 2

WHITE_BRUSH = 0

IDC_ARROW = 31514

WNDPROCTYPE = WINFUNCTYPE(c_int, HWND, c_uint, WPARAM, LPARAM)


class WNDCLASSEX(Structure):
    _fields_ = [
        ("cbSize", c_uint),
        ("style", c_uint),
        ("lpfnWndProc", WNDPROCTYPE),
        ("cbClsExtra", c_int),
        ("cbWndExtra", c_int),
        ("hInstance", HANDLE),
        ("hIcon", HANDLE),
        ("hCursor", HANDLE),
        ("hBrush", HANDLE),
        ("lpszMenuName", LPCWSTR),
        ("lpszClassName", LPCWSTR),
        ("hIconSm", HANDLE)]


def on_load_data(ld):
    """Custom documents loader, just for example."""
    uri = ld.uri
    uri = uri
    return 0


def on_create_behavior(ld):
    """Custom behavior factory, just for example."""
    name = ld.behaviorName
    name = name
    return 0


def on_sciter_callback(pld, param):
    """Sciter notifications callback."""
    ld = pld.contents
    if ld.code == SciterNotification.SC_LOAD_DATA:
        return on_load_data(cast(pld, POINTER(SCN_LOAD_DATA)).contents)
    elif ld.code == SciterNotification.SC_ATTACH_BEHAVIOR:
        return on_create_behavior(cast(pld, POINTER(SCN_ATTACH_BEHAVIOR)).contents)
    return 0


def on_wnd_message(hWnd, Msg, wParam, lParam):
    """WindowProc Function."""
    handled = BOOL(0)
    lr = sapi.SciterProcND(hWnd, Msg, wParam, lParam, byref(handled))
    if handled:
        return lr

    if Msg == WM_DESTROY:
        windll.user32.PostQuitMessage(0)
        return 0

    try:
        return windll.user32.DefWindowProcW(hWnd, Msg, wParam, lParam)
    except:
        # etype, evalue, estack = sys.exc_info()
        print("WndProc exception: %X, 0x%04X, 0x%X, 0x%X" % (hWnd, Msg, wParam, lParam))
        # traceback.print_exception(etype, evalue, estack)
    return 0


def main():
    clsname = sapi.SciterClassName()
    title = u"Win32 Sciter"
    clsname = u"PySciter"

    WndProc = WNDPROCTYPE(on_wnd_message)
    wndClass = WNDCLASSEX()
    wndClass.cbSize = sizeof(WNDCLASSEX)
    wndClass.style = CS_HREDRAW | CS_VREDRAW
    wndClass.lpfnWndProc = WndProc
    wndClass.cbClsExtra = 0
    wndClass.cbWndExtra = 0
    wndClass.hInstance = windll.kernel32.GetModuleHandleW(0)
    wndClass.hIcon = 0
    wndClass.hCursor = windll.user32.LoadCursorW(0, IDC_ARROW)
    wndClass.hBrush = windll.gdi32.GetStockObject(WHITE_BRUSH)
    wndClass.lpszMenuName = 0
    wndClass.lpszClassName = clsname
    wndClass.hIconSm = 0

    if not windll.user32.RegisterClassExW(byref(wndClass)):
        err = windll.kernel32.GetLastError()
        print('Failed to register window: ', err)
        exit(0)

    hWnd = windll.user32.CreateWindowExW(0, clsname, title, WS_OVERLAPPEDWINDOW, CW_USEDEFAULT, CW_USEDEFAULT, 800, 600, 0, 0, 0, 0)
    if not hWnd:
        err = windll.kernel32.GetLastError()
        print('Failed to create window: ', err)
        exit(0)

    scproc = SciterHostCallback(on_sciter_callback)
    sapi.SciterSetCallback(hWnd, scproc, None)

    url = u"examples/minimal.htm"
    sapi.SciterLoadFile(hWnd, url)

    windll.user32.ShowWindow(hWnd, SW_SHOW)
    windll.user32.UpdateWindow(hWnd)

    msg = MSG()
    lpmsg = pointer(msg)

    print('Entering message loop')
    while windll.user32.GetMessageW(lpmsg, 0, 0, 0) != 0:
        windll.user32.TranslateMessage(lpmsg)
        windll.user32.DispatchMessageW(lpmsg)

    print('Quit.')

if __name__ == '__main__':
    main()
