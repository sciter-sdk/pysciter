"""Behaviors support (a.k.a windowless controls)."""

import ctypes

from sciter.scbehavior import *
from sciter.scdom import SCDOM_RESULT
import sciter.scdef

_api = sciter.SciterAPI()


class EventHandler:
    """."""

    def __init__(self, wnd=None, element=None, subscription=EVENT_GROUPS.HANDLE_ALL):
        """Attach event handler to dom::element or sciter::window."""
        self.subscription = subscription
        self.element = None
        self._attached_to_window = None
        self._attached_to_element = None
        if wnd or element:
            self.attach(wnd, element, subscription)
        pass

    def __del__(self):
        assert(not self.element)
        pass

    def attach(self, wnd=None, element=None, subscription=EVENT_GROUPS.HANDLE_ALL):
        """Attach event handler to dom::element or sciter::window."""
        assert(wnd or element)
        self.subscription = subscription
        self._event_handler_proc = sciter.scdef.ElementEventProc(self._element_proc)
        tag = id(self)
        if wnd:
            self._attached_to_window = wnd
            ok = _api.SciterWindowAttachEventHandler(wnd, self._event_handler_proc, tag, subscription)
            if ok != SCDOM_RESULT.SCDOM_OK:
                raise sciter.SciterError("Could not attach to window")
        elif element:
            self._attached_to_element = element
            ok = _api.SciterAttachEventHandler(element, self._event_handler_proc, tag)
            if ok != SCDOM_RESULT.SCDOM_OK:
                raise sciter.SciterError("Could not attach to element")
        pass

    def detach(self):
        """Detach event handler from dom::element or sciter::window."""
        tag = id(self)
        if self._attached_to_window:
            ok = _api.SciterWindowDetachEventHandler(self._attached_to_window, self._event_handler_proc, tag)
            if ok != SCDOM_RESULT.SCDOM_OK:
                raise sciter.SciterError("Could not detach from window")
        elif self._attached_to_element:
            ok = _api.SciterDetachEventHandler(self._attached_to_element, self._event_handler_proc, tag)
            if ok != SCDOM_RESULT.SCDOM_OK:
                raise sciter.SciterError("Could not attach from element")
        pass

    def dispatch(self, name, args):
        """Route script call to python handler directly."""
        fn = getattr(self, name, None)
        if fn is not None:
            return fn(*args)
        pass


    ## @name following functions can be overloaded
    ## @param he - a `this` element for behavior attached to
    ## @param source - source element of this event
    ## @param target - target element of this event

    def attached(self, he):
        pass

    def detached(self, he):
        pass

    def document_complete(self):
        """Notification that document finishes its loading - all requests for external resources are finished."""
        pass

    def document_close(self):
        """The last notification before document removal from the DOM."""
        pass

    def on_subscription(self, groups: EVENT_GROUPS):
        """Return list of event groups this event_handler is subscribed to."""
        return self.subscription

    def on_script_call(self, name: str, args: list):
        """Script calls from CSSS! script and TIScript."""
        pass

    def on_event(self, source: HELEMENT, target: HELEMENT, code: BEHAVIOR_EVENTS, phase: PHASE_MASK, reason: EVENT_REASON):
        """Notification event from builtin behaviors."""
        pass

    def on_data_arrived(self, nm: DATA_ARRIVED_PARAMS):
        """Requested data has been delivered."""
        pass

    ## @}

    def _on_script_call(self, f):
        args = sciter.Value.unpack_from(f.argv, f.argc)
        try:
            rv = self.on_script_call(f.name.decode('utf-8'), args)
        except Exception as e:
            rv = e
        if rv is not None:
            sciter.Value.pack_to(f.result, rv)
            return True
        return False


    def _element_proc(self, tag, he, evt, params):
        he = HELEMENT(he)
        if evt == EVENT_GROUPS.SUBSCRIPTIONS_REQUEST:
            p = ctypes.cast(params, ctypes.POINTER(ctypes.c_uint))
            subscribed = self.on_subscription(p.contents)
            if subscribed is not None:
                p.contents = ctypes.c_ulong(int(subscribed))
                return True

        elif evt == EVENT_GROUPS.HANDLE_INITIALIZATION:
            # handle initialization events and route to attached() and detached()
            # NOTE: when attaching to empty window, this called with he == NULL
            p = ctypes.cast(params, ctypes.POINTER(INITIALIZATION_PARAMS))
            if p.contents.cmd == INITIALIZATION_EVENTS.BEHAVIOR_DETACH:
                self.detached(he)
                self.element = None
            elif p.contents.cmd == INITIALIZATION_EVENTS.BEHAVIOR_ATTACH:
                self.element = sciter.Element(he)
                self.attached(he)
            return True

        elif evt == EVENT_GROUPS.HANDLE_BEHAVIOR_EVENT:
            # handle behavior events and route to on_event(), document_complete() and document_close()
            p = ctypes.cast(params, ctypes.POINTER(BEHAVIOR_EVENT_PARAMS))
            m = p.contents
            if m.cmd == BEHAVIOR_EVENTS.DOCUMENT_COMPLETE:
                self.element = sciter.Element(he)
                self.document_complete()
            elif m.cmd == BEHAVIOR_EVENTS.DOCUMENT_CLOSE:
                self.document_close()
                self.element = None

            phase = m.cmd & 0xFFFFF000
            code = m.cmd & 0xFFF
            handled = self.on_event(m.he, m.heTarget, code, phase, m.reason)
            return handled or False

        elif evt == EVENT_GROUPS.HANDLE_SCRIPTING_METHOD_CALL:
            # handle script calls
            p = ctypes.cast(params, ctypes.POINTER(SCRIPTING_METHOD_PARAMS))
            return self._on_script_call(p.contents)

        elif evt == EVENT_GROUPS.HANDLE_DATA_ARRIVED:
            # notification event: data requested by HTMLayoutRequestData just delivered
            p = ctypes.cast(params, ctypes.POINTER(DATA_ARRIVED_PARAMS))
            handled = self.on_data_arrived(p.contents)
            return handled or False

        return False
