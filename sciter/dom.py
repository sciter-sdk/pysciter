"""DOM access methods."""

import ctypes

import sciter.error
import sciter.capi.scdef

from sciter.capi.scdom import *
from sciter.capi.screquest import SciterResourceType
from sciter.capi.scbehavior import BEHAVIOR_EVENTS, CLICK_REASON

_api = sciter.SciterAPI()

# TODO: behaviors support, create behavior
#
# Not implemented or not used APIs:
#
# SciterAttachHwndToElement
# SciterCallBehaviorMethod
# SciterCombineURL
# SciterControlGetType
# SciterGetElementIntrinsicHeight
# SciterGetElementIntrinsicWidths
# SciterGetElementNamespace
# SciterGetElementType
# SciterGetObject
# SciterHidePopup
# SciterNodeCastFromElement
# SciterSelectElementsW
# SciterSelectParentW
# SciterShowPopup
# SciterShowPopupAt
# SciterSortElements
# SciterTraverseUIEvent
#


class DomError(sciter.error.SciterError):
    """Raised from DOM operations."""

    def __init__(self, code, context=None):
        """."""
        name = SCDOM_RESULT(code).name
        msg = name.replace("SCDOM_", "").replace("_", " ").lower()
        if context is not None:
            msg = msg + " at " + context
        super().__init__(msg)
    pass


class Node:
    """DOM node - element, comment, text."""

    @classmethod
    def create(cls, text, kind=NODE_TYPE.NT_TEXT):
        """Make text or comment node with specified text."""
        if text is None:
            text = ""
        rv = HNODE()
        if kind == NODE_TYPE.NT_TEXT:
            ok = _api.SciterCreateTextNode(text, len(text), ctypes.byref(rv))
        elif kind == NODE_TYPE.NT_COMMENT:
            ok = _api.SciterCreateCommentNode(text, len(text), ctypes.byref(rv))
        Node._throw_if(ok)
        return Node(rv)

    def __init__(self, node=None):
        """Construct Node object from HNODE or HELEMENT."""
        super().__init__()
        self.h = None
        if node is not None:
            if isinstance(node, (HNODE, HELEMENT)):
                self._use(node)
            elif isinstance(node, (Node, Element)):
                self._use(node.h)
            else:
                raise TypeError("Unknown type of Node argument")
        pass

    def __del__(self):
        """Release node pointer."""
        self._unuse()
        pass

    def __eq__(self, other):
        """Test equality with another HNODE or Node object."""
        if isinstance(other, HNODE):
            return self.h == other
        elif isinstance(other, Node):
            return self.h == other.h
        else:
            return NotImplemented
        pass

    def __bool__(self):
        """Test object for None."""
        return self.h is not None

    def __length__(self):
        """Node children count."""
        return self.children_count()

    def __getitem__(self, key):
        """Get node child at specified index."""
        if not isinstance(key, int):
            raise TypeError
        count = len(self)
        key = count + key if key < 0 else key
        if key < 0 or key >= count:
            raise IndexError
        p = HNODE()
        ok = _api.SciterNodeNthChild(self, key, ctypes.byref(p))
        self._throw_if(ok)
        return Node(p)

    def _use(self, h):
        ok = _api.SciterNodeAddRef(h)
        self.h = h if ok == SCDOM_RESULT.SCDOM_OK else None
        self._as_parameter_ = self.h
        pass

    def _unuse(self):
        if self.h:
            _api.SciterNodeRelease(self.h)
            self.h = None
            self._as_parameter_ = self.h
        pass

    def parent(self):
        """Get parent element of node."""
        p = HELEMENT()
        ok = _api.SciterNodeParent(self, ctypes.byref(p))
        self._throw_if(ok, True)
        return None if ok == SCDOM_RESULT.SCDOM_OK_NOT_HANDLED else Element(p)

    def next_sibling(self):
        """Get next sibling node."""
        p = HNODE()
        ok = _api.SciterNodeNextSibling(self, ctypes.byref(p))
        self._throw_if(ok, True)
        return None if ok == SCDOM_RESULT.SCDOM_OK_NOT_HANDLED else Node(p)

    def prev_sibling(self):
        """Get previous sibling node."""
        p = HNODE()
        ok = _api.SciterNodePrevSibling(self, ctypes.byref(p))
        self._throw_if(ok, True)
        return None if ok == SCDOM_RESULT.SCDOM_OK_NOT_HANDLED else Node(p)

    def first_child(self):
        """Get first child of node."""
        p = HNODE()
        ok = _api.SciterNodeFirstChild(self, ctypes.byref(p))
        self._throw_if(ok)
        return Node(p)

    def last_child(self):
        """Get last child of node."""
        p = HNODE()
        ok = _api.SciterNodeLastChild(self, ctypes.byref(p))
        self._throw_if(ok)
        return Node(p)

    def children_count(self):
        """Return node children count."""
        n = ctypes.c_uint()
        ok = _api.SciterNodeChildrenCount(self, ctypes.byref(n))
        self._throw_if(ok)
        return n.value

    def get_type(self):
        """Get node type (text, comment or element)."""
        n = ctypes.c_uint()
        ok = _api.SciterNodeType(self, ctypes.byref(n))
        self._throw_if(ok)
        return NODE_TYPE(n.value)

    def is_text(self):
        """Is it a text node."""
        return self.get_type() == NODE_TYPE.NT_TEXT

    def is_comment(self):
        """Is it a comment node."""
        return self.get_type() == NODE_TYPE.NT_COMMENT

    def is_element(self):
        """Is it an element node."""
        return self.get_type() == NODE_TYPE.NT_ELEMENT

    def to_element(self):
        """Get Element object of this node."""
        p = HELEMENT()
        ok = _api.SciterNodeCastToElement(self, ctypes.byref(p))
        self._throw_if(ok)
        return Element(p)

    def remove(self):
        """Remove node from the DOM and free it."""
        ok = _api.SciterNodeRemove(self, True)
        self._throw_if(ok)
        ok = _api.SciterNodeRelease(self)
        self.h = None
        self._as_parameter_ = self.h
        pass

    def detach(self):
        """Remove node from the DOM, but not free it to save for further usage."""
        ok = _api.SciterNodeRemove(self, False)
        self._throw_if(ok)
        return self

    def append(self, node):
        """Insert new node as last child of current object."""
        ok = _api.SciterNodeInsert(self, NODE_INS_TARGET.NIT_APPEND, node)
        self._throw_if(ok)
        return self

    def prepend(self, node):
        """Insert new node as first child of current object."""
        ok = _api.SciterNodeInsert(self, NODE_INS_TARGET.NIT_PREPEND, node)
        self._throw_if(ok)
        return self

    def insert_before(self, node):
        """Insert new node before current one (as previous sibling)."""
        ok = _api.SciterNodeInsert(self, NODE_INS_TARGET.NIT_BEFORE, node)
        self._throw_if(ok)
        return self

    def insert_after(self, node):
        """Insert new node after current one (as next sibling)."""
        ok = _api.SciterNodeInsert(self, NODE_INS_TARGET.NIT_AFTER, node)
        self._throw_if(ok)
        return self

    def get_text(self):
        """Get contents of text/comment node."""
        cb = sciter.capi.scdef.StringReceiver('wchar')
        ok = _api.SciterNodeGetText(self, cb, None)
        self._throw_if(ok)
        return cb.text

    def set_text(self, text: str):
        """Set contents of text/comment node."""
        ok = _api.SciterNodeSetText(self, text, len(text))
        self._throw_if(ok)
        return self

    text = property(get_text, set_text)

    @staticmethod
    def _throw_if(code, skip_not_handled=False):
        if code == 0:
            return
        elif code == SCDOM_RESULT.SCDOM_OK_NOT_HANDLED and skip_not_handled:
            return
        import inspect
        context = inspect.stack()[1][3]
        raise DomError(code, "Node." + context)

    pass


class Element:
    """DOM element wrapper."""

    @classmethod
    def create(cls, tag: str, text=None):
        """Create new element, the element is disconnected initially from the DOM."""
        p = HELEMENT()
        ok = _api.SciterCreateElement(tag.encode('utf-8'), text, ctypes.byref(p))
        Element._throw_if(ok)
        return Element(p)

    @classmethod
    def from_window(cls, hwnd):
        """Get root DOM element of the Sciter document."""
        p = HELEMENT()
        ok = _api.SciterGetRootElement(hwnd, ctypes.byref(p))
        Element._throw_if(ok)
        return Element(p) if p else None

    @classmethod
    def from_focus(cls, hwnd):
        """Get focus DOM element of the Sciter document."""
        p = HELEMENT()
        ok = _api.SciterGetFocusElement(hwnd, ctypes.byref(p))
        Element._throw_if(ok)
        return Element(p) if p else None

    @classmethod
    def from_point(cls, hwnd, x, y):
        """Find DOM element of the Sciter document by coordinates."""
        p = HELEMENT()
        pt = sciter.capi.sctypes.POINT(x, y)
        ok = _api.SciterFindElement(hwnd, pt, ctypes.byref(p))
        Element._throw_if(ok)
        return Element(p) if p else None

    @classmethod
    def from_highlighted(cls, hwnd):
        """Get highlighted element."""
        p = HELEMENT()
        ok = _api.SciterGetHighlightedElement(hwnd, ctypes.byref(p))
        Element._throw_if(ok)
        return Element(p) if p else None

    @classmethod
    def from_uid(cls, hwnd, uid: int):
        """Get element handle by its UID."""
        p = HELEMENT()
        ok = _api.SciterGetElementByUID(hwnd, uid, ctypes.byref(p))
        Element._throw_if(ok)
        return Element(p) if p else None

    # instance methods
    def __init__(self, node=None):
        """Construct Element object from HNODE or HELEMENT handle."""
        super().__init__()
        self.h = None
        if node is not None:
            if isinstance(node, (HNODE, HELEMENT)):
                self._use(node)
            elif isinstance(node, (Node, Element)):
                self._use(node.h)
            else:
                raise TypeError("Unknown type of Element argument")
        pass

    def __del__(self):
        """Release element pointer."""
        self._unuse()
        pass

    def _use(self, h):
        ok = _api.Sciter_UseElement(h)
        self.h = h if ok == SCDOM_RESULT.SCDOM_OK else None
        self._as_parameter_ = self.h
        pass

    def _unuse(self):
        if self.h:
            ok = _api.Sciter_UnuseElement(self.h)
            self._throw_if(ok)
            self.h = None
            self._as_parameter_ = self.h
        pass

    def __eq__(self, other):
        """Test equality with another Element object or handle."""
        if isinstance(other, HELEMENT):
            return self.h == other
        elif isinstance(other, Element):
            return self.h == other.h
        else:
            return NotImplemented
        pass

    def __bool__(self):
        """Test object for None."""
        return self.h is not None

    def __length__(self):
        """Element children count."""
        return self.children_count()

    def __getitem__(self, key):
        """Get element child at specified index."""
        if not isinstance(key, int):
            raise TypeError
        count = len(self)
        key = count + key if key < 0 else key
        if key < 0 or key >= count:
            raise IndexError
        p = HELEMENT()
        ok = _api.SciterGetNthChild(self, key, ctypes.byref(p))
        self._throw_if(ok)
        return Element(p) if p else None

    def __str__(self):
        """Human element representation."""
        # tag#id.class|type(name)
        # tag#id.class
        if not self.h:
            return 'None'
        tag = self.get_tag()
        typ, name, id, cls = (self.attribute('type'), self.attribute('name'), self.attribute('id'), self.attribute('class'))
        fmt = [tag]
        if id:
            fmt.extend(('#', id))
        if cls:
            fmt.extend(('.', cls))
        if typ:
            fmt.extend(('|', typ))
        if name:
            fmt.extend(('(', name, ')'))
        return ''.join(fmt)

    def __repr__(self):
        """Machine-like element visualization."""
        return ''.join(('<', str(self), '>'))

    def clone(self):
        """Create new element as copy of existing element, new element is a full (deep) copy of the element and is disconnected initially from the DOM."""
        p = HELEMENT()
        ok = _api.SciterCloneElement(self, ctypes.byref(p))
        self._throw_if(ok)
        return Element(p)



    ## @name Common methods:

    def get_uid(self):
        """Get element UID - identifier suitable for storage."""
        n = ctypes.c_uint()
        ok = _api.SciterGetElementUID(self, ctypes.byref(n))
        self._throw_if(ok)
        return n.value

    def get_tag(self):
        """Return element tag as string (e.g. 'div', 'body')."""
        cb = sciter.capi.scdef.StringReceiver('char')
        ok = _api.SciterGetElementTypeCB(self, cb, None)
        self._throw_if(ok)
        return cb.text

    def clear(self):
        """Clear content of the element."""
        ok = _api.SciterSetElementText(self, None, 0)
        self._throw_if(ok)
        return self

    def get_value(self):
        """Get value of the element."""
        rv = sciter.Value()
        ok = _api.SciterGetValue(self, rv)
        self._throw_if(ok)
        return rv

    def set_value(self, val):
        """Set value of the element."""
        sval = sciter.Value(val)
        ok = _api.SciterSetValue(self, sval)
        self._throw_if(ok)
        return self

    def get_text(self) -> str:
        """Get inner text of the element as string."""
        cb = sciter.capi.scdef.StringReceiver('wchar')
        ok = _api.SciterGetElementTextCB(self, cb, None)
        self._throw_if(ok)
        return cb.text

    def set_text(self, text: str):
        """Set inner text of the element."""
        ok = _api.SciterSetElementText(self, text, len(text))
        self._throw_if(ok)
        return self

    def get_html(self, outer=True) -> bytes:
        """Get html representation of the element as utf-8 bytes."""
        cb = sciter.capi.scdef.StringReceiver('byte')
        ok = _api.SciterGetElementHtmlCB(self, outer, cb, None)
        self._throw_if(ok)
        return cb.text

    def set_html(self, html: bytes, where=SET_ELEMENT_HTML.SIH_REPLACE_CONTENT):
        """Set inner or outer html of the element."""
        if not html:
            self.clear()
            return self
        if not isinstance(html, bytes):
            raise TypeError("html must be a bytes type")
        ok = _api.SciterSetElementHtml(self, html, len(html), where)
        self._throw_if(ok)
        return self

    def get_expando(self, force_create=False):
        """Get scripting object (as Value) associated with this DOM element."""
        rv = sciter.Value()
        ok = _api.SciterGetExpando(self, rv, force_create)
        self._throw_if(ok)
        return rv

    def get_hwnd(self, for_root: bool):
        """Get HWINDOW of containing window."""
        hwnd = sciter.capi.sctypes.HWINDOW()
        ok = _api.SciterGetElementHwnd(self, ctypes.byref(hwnd), for_root)
        self._throw_if(ok)
        return hwnd

    def get_location(self, kind=ELEMENT_AREAS.SELF_RELATIVE | ELEMENT_AREAS.CONTENT_BOX):
        """Get bounding rectangle of the element."""
        rc = sciter.capi.sctypes.RECT(0, 0, 0, 0)
        ok = _api.SciterGetElementLocation(self, ctypes.byref(rc), kind)
        self._throw_if(ok)
        return rc

    def request_data(self, url: str, data_type=SciterResourceType.RT_DATA_HTML, initiator=None):
        """Request data download for this element."""
        ok = _api.SciterRequestElementData(self, url, data_type, initiator)
        self._throw_if(ok)
        return self

    def request_html(self, url: str, initiator=None):
        """Request HTML data download for this element."""
        return self.request_data(url, SciterResourceType.RT_DATA_HTML, initiator)

    def send_request(self, url: str, params=None, method='GET', send_async=False, data_type=SciterResourceType.RT_DATA_HTML):
        """Send HTTP GET or POST request for the element."""
        if method not in ('GET', 'POST'):
            raise ValueError("Only GET or POST supported here.")

        # GET_ASYNC = 0, GET_SYNC = 2, POST_ASYNC = 1, POST_SYNC = 3
        method_type = 2 if send_async is False else 0
        method_type += 1 if method == 'POST' else 0

        if params:
            nparams = len(params)
            ParamsType = REQUEST_PARAM * nparams
            method_params = ParamsType()
            for i, k in enumerate(params):
                method_params[i].name = k
                method_params[i].value = params[k]
        else:
            method_params = None
            nparams = 0
        ok = _api.SciterHttpRequest(self, url, data_type, method_type, method_params, nparams)
        self._throw_if(ok)
        return self

    def send_event(self, code: BEHAVIOR_EVENTS, reason=CLICK_REASON.SYNTHESIZED, source=None):
        """Send sinking/bubbling event to the child/parent chain of the element."""
        handled = sciter.capi.sctypes.BOOL()
        ok = _api.SciterSendEvent(self, code, source if source else self.h, reason, ctypes.byref(handled))
        self._throw_if(ok)
        return handled != False

    def post_event(self, code: BEHAVIOR_EVENTS, reason=CLICK_REASON.SYNTHESIZED, source=None):
        """Post sinking/bubbling event to the child/parent chain of the element."""
        ok = _api.SciterPostEvent(self, code, source if source else self.h, reason)
        self._throw_if(ok)
        return self

    def fire_event(self, code: BEHAVIOR_EVENTS, reason=CLICK_REASON.SYNTHESIZED, source=None, post=True, data=None):
        """Send or post sinking/bubbling event to the child/parent chain of the element."""
        params = sciter.capi.scbehavior.BEHAVIOR_EVENT_PARAMS()
        params.cmd = code
        params.reason = reason
        params.he = source if source else self.h
        params.heTarget = self.h
        if data is not None:
            sciter.Value.pack_to(params.data, data)
        handled = sciter.capi.sctypes.BOOL()
        ok = _api.SciterFireEvent(ctypes.byref(params), post, ctypes.byref(handled))
        self._throw_if(ok)
        return handled != False

    def eval_script(self, script: str, name=None):
        """Evaluate script in element context."""
        rv = sciter.Value()
        ok = _api.SciterEvalElementScript(self, script, len(script), rv)
        sciter.Value.raise_from(rv, ok == SCDOM_RESULT.SCDOM_OK, name if name else 'Element.eval')
        self._throw_if(ok)
        return rv

    def call_function(self, name: str, *args):
        """Call scripting function defined in the namespace of the element (a.k.a. global function)."""
        rv = sciter.Value()
        argc, argv, _ = sciter.Value.pack_args(*args)
        ok = _api.SciterCallScriptingFunction(self, name.encode('utf-8'), argv, argc, rv)
        sciter.Value.raise_from(rv, ok == SCDOM_RESULT.SCDOM_OK, name)
        self._throw_if(ok)
        return rv

    def call_method(self, name: str, *args):
        """Call scripting method defined for the element."""
        rv = sciter.Value()
        argc, argv, _ = sciter.Value.pack_args(*args)
        ok = _api.SciterCallScriptingMethod(self, name.encode('utf-8'), argv, argc, rv)
        sciter.Value.raise_from(rv, ok == SCDOM_RESULT.SCDOM_OK, name)
        self._throw_if(ok)
        return rv


    ## @name Attributes:
    uid = property(get_uid)
    tag = property(get_tag)
    text = property(get_text, set_text)
    html = property(get_html, set_html)
    value = property(get_value, set_value)

    def attribute_count(self):
        """Get number of the attributes."""
        n = ctypes.c_uint()
        ok = _api.SciterGetAttributeCount(self, ctypes.byref(n))
        self._throw_if(ok)
        return n.value

    def attribute_name(self, n):
        """Get attribute name by its index."""
        cb = sciter.capi.scdef.StringReceiver('char')
        ok = _api.SciterGetNthAttributeNameCB(self, n, cb, None)
        self._throw_if(ok)
        return cb.text

    def attribute(self, name_or_index, default=None):
        """Get attribute value by its name or index."""
        cb = sciter.capi.scdef.StringReceiver('wchar')
        if isinstance(name_or_index, int):
            ok = _api.SciterGetNthAttributeValueCB(self, name_or_index, cb, None)
        elif isinstance(name_or_index, str):
            ok = _api.SciterGetAttributeByNameCB(self, name_or_index.encode('utf-8'), cb, None)
        else:
            raise TypeError("name_or_index must be int or str")
        if ok == SCDOM_RESULT.SCDOM_OK_NOT_HANDLED:
            return default
        self._throw_if(ok)
        return cb.text

    def set_attribute(self, name: str, val: str):
        """Add or replace attribute."""
        ok = _api.SciterSetAttributeByName(self, name.encode('utf-8'), str(val))
        self._throw_if(ok)
        return self

    def remove_attribute(self, name: str):
        """Remove attribute."""
        ok = _api.SciterSetAttributeByName(self, name.encode('utf-8'), None)
        self._throw_if(ok)
        return self

    def toggle_attribute(self, name: str, isset: bool, val=''):
        """Toggle attribute."""
        if isset:
            self.set_attribute(name, val)
        else:
            self.remove_attribute(name)
        return self

    def clear_attributes(self):
        """Remove all attributes from the element."""
        ok = _api.SciterClearAttributes(self)
        self._throw_if(ok)
        return self


    ## @name Style attributes:

    def style_attribute(self, name: str):
        """Get style attribute of the element by its name."""
        cb = sciter.capi.scdef.StringReceiver('wchar')
        ok = _api.SciterGetStyleAttributeCB(self, name.encode('utf-8'), cb, None)
        self._throw_if(ok)
        return cb.text

    def set_style_attribute(self, name: str, val: str):
        """Set style attribute."""
        ok = _api.SciterSetStyleAttribute(self, name.encode('utf-8'), val)
        self._throw_if(ok)
        return self


    ## @name State methods:

    def set_state(self, set_bits, clear_bits=0, update=True):
        """Set UI state of the element with optional view update."""
        ok = _api.SciterSetElementState(self, set_bits, clear_bits, update)
        self._throw_if(ok)
        return self

    def state(self):
        """Get UI state bits of the element as set of ELEMENT_STATE_BITS."""
        n = ctypes.c_uint()
        ok = _api.SciterGetElementState(self, ctypes.byref(n))
        self._throw_if(ok)
        return ELEMENT_STATE_BITS(n.value)

    def has_state(self, check: ELEMENT_STATE_BITS):
        """Check if particular UI state bits are set in the element."""
        current = self.state()
        return (current & check) != 0

    def is_enabled(self):
        """Deep enable state, determines if element enabled - is not disabled by itself or no one of its parents is disabled."""
        n = sciter.capi.sctypes.BOOL()
        ok = _api.SciterIsElementEnabled(self, ctypes.byref(n))
        self._throw_if(ok)
        return bool(n.value)

    def is_visible(self):
        """Deep visibility, determines if element visible - has no visiblity:hidden and no display:none defined for itself or for any its parents."""
        n = sciter.capi.sctypes.BOOL()
        ok = _api.SciterIsElementVisible(self, ctypes.byref(n))
        self._throw_if(ok)
        return bool(n.value)

    def highlight(self, isset=True):
        """Highlight element visually (used for debug purposes)."""
        hwnd = self.get_hwnd(True)
        ok = _api.SciterSetHighlightedElement(hwnd, self if isset else None)
        self._throw_if(ok)
        return self


    ## @name DOM tree access:

    def root(self):
        """Get root of the element."""
        dad = self.parent()
        return dad.root() if dad else self

    def parent(self):
        """Get parent element."""
        p = HELEMENT()
        ok = _api.SciterGetParentElement(self, ctypes.byref(p))
        self._throw_if(ok)
        return Element(p) if p else None

    def index(self):
        """Get index of this element in its parent collection."""
        n = ctypes.c_uint()
        ok = _api.SciterGetElementIndex(self, ctypes.byref(n))
        self._throw_if(ok)
        return n.value

    def next_sibling(self):
        """Get next sibling element."""
        idx = self.index() + 1
        dad = self.parent()
        if not dad or idx >= len(dad):
            return None
        return dad[idx]     # pylint: disable=unsubscriptable-object

    def prev_sibling(self):
        """Get previous sibling element."""
        idx = self.index() - 1
        dad = self.parent()
        if not dad or idx < 0 or idx >= len(dad):
            return None
        return dad[idx]     # pylint: disable=unsubscriptable-object

    def first_sibling(self):
        """Get first sibling element."""
        dad = self.parent()
        if not dad or len(dad) == 0:
            return None
        return dad[0]     # pylint: disable=unsubscriptable-object

    def last_sibling(self):
        """Get last sibling element."""
        dad = self.parent()
        if not dad or len(dad) == 0:
            return None
        return dad[len(dad)-1]     # pylint: disable=unsubscriptable-object

    def children_count(self):
        """Get number of child elements."""
        n = ctypes.c_uint()
        ok = _api.SciterGetChildrenCount(self, ctypes.byref(n))
        self._throw_if(ok)
        return n.value

    def insert(self, child, index: int):
        """Insert element at index position of this element."""
        ok = _api.SciterInsertElement(child.h, self.h, index)
        self._throw_if(ok)
        return self

    def append(self, child):
        """Append element as last child of this element."""
        return self.insert(child, 0x7FFFFFFF)

    def detach(self):
        """Take element out of its container (and DOM tree)."""
        ok = _api.SciterDetachElement(self.h)
        self._throw_if(ok)
        return self

    def destroy(self):
        """Take element out of its container (and DOM tree) and force destruction of all behaviors."""
        tmp = self.h
        self.h = None
        ok = _api.SciterDeleteElement(tmp)
        self._throw_if(ok)
        return self

    def swap(self, el):
        """Swap element positions."""
        ok = _api.SciterSwapElements(self, el)
        self._throw_if(ok)
        return self

    def test(self, selector: str) -> bool:
        """Test this element against CSS selector(s)."""
        found = HELEMENT()
        ok = _api.SciterSelectParent(self, selector.encode('utf-8'), 1, ctypes.byref(found))
        self._throw_if(ok)
        return bool(found)

    def select_elements(self, callback, selector: str):
        """Call specified function for every element in a DOM that meets specified CSS selectors."""
        def on_element(he, param):
            el = Element(HELEMENT(he))
            stop = callback(el)
            return stop
        scfunc = sciter.capi.scdef.SciterElementCallback(on_element)
        ok = _api.SciterSelectElements(self, selector.encode('utf-8'), scfunc, None)
        self._throw_if(ok)
        return self

    def find_first(self, selector: str):
        """Will find first element starting from this satisfying given css selector(s)."""
        rv = []
        def on_element(el):
            rv.append(el)
            return True  # stop enumeration

        self.select_elements(on_element, selector)
        return rv[0] if len(rv) else None

    def find_nearest_parent(self, selector: str):
        """Will find first parent element starting from this satisfying given css selector(s)."""
        found = HELEMENT()
        ok = _api.SciterSelectParent(self, selector.encode('utf-8'), 0, ctypes.byref(found))
        self._throw_if(ok)
        return Element(found) if found else None

    def find_all(self, selector: str):
        """Will find all elements starting from this satisfying given css selector(s)."""
        rv = []
        def on_element(el):
            rv.append(el)
            return False  # continue enumeration

        self.select_elements(on_element, selector)
        return rv


    ## @name Scroll methods:

    def scroll_to_view(self, view_top=False, smooth=False):
        """Scroll this element to view."""
        how = 0
        if view_top:
            how = how | SCITER_SCROLL_FLAGS.SCROLL_TO_TOP
        if smooth:
            how = how | SCITER_SCROLL_FLAGS.SCROLL_SMOOTH
        ok = _api.SciterScrollToView(self, how)
        self._throw_if(ok)
        return self

    def set_scroll_pos(self, x, y, smooth=True):
        """Set scroll position of element with overflow:scroll or auto."""
        pt = sciter.capi.sctypes.POINT(x,y)
        ok = _api.SciterSetScrollPos(self, pt, smooth)
        self._throw_if(ok)
        return self

    def scroll_info(self):
        """Get scroll info of element with overflow:scroll or auto."""
        def struct2dict(st):
            rv = dict()
            for field in st._fields_:
                name = field[0]
                rv[name] = getattr(st, name)
            return rv
        pos = sciter.capi.sctypes.POINT()
        view = sciter.capi.sctypes.RECT()
        size = sciter.capi.sctypes.SIZE()
        ok = _api.SciterGetScrollInfo(self, ctypes.byref(pos), ctypes.byref(view), ctypes.byref(size))
        self._throw_if(ok)
        return dict(scroll_pos=struct2dict(pos), view_rect=struct2dict(view), content_size=struct2dict(size))


    ## @name Other methods:

    def set_capture(self):
        """Set mouse capture."""
        ok = _api.SciterSetCapture(self)
        self._throw_if(ok)
        return self

    def release_capture(self):
        """Release mouse capture."""
        ok = _api.SciterReleaseCapture(self)
        self._throw_if(ok)
        return self

    def update(self, render_now=False):
        """Apply changes and refresh element area in its window."""
        ok = _api.SciterUpdateElement(self, render_now)
        self._throw_if(ok)
        return self

    def refresh(self, area=None):
        """Refresh element area in its window."""
        assert area is None or isinstance(area, sciter.capi.sctypes.RECT)
        if area is None:
            area = self.get_location(ELEMENT_AREAS.SELF_RELATIVE | ELEMENT_AREAS.CONTENT_BOX)
        ok = _api.SciterRefreshElementArea(self, area)
        self._throw_if(ok)
        return self

    def start_timer(self, ms: int, timer_id=None):
        """Start Timer for the element. Element will receive on_timer event."""
        p = sciter.capi.sctypes.UINT_PTR(timer_id)
        ok = _api.SciterSetTimer(self, ms, p)
        self._throw_if(ok)
        return self

    def stop_timer(self, timer_id=None):
        """Stop Timer for the element."""
        if self.h:
            p = sciter.capi.sctypes.UINT_PTR(timer_id)
            ok = _api.SciterSetTimer(self, 0, p)
            self._throw_if(ok)
        return self

    # helper
    @staticmethod
    def _throw_if(code):
        if code == 0:
            return
        import inspect
        context = inspect.stack()[1][3]
        raise DomError(code, "Element." + context)

    pass
