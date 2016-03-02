"""DOM access methods, C interface."""

import enum
import ctypes

from sciter.capi.sctypes import INT, UINT, LPCWSTR, UTF16LEField

HELEMENT = ctypes.c_void_p
HNODE = ctypes.c_void_p
HRANGE = ctypes.c_void_p
HSARCHIVE = ctypes.c_void_p


class SCDOM_RESULT(enum.IntEnum):
    """Result value for Sciter DOM functions."""

    # function completed successfully
    SCDOM_OK = 0

    # invalid HWINDOW
    SCDOM_INVALID_HWND = 1

    # invalid HELEMENT
    SCDOM_INVALID_HANDLE = 2

    # attempt to use HELEMENT which is not marked by Sciter_UseElement()
    SCDOM_PASSIVE_HANDLE = 3

    # parameter is invalid, e.g. pointer is null
    SCDOM_INVALID_PARAMETER = 4

    # operation failed, e.g. invalid html in SciterSetElementHtml()
    SCDOM_OPERATION_FAILED = 5

    SCDOM_OK_NOT_HANDLED = (-1)
# end


class HPOSITION(ctypes.Structure):
    """."""
    _fields_ = [
        ("hn", HNODE),
        ("pos", INT),
        ]


class METHOD_PARAMS(ctypes.Structure):
    """."""
    _fields_ = [("methodID", UINT), ]


class REQUEST_PARAM(ctypes.Structure):
    """."""
    _fields_ = [
        ("_name", LPCWSTR),
        ("_value", LPCWSTR),
        ]
    name = UTF16LEField('_name')
    value = UTF16LEField('_value')


class NODE_TYPE(enum.IntEnum):
    """."""
    NT_ELEMENT = 0
    NT_TEXT = 1
    NT_COMMENT = 2


class NODE_INS_TARGET(enum.IntEnum):
    """."""
    NIT_BEFORE = 0
    NIT_AFTER = 1
    NIT_APPEND = 2
    NIT_PREPEND = 3


class ELEMENT_AREAS(enum.IntEnum):
    """Bounding rectangle of the element."""

    ROOT_RELATIVE = 0x01        # - or this flag if you want to get HTMLayout window relative coordinates,
    SELF_RELATIVE = 0x02        # - "or" this flag if you want to get coordinates relative to the origin
    CONTAINER_RELATIVE = 0x03   # - position inside immediate container.
    VIEW_RELATIVE = 0x04        # - position relative to view - HTMLayout window

    CONTENT_BOX = 0x00    # content (inner)  box
    PADDING_BOX = 0x10    # content + paddings
    BORDER_BOX = 0x20    # content + paddings + border
    MARGIN_BOX = 0x30    # content + paddings + border + margins

    BACK_IMAGE_AREA = 0x40  # relative to content origin - location of background image (if it set no-repeat)
    FORE_IMAGE_AREA = 0x50  # relative to content origin - location of foreground image (if it set no-repeat)

    SCROLLABLE_AREA = 0x60    # scroll_area - scrollable area in content box


class SCITER_SCROLL_FLAGS(enum.IntEnum):
    """."""
    SCROLL_TO_TOP = 0x01
    SCROLL_SMOOTH = 0x10


class SET_ELEMENT_HTML(enum.IntEnum):
    """."""
    SIH_REPLACE_CONTENT = 0     # replace content of the element
    SIH_INSERT_AT_START = 1     # insert html before first child of the element
    SIH_APPEND_AFTER_LAST = 2   # insert html after last child of the element
    SOH_REPLACE = 3             # replace element by html, a.k.a. element.outerHtml = "something"
    SOH_INSERT_BEFORE = 4       # insert html before the element
    SOH_INSERT_AFTER = 5        # insert html after the element


class ELEMENT_STATE_BITS(enum.IntEnum):
    """Runtime DOM element state."""
    STATE_LINK             = 0x00000001
    STATE_HOVER            = 0x00000002
    STATE_ACTIVE           = 0x00000004
    STATE_FOCUS            = 0x00000008
    STATE_VISITED          = 0x00000010
    STATE_CURRENT          = 0x00000020  # current (hot) item
    STATE_CHECKED          = 0x00000040  # element is checked (or selected)
    STATE_DISABLED         = 0x00000080  # element is disabled
    STATE_READONLY         = 0x00000100  # readonly input element
    STATE_EXPANDED         = 0x00000200  # expanded state - nodes in tree view
    STATE_COLLAPSED        = 0x00000400  # collapsed state - nodes in tree view - mutually exclusive with
    STATE_INCOMPLETE       = 0x00000800  # one of fore/back images requested but not delivered
    STATE_ANIMATING        = 0x00001000  # is animating currently
    STATE_FOCUSABLE        = 0x00002000  # will accept focus
    STATE_ANCHOR           = 0x00004000  # anchor in selection (used with current in selects)
    STATE_SYNTHETIC        = 0x00008000  # this is a synthetic element - don't emit it's head/tail
    STATE_OWNS_POPUP       = 0x00010000  # this is a synthetic element - don't emit it's head/tail
    STATE_TABFOCUS         = 0x00020000  # focus gained by tab traversal
    STATE_EMPTY            = 0x00040000  # empty - element is empty (text.size() == 0 && subs.size() == 0)
                                         # if element has behavior attached then the behavior is responsible for the value of this flag.
    STATE_BUSY             = 0x00080000  # busy; loading

    STATE_DRAG_OVER        = 0x00100000  # drag over the block that can accept it (so is current drop target). Flag is set for the drop target block
    STATE_DROP_TARGET      = 0x00200000  # active drop target.
    STATE_MOVING           = 0x00400000  # dragging/moving - the flag is set for the moving block.
    STATE_COPYING          = 0x00800000  # dragging/copying - the flag is set for the copying block.
    STATE_DRAG_SOURCE      = 0x01000000  # element that is a drag source.
    STATE_DROP_MARKER      = 0x02000000  # element is drop marker

    STATE_PRESSED          = 0x04000000  # pressed - close to active but has wider life span - e.g. in MOUSE_UP it
                                         # is still on; so behavior can check it in MOUSE_UP to discover CLICK condition.
    STATE_POPUP            = 0x08000000  # this element is out of flow - popup

    STATE_IS_LTR           = 0x10000000  # the element or one of its containers has dir=ltr declared
    STATE_IS_RTL           = 0x20000000  # the element or one of its containers has dir=rtl declared


class REQUEST_TYPE(enum.IntEnum):
    """."""
    GET_ASYNC = 0
    POST_ASYNC = 1
    GET_SYNC = 2
    POST_SYNC = 3


class CTL_TYPE(enum.IntEnum):
    """DOM control type."""
    (CTL_NO,              # This dom element has no behavior at all.
    CTL_UNKNOWN,          # This dom element has behavior but its type is unknown.
    CTL_EDIT,             # Single line edit box.
    CTL_NUMERIC,          # Numeric input with optional spin buttons.
    CTL_CLICKABLE,        # toolbar button, behavior:clickable.
    CTL_BUTTON,           # Command button.
    CTL_CHECKBOX,         # CheckBox (button).
    CTL_RADIO,            # OptionBox (button).
    CTL_SELECT_SINGLE,    # Single select, ListBox or TreeView.
    CTL_SELECT_MULTIPLE,  # Multiselectable select, ListBox or TreeView.
    CTL_DD_SELECT,        # Dropdown single select.
    CTL_TEXTAREA,         # Multiline TextBox.
    CTL_HTMLAREA,         # WYSIWYG HTML editor.
    CTL_PASSWORD,         # Password input element.
    CTL_PROGRESS,         # Progress element.
    CTL_SLIDER,           # Slider input element.
    CTL_DECIMAL,          # Decimal number input element.
    CTL_CURRENCY,         # Currency input element.
    CTL_SCROLLBAR,

    CTL_HYPERLINK,

    CTL_MENUBAR,
    CTL_MENU,
    CTL_MENUBUTTON,

    CTL_CALENDAR,
    CTL_DATE,
    CTL_TIME,

    CTL_FRAME,
    CTL_FRAMESET,

    CTL_GRAPHICS,
    CTL_SPRITE,

    CTL_LIST,
    CTL_RICHTEXT,
    CTL_TOOLTIP,

    CTL_HIDDEN,
    CTL_URL,            # URL input element.
    CTL_TOOLBAR,

    CTL_FORM,
    CTL_FILE,           # file input element.
    CTL_PATH,           # path input element.
    CTL_WINDOW,         # has HWND attached to it

    CTL_LABEL,            
    CTL_IMAGE) = range(42) # image/object.  


assert (CTL_TYPE.CTL_NO == 0)
assert (CTL_TYPE.CTL_IMAGE == 41)
