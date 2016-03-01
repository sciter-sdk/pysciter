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

    @scriptmethod
    def mcall(self, *args):
        print("->mcall args:", "\t".join(args))
        # explicit null for example, in other cases you can return any python object like None or True
        return sciter.Value.null() 

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

        if code == sciter.event.BEHAVIOR_EVENTS.CLICK and he.test('#native'):
            print("native handler called")
            return True
        pass

    pass

if __name__ == "__main__":
    print("Sciter version:", sciter.version(as_str=True))

    # create window
    frame = Frame()

    # enable debug
    frame.setup_debug()#frame.get_hwnd())

    # load file
    frame.load_file("examples/handlers.htm")

    frame.test_call()

    frame.run_app()
