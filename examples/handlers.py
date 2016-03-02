"""Sciter handlers sample (Go examples port)."""

import sciter


def scriptmethod(name=None):
    """Style decorator for method, called from script."""
    def decorator(func):
        attr = True if name is None else name
        func._from_sciter = attr
        return func
    if isinstance(name, str):
        return decorator
    func = name
    name = None
    return decorator(func)


class RootEventHandler(sciter.EventHandler):
    def __init__(self, el, frame):
        super().__init__(element=el)
        self.parent = frame
        pass

    def on_event(self, source, target, code, phase, reason):
        he = sciter.Element(source)
        #print("-> event:", code, phase, he)
        pass

    @scriptmethod('mcall')
    def method_call(self, *args):
        #
        # `root.mcall()` (see handlers.htm) calls behavior method of the root dom element (native equivalent is `Element.call_method()`),
        #  so we need to attach a "behavior" to that element to catch and handle such calls.
        # Also it can be handled at script by several ways: 
        # * `behavior` - Element subclassing with full control
        # * `aspect` - provides partial handling by attaching a single function to the dom element
        # *  manually attaching function to Element via code like `root.mcall = function(args..) {};`
        # 
        print("->mcall args:", "\t".join(map(str, args)))
        # explicit null for example, in other cases you can return any python object like None or True
        return sciter.Value.null() 

    pass


class Frame(sciter.Window):
        
    def __init__(self):
        super().__init__(ismain=True, uni_theme=False, debug=False)
        self.set_dispatch_options(enable=True, require_attribute=False)
        pass

    def test_call(self):
        # test sciter call
        v = self.call_function('gFunc', "kkk", 555)
        print("sciter   call successfully:", v)

        # test method call
        root = self.get_root()
        v = root.call_method('mfn', "method call", 10300)
        print("method   call successfully:", v)

        # test function call
        v = root.call_function('gFunc', "function call", 10300)
        print("function call successfully:", v)
        pass

    # Functions called from script:

    #@sciter.script - optional attribute here because of self.set_dispatch_options()
    def kkk(self):
        print("kkk called!")
        def fn(*args):
            print("%d: %s" % ( len(args), ",".join(map(str, args)) ))
            return "native functor called"
        rv = {}
        rv['num'] = 1000
        rv['str'] = "a string"
        rv['f'] = fn
        return rv
    
    @sciter.script
    def sumall(self, *args):
        sum = 0
        for v in args:
            sum += v
        return sum

    @sciter.script("gprintln")
    def gprint(self, *args):
        print("->", " ".join(map(str, args)))
        pass

    def on_load_data(self, nm):
        print("loading", nm.uri)
        pass

    def on_data_loaded(self, nm):
        print("loaded ", nm.uri)
        pass

    def on_event(self, source, target, code, phase, reason):
        # events from html controls (behaviors)
        he = sciter.Element(source)
        #print(".. event:", code, phase)

        # TODO: following statement looks ugly.
        # Guess it wasn't a nice idea to split event mask to separate code and phase values
        # Or we may pack all event arguments to single object (dict) to eliminate such parameters bloat
        # 
        if code == sciter.event.BEHAVIOR_EVENTS.BUTTON_CLICK and phase == sciter.event.PHASE_MASK.SINKING and he.test('#native'):
            print("native button clicked!")
            return True
        pass

    pass

if __name__ == "__main__":
    print("Sciter version:", sciter.version(as_str=True))

    # create window
    frame = Frame()

    # enable debug only for this window
    frame.setup_debug()

    # load file
    frame.load_file("examples/handlers.htm")
    #frame.load_html(b"""<html><body><button id='native'>Click</button></body></html>""")

    # install additional handler
    ev2 = RootEventHandler(frame.get_root(), frame)

    frame.test_call()

    frame.run_app()
