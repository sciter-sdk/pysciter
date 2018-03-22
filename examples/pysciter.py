"""More complex PySciter sample."""

import sciter

# main frame
class Frame(sciter.Window):
    def __init__(self):
        super().__init__(ismain=True, uni_theme=True)
        pass

    def on_subscription(self, groups):
        # subscribing only for scripting calls and document events
        from sciter.event import EVENT_GROUPS
        return EVENT_GROUPS.HANDLE_BEHAVIOR_EVENT | EVENT_GROUPS.HANDLE_SCRIPTING_METHOD_CALL

    def on_script_call(self, name, args):
        # script calls
        print(name, "called from script")
        return self.dispatch(name, args)


    ## @name The following functions are called from scripts:
    @sciter.script
    def PythonCall(self, arg):
        return "Pythonic window (%s)" % str(arg)

    @sciter.script
    def GetNativeApi(self):

        def on_add(a, b):
            return a + b

        def on_sub(a, b):
            raise Exception("sub(%d,%d) raised exception" % (a, b))

        api = { 'add': on_add,              # plain function
                'sub': on_sub,              # raised exception will propagated to script
                'mul': lambda a,b: a * b,   # lambdas support
                }
        return api

    @sciter.script
    def ScriptCallTest(self):
        print("calling 'hello'")
        answer = self.call_function('hello', "hello, python")
        print("call answer: ", answer)

        print("get and call 'hello'")
        answer = self.eval_script('hello')
        answer = answer.call('argument', name='on_script_call')
        print("get answer: ", answer)

        print("eval 'hello'")
        answer = self.eval_script('hello("42");')
        print("eval answer: ", answer)

        try:
            print("\ncalling 'raise_error'")
            answer = self.call_function('raise_error', 17, '42', False)
            print("expected ScriptError")
        except sciter.ScriptError as e:
            print("answer: ", str(e))


        try:
            print("\nget and call 'raise_error'")
            answer = self.eval_script('raise_error')
            answer = answer.call('argument', name='on_script_call')
            print("expected ScriptError")
        except sciter.ScriptError as e:
            print("answer: ", str(e))

        try:
            print("\ncalling unexisting function")
            answer = self.call_function('raise_error2')
            print("expected ScriptError")
        except sciter.ScriptError as e:
            print("answer: ", str(e))
        return True

    ## @}

# end


if __name__ == '__main__':
    import os
    htm = os.path.join(os.path.dirname(__file__), 'pysciter.htm')
    frame = Frame()
    frame.load_file(htm)
    frame.run_app()
