"""More complex PySciter sample."""

import sciter

# main frame
class Frame(sciter.Window):
    def __init__(self):
        super().__init__(ismain=True, uni_theme=True)
        pass

    def get_api(self):

        def on_add(a, b):
            return a + b

        def on_sub(a, b):
            raise Exception("sub(%d,%d) raised exception" % (a, b))
                
        api = {'add': on_add,               # plain function
                'sub': on_sub,              # raised exception will propagated to script 
                'mul': lambda a,b: a * b,   # lambdas support
                }
        return api


    def on_subscription(self, groups):
        # subscribing only for scripting calls and document events
        from sciter.behavior import EVENT_GROUPS
        return EVENT_GROUPS.HANDLE_BEHAVIOR_EVENT | EVENT_GROUPS.HANDLE_SCRIPTING_METHOD_CALL

    def on_script_call(self, name, args):
        # script calls
        print(name, "called from script")
        if name == 'PythonCall':
            return "Pythonic window"

        elif name == 'GetNativeApi':
            return self.get_api()

        elif name == 'ScriptCallTest':
            print("calling 'hello'")
            answer = self.call_function('hello', "hello, python")
            print("hello answer: ", answer)

            try:
                print("calling 'raise_error'")
                answer = self.call_function('raise_error', 17, '42', False)
            except sciter.ScriptError as e:
                print("answer: ", str(e))

            answer = self.eval_script('hello')
            answer = answer.call('argument', name='on_script_call')

            try:
                answer = self.eval_script('raise_error')
                answer = answer.call('argument', name='on_script_call')
            except sciter.ScriptError as e:
                print("answer: ", str(e))

            try:
                print("calling unexisting function")
                answer = self.call_function('raise_error2')
            except sciter.ScriptError as e:
                print("answer: ", str(e))
            return True

        pass
# end


def main():
    frame = Frame()
    frame.load_file("examples/pysciter.htm")
    frame.set_title("PySciter")
    frame.expand()
    frame.run_app()

main()
