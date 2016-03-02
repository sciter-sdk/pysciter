"""C interface for behaviors support (a.k.a windowless controls)."""

import enum
import ctypes

from sciter.capi.scdom import HELEMENT
from sciter.capi.scvalue import SCITER_VALUE
from sciter.capi.scgraphics import HGFX
from sciter.capi.sctypes import *

import sciter.capi.sctiscript as sctiscript


class EVENT_GROUPS(enum.IntEnum):
    """event groups."""
    HANDLE_INITIALIZATION = 0x0000  # attached/detached */
    HANDLE_MOUSE = 0x0001           # mouse events */
    HANDLE_KEY = 0x0002             # key events */
    HANDLE_FOCUS = 0x0004           # focus events  if this flag is set it also means that element it attached to is focusable */
    HANDLE_SCROLL = 0x0008          # scroll events */
    HANDLE_TIMER = 0x0010           # timer event */
    HANDLE_SIZE = 0x0020            # size changed event */
    HANDLE_DRAW = 0x0040            # drawing request (event) */
    HANDLE_DATA_ARRIVED = 0x080     # requested data () has been delivered */
    HANDLE_BEHAVIOR_EVENT = 0x0100  # logical, synthetic events: BUTTON_CLICK, HYPERLINK_CLICK, etc., a.k.a. notifications from intrinsic behaviors */
    HANDLE_METHOD_CALL = 0x0200     # behavior specific methods */
    HANDLE_SCRIPTING_METHOD_CALL = 0x0400  # behavior specific methods */
    HANDLE_TISCRIPT_METHOD_CALL = 0x0800   # behavior specific methods using direct tiscript::value's */
    HANDLE_EXCHANGE = 0x1000  # system drag-n-drop */
    HANDLE_GESTURE = 0x2000  # touch input events */
    HANDLE_ALL = 0xFFFF  # all of them */
    SUBSCRIPTIONS_REQUEST = 0xFFFFFFFF  # special value for getting subscription flags */


class PHASE_MASK(enum.IntEnum):
    """."""
    BUBBLING = 0
    SINKING = 0x8000
    HANDLED = 0x10000
    SINKING_HANDLED = HANDLED|SINKING

class MOUSE_BUTTONS(enum.IntEnum):
    """."""
    MAIN_MOUSE_BUTTON = 1
    PROP_MOUSE_BUTTON = 2
    MIDDLE_MOUSE_BUTTON = 4


class KEYBOARD_STATES(enum.IntEnum):
    CONTROL_KEY_PRESSED = 0x1
    SHIFT_KEY_PRESSED = 0x2
    ALT_KEY_PRESSED = 0x4


class INITIALIZATION_EVENTS(enum.IntEnum):
    BEHAVIOR_DETACH = 0
    BEHAVIOR_ATTACH = 1


class INITIALIZATION_PARAMS(ctypes.Structure):
    _fields_ = [
        ("cmd", UINT),  # INITIALIZATION_EVENTS
    ]


class DRAGGING_TYPE(enum.IntEnum):
    NO_DRAGGING = 0
    DRAGGING_MOVE = 1
    DRAGGING_COPY = 2


class MOUSE_EVENTS(enum.IntEnum):
    (MOUSE_ENTER,
    MOUSE_LEAVE,
    MOUSE_MOVE,
    MOUSE_UP,
    MOUSE_DOWN,
    MOUSE_DCLICK,
    MOUSE_WHEEL,
    MOUSE_TICK,
    MOUSE_IDLE,
    DROP,
    DRAG_ENTER,
    DRAG_LEAVE,
    DRAG_REQUEST) = range(13)

    MOUSE_CLICK = 0xFF
    DRAGGING = 0x100


class MOUSE_PARAMS(ctypes.Structure):
    _fields_ = [
        ("cmd", UINT),           # MOUSE_EVENTS
        ("target", HELEMENT),        # target element
        ("pos", POINT),           # position of cursor, element relative
        ("pos_view", POINT),      # position of cursor, view relative
        ("button_state", UINT),  # MOUSE_BUTTONS
        ("alt_state", UINT),     # KEYBOARD_STATES
        ("cursor_type", UINT),   # CURSOR_TYPE to set, see CURSOR_TYPE
        ("is_on_icon", BOOL),    # mouse is over icon (foreground-image, foreground-repeat:no-repeat)
        ("dragging", HELEMENT),      # element that is being dragged over, this field is not NULL if (cmd & DRAGGING) != 0
        ("dragging_mode", UINT), # see DRAGGING_TYPE. 
    ]


class CURSOR_TYPE(enum.IntEnum):
    (CURSOR_ARROW,
    CURSOR_IBEAM,
    CURSOR_WAIT,
    CURSOR_CROSS,
    CURSOR_UPARROW,
    CURSOR_SIZENWSE,
    CURSOR_SIZENESW,
    CURSOR_SIZEWE,
    CURSOR_SIZENS,
    CURSOR_SIZEALL,
    CURSOR_NO,
    CURSOR_APPSTARTING,
    CURSOR_HELP,
    CURSOR_HAND,
    CURSOR_DRAG_MOVE,
    CURSOR_DRAG_COPY) = range(16)


class KEY_EVENTS(enum.IntEnum):
    KEY_DOWN = 0
    KEY_UP = 1
    KEY_CHAR = 2


class KEY_PARAMS(ctypes.Structure):
    _fields_ = [
        ("cmd", UINT),           # KEY_EVENTS
        ("target", HELEMENT),        # target element
        ("key_code", UINT),      # key scan code, or character unicode for KEY_CHAR
        ("alt_state", UINT),     # KEYBOARD_STATES
    ]


class FOCUS_EVENTS(enum.IntEnum):
    FOCUS_LOST = 0  # non-bubbling event, target is new focus element
    FOCUS_GOT = 1   # non-bubbling event, target is old focus element
    FOCUS_IN = 2    # bubbling event/notification, target is an element that got focus
    FOCUS_OUT = 3   # bubbling event/notification, target is an element that lost focus


class FOCUS_PARAMS(ctypes.Structure):
    _fields_ = [
        ("cmd", UINT),           # FOCUS_EVENTS
        ("target", HELEMENT),        # target element, for FOCUS_LOST it is a handle of new focus element
                                 #    and for FOCUS_GOT it is a handle of old focus element, can be NULL
        ("by_mouse_click", BOOL),  # true if focus is being set by mouse click
        ("cancel", BOOL),          # in FOCUS_LOST phase setting this field to true will cancel transfer focus from old element to the new one.
    ]


class SCROLL_EVENTS(enum.IntEnum):
    (SCROLL_HOME,
    SCROLL_END,
    SCROLL_STEP_PLUS,
    SCROLL_STEP_MINUS,
    SCROLL_PAGE_PLUS,
    SCROLL_PAGE_MINUS,
    SCROLL_POS,
    SCROLL_SLIDER_RELEASED,
    SCROLL_CORNER_PRESSED,
    SCROLL_CORNER_RELEASED) = range(10)


class SCROLL_PARAMS(ctypes.Structure):
    _fields_ = [
        ("cmd", UINT),           # SCROLL_EVENTS
        ("target", HELEMENT),        # target element
        ("pos", INT),           # scroll position if SCROLL_POS
        ("vertical", BOOL),      # true if from vertical scrollbar
    ]


class GESTURE_CMD(enum.IntEnum):
    (GESTURE_REQUEST,  # return true and fill flags if it will handle gestures.
    GESTURE_ZOOM,         # The zoom gesture.
    GESTURE_PAN,          # The pan gesture.
    GESTURE_ROTATE,       # The rotation gesture.
    GESTURE_TAP1,         # The tap gesture.
    GESTURE_TAP2) = range(6)   # The two-finger tap gesture.


class GESTURE_STATE(enum.IntEnum):
    GESTURE_STATE_BEGIN = 1     # starts
    GESTURE_STATE_INERTIA = 2   # events generated by inertia processor
    GESTURE_STATE_END = 4       # end, last event of the gesture sequence


class GESTURE_TYPE_FLAGS(enum.IntEnum):
    GESTURE_FLAG_ZOOM               = 0x0001
    GESTURE_FLAG_ROTATE             = 0x0002
    GESTURE_FLAG_PAN_VERTICAL       = 0x0004
    GESTURE_FLAG_PAN_HORIZONTAL     = 0x0008
    GESTURE_FLAG_TAP1               = 0x0010   # press & tap
    GESTURE_FLAG_TAP2               = 0x0020   # two fingers tap

    GESTURE_FLAG_PAN_WITH_GUTTER    = 0x4000   # PAN_VERTICAL and PAN_HORIZONTAL modifiers
    GESTURE_FLAG_PAN_WITH_INERTIA   = 0x8000   #
    GESTURE_FLAGS_ALL               = 0xFFFF   #


class GESTURE_PARAMS(ctypes.Structure):
    _fields_ = [
        ("cmd", UINT),           # GESTURE_EVENTS
        ("target", HELEMENT),        # target element
        ("pos", POINT),           # position of cursor, element relative
        ("pos_view", POINT),      # position of cursor, view relative
        ("flags", UINT),         # for GESTURE_REQUEST combination of GESTURE_FLAGs.
                             # for others it is a combination of GESTURE_STATe's
        ("delta_time", UINT),    # period of time from previous event.
        ("delta_xy", SIZE),      # for GESTURE_PAN it is a direction vector
        ("delta_v", c_double),       # for GESTURE_ROTATE - delta angle (radians)
                             # for GESTURE_ZOOM - zoom value, is less or greater than 1.0
    ]


class DRAW_EVENTS(enum.IntEnum):
    DRAW_BACKGROUND = 0
    DRAW_CONTENT = 1
    DRAW_FOREGROUND = 2


class DRAW_PARAMS(ctypes.Structure):
    _fields_ = [
        ("cmd", UINT),        # DRAW_EVENTS
        ("gfx", HGFX),        # hdc to paint on
        ("area", RECT),       # element area, to get invalid area to paint use GetClipBox,
        ("reserved", UINT),   # for DRAW_BACKGROUND/DRAW_FOREGROUND - it is a border box
    ]                         # for DRAW_CONTENT - it is a content box


class CONTENT_CHANGE_BITS(enum.IntEnum):
    CONTENT_ADDED = 0x01
    CONTENT_REMOVED = 0x02


class BEHAVIOR_EVENTS(enum.IntEnum):
    """Behavior event code."""
    BUTTON_CLICK = 0               # click on button
    BUTTON_PRESS = 1               # mouse down or key down in button
    BUTTON_STATE_CHANGED = 2       # checkbox/radio/slider changed its state/value
    EDIT_VALUE_CHANGING = 3        # before text change
    EDIT_VALUE_CHANGED = 4         # after text change
    SELECT_SELECTION_CHANGED = 5   # selection in <select> changed
    SELECT_STATE_CHANGED = 6       # node in select expanded/collapsed, heTarget is the node

    POPUP_REQUEST   = 7            # request to show popup just received,
                                  #     here DOM of popup element can be modifed.
    POPUP_READY     = 8            # popup element has been measured and ready to be shown on screen,
                                  #     here you can use functions like ScrollToView.
    POPUP_DISMISSED = 9            # popup element is closed,
                                  #     here DOM of popup element can be modifed again - e.g. some items can be removed
                                  #     to free memory.

    MENU_ITEM_ACTIVE = 0xA         # menu item activated by mouse hover or by keyboard,
    MENU_ITEM_CLICK = 0xB          # menu item click,
                                  #   BEHAVIOR_EVENT_PARAMS structure layout
                                  #   BEHAVIOR_EVENT_PARAMS.cmd - MENU_ITEM_CLICK/MENU_ITEM_ACTIVE
                                  #   BEHAVIOR_EVENT_PARAMS.heTarget - owner(anchor) of the menu
                                  #   BEHAVIOR_EVENT_PARAMS.he - the menu item, presumably <li> element
                                  #   BEHAVIOR_EVENT_PARAMS.reason - BY_MOUSE_CLICK | BY_KEY_CLICK

    CONTEXT_MENU_REQUEST = 0x10    # "right-click", BEHAVIOR_EVENT_PARAMS::he is current popup menu HELEMENT being processed or NULL.
                                  # application can provide its own HELEMENT here (if it is NULL) or modify current menu element.

    VISIUAL_STATUS_CHANGED = 0x11  # broadcast notification, sent to all elements of some container being shown or hidden
    DISABLED_STATUS_CHANGED = 0x12 # broadcast notification, sent to all elements of some container that got new value of :disabled state

    POPUP_DISMISSING = 0x13        # popup is about to be closed

    CONTENT_CHANGED = 0x15         # content has been changed, is posted to the element that gets content changed,  reason is combination of CONTENT_CHANGE_BITS.
                                  # target == NULL means the window got new document and this event is dispatched only to the window.

    CLICK = 0x16                   # generic click
    CHANGE = 0x17                  # generic change

    # "grey" event codes  - notfications from behaviors from this SDK
    HYPERLINK_CLICK = 0x80         # hyperlink click

    ELEMENT_COLLAPSED = 0x90       # element was collapsed, so far only behavior:tabs is sending these two to the panels
    ELEMENT_EXPANDED = 0x91        # element was expanded,

    ACTIVATE_CHILD = 0x92          # activate (select) child,
                                 # used for example by accesskeys behaviors to send activation request, e.g. tab on behavior:tabs.

    INIT_DATA_VIEW = 0x93          # request to virtual grid to initialize its view

    ROWS_DATA_REQUEST = 0x94       # request from virtual grid to data source behavior to fill data in the table
                                 # parameters passed throug DATA_ROWS_PARAMS structure.

    UI_STATE_CHANGED = 0x95        # ui state changed, observers shall update their visual states.
                                 # is sent for example by behavior:richtext when caret position/selection has changed.

    FORM_SUBMIT = 0x96             # behavior:form detected submission event. BEHAVIOR_EVENT_PARAMS::data field contains data to be posted.
                                 # BEHAVIOR_EVENT_PARAMS::data is of type T_MAP in this case key/value pairs of data that is about 
                                 # to be submitted. You can modify the data or discard submission by returning true from the handler.
    FORM_RESET = 0x97              # behavior:form detected reset event (from button type=reset). BEHAVIOR_EVENT_PARAMS::data field contains data to be reset.
                                 # BEHAVIOR_EVENT_PARAMS::data is of type T_MAP in this case key/value pairs of data that is about 
                                 # to be rest. You can modify the data or discard reset by returning true from the handler.

    DOCUMENT_COMPLETE = 0x98       # document in behavior:frame or root document is complete.

    HISTORY_PUSH = 0x99            # requests to behavior:history (commands)
    HISTORY_DROP = 0x9A
    HISTORY_PRIOR = 0x9B
    HISTORY_NEXT = 0x9C
    HISTORY_STATE_CHANGED = 0x9D   # behavior:history notification - history stack has changed

    CLOSE_POPUP = 0x9E             # close popup request,
    REQUEST_TOOLTIP = 0x9F         # request tooltip, evt.source <- is the tooltip element.

    ANIMATION         = 0xA0       # animation started (reason=1) or ended(reason=0) on the element.

    DOCUMENT_CREATED  = 0xC0       # document created, script namespace initialized. target -> the document
    DOCUMENT_CLOSE_REQUEST = 0xC1  # document is about to be closed, to cancel closing do: evt.data = sciter::value("cancel");
    DOCUMENT_CLOSE    = 0xC2       # last notification before document removal from the DOM
    DOCUMENT_READY    = 0xC3       # document has got DOM structure, styles and behaviors of DOM elements. Script loading run is complete at this moment. 

    VIDEO_INITIALIZED = 0xD1       # <video> "ready" notification
    VIDEO_STARTED     = 0xD2       # <video> playback started notification
    VIDEO_STOPPED     = 0xD3       # <video> playback stoped/paused notification
    VIDEO_BIND_RQ     = 0xD4       # <video> request for frame source binding,
                                 #   If you want to provide your own video frames source for the given target <video> element do the following:
                                 #   1. Handle and consume this VIDEO_BIND_RQ request
                                 #   2. You will receive second VIDEO_BIND_RQ request/event for the same <video> element
                                 #      but this time with the 'reason' field set to an instance of sciter::video_destination interface.
                                 #   3. add_ref() it and store it for example in worker thread producing video frames.
                                 #   4. call sciter::video_destination::start_streaming(...) providing needed parameters
                                 #      call sciter::video_destination::render_frame(...) as soon as they are available
                                 #      call sciter::video_destination::stop_streaming() to stop the rendering (a.k.a. end of movie reached)

    PAGINATION_STARTS  = 0xE0      # behavior:pager starts pagination
    PAGINATION_PAGE    = 0xE1      # behavior:pager paginated page no, reason -> page no
    PAGINATION_ENDS    = 0xE2      # behavior:pager end pagination, reason -> total pages

    FIRST_APPLICATION_EVENT_CODE = 0x100
    # all custom event codes shall be greater
    # than this number. All codes below this will be used
    # solely by application - HTMLayout will not intrepret it
    # and will do just dispatching.
    # To send event notifications with  these codes use
    # HTMLayoutSend/PostEvent API.


class EVENT_REASON(enum.IntEnum):
    BY_MOUSE_CLICK = 0
    BY_KEY_CLICK = 1
    SYNTHESIZED = 2  # synthesized, programmatically generated.


class EDIT_CHANGED_REASON(enum.IntEnum):
    BY_INS_CHAR = 0   # single char insertion
    BY_INS_CHARS = 1  # character range insertion, clipboard
    BY_DEL_CHAR = 2   # single char deletion
    BY_DEL_CHARS = 3  # character range deletion (selection)


class BEHAVIOR_EVENT_PARAMS(ctypes.Structure):
    _fields_ = [
        ("cmd", UINT),              # BEHAVIOR_EVENTS
        ("heTarget", HELEMENT),     # target element handler, in MENU_ITEM_CLICK this is owner element that caused this menu - e.g. context menu owner
                                    # In scripting this field named as Event.owner
        ("he", HELEMENT),           # source element e.g. in SELECTION_CHANGED it is new selected <option>, in MENU_ITEM_CLICK it is menu item (LI) element
        ("reason", UINT_PTR),       # EVENT_REASON or EDIT_CHANGED_REASON - UI action causing change.
                                    # In case of custom event notifications this may be any
                                    # application specific value.
        ("data", SCITER_VALUE),     # auxiliary data accompanied with the event. E.g. FORM_SUBMIT event is using this field to pass collection of values.
    ]


class TIMER_PARAMS(ctypes.Structure):
    _fields_ = [
        ("timerId", UINT_PTR),     # timerId that was used to create timer by using HTMLayoutSetTimerEx
    ]


class BEHAVIOR_METHOD_IDENTIFIERS(enum.IntEnum):
    """"Identifiers of methods currently supported by intrinsic behaviors."""
    DO_CLICK = 0

    GET_TEXT_VALUE = 1
    SET_TEXT_VALUE = 2

    TEXT_EDIT_GET_SELECTION = 3
    TEXT_EDIT_SET_SELECTION = 4
    TEXT_EDIT_REPLACE_SELECTION = 5
    SCROLL_BAR_GET_VALUE = 6
    SCROLL_BAR_SET_VALUE = 7

    TEXT_EDIT_GET_CARET_POSITION = 8
    TEXT_EDIT_GET_SELECTION_TEXT = 9    # p - TEXT_SELECTION_PARAMS
    TEXT_EDIT_GET_SELECTION_HTML = 10   # p - TEXT_SELECTION_PARAMS
    TEXT_EDIT_CHAR_POS_AT_XY = 11       # p - TEXT_EDIT_CHAR_POS_AT_XY_PARAMS

    IS_EMPTY      = 0xFC        # p - IS_EMPTY_PARAMS  # set VALUE_PARAMS::is_empty (false/true) reflects :empty state of the element.
    GET_VALUE     = 0xFD        # p - VALUE_PARAMS 
    SET_VALUE     = 0xFE        # p - VALUE_PARAMS 

    FIRST_APPLICATION_METHOD_ID = 0x100


class SCRIPTING_METHOD_PARAMS(ctypes.Structure):
    _fields_ = [
        ("name", LPCSTR),                   # method name
        ("argv", POINTER(SCITER_VALUE)),    # vector of arguments
        ("argc", UINT),                     # argument count
        ("result", SCITER_VALUE),           # return value
    ]


class TISCRIPT_METHOD_PARAMS(ctypes.Structure):
    _fields_ = [
        # parameters are accessible through tiscript::args.
        ("vm", sctiscript.HVM),
        ("tag", sctiscript.value),     # method id (symbol)
        ("result", sctiscript.value),  # return value
    ]


# GET_VALUE/SET_VALUE methods params
class VALUE_PARAMS(ctypes.Structure):
    _fields_ = [
        ("methodID", UINT),
        ("val", SCITER_VALUE),
    ]


# IS_EMPTY method params
class IS_EMPTY_PARAMS(ctypes.Structure):
    _fields_ = [
        ("methodID", UINT),
        ("is_empty", UINT),  # !0 - is empty
    ]


# see SciterRequestElementData
class DATA_ARRIVED_PARAMS(ctypes.Structure):
    _fields_ = [
        ("initiator", HELEMENT),  # element intiator of HTMLayoutRequestElementData request,
        ("data", LPCBYTE),       # data buffer
        ("dataSize", UINT),      # size of data
        ("dataType", UINT),      # data type passed "as is" from HTMLayoutRequestElementData
        ("status", UINT),        # status = 0 (dataSize == 0) - unknown error.
                                 # status = 100..505 - http response status, Note: 200 - OK!
                                 # status > 12000 - wininet error code, see ERROR_INTERNET_*** in wininet.h
        ("_uri", LPCWSTR),       # requested url
    ]
    uri = UTF16LEField('_uri')

