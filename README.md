# Sciter bindings for Python

What supported right now:

* [sciter::value](https://github.com/c-smile/sciter-sdk/blob/master/include/value.hpp) pythonic wrapper with sciter::script_error and sciter::native_function support
* [sciter::host](https://github.com/c-smile/sciter-sdk/blob/master/include/sciter-x-host-callback.h) extensible implementation with transparent script calls from python code
* [sciter::event_handler](https://github.com/c-smile/sciter-sdk/blob/master/include/sciter-x-behavior.h) with basic event handling (attached, document_complete, on_script_call), additional handlers will come
* [sciter::window](https://github.com/c-smile/sciter-sdk/blob/master/include/sciter-x-window.hpp) which brings together window creation, host and event handlers

Minimal sciter app is extremely small:
```python
import sciter

if __name__ == '__main__':
    frame = sciter.Window(ismain=True, uni_theme=True)
    frame.load_file("minimal.htm")
    frame.set_title("PySciter")
    frame.expand()
    frame.run_app()
```

Check `pysciter/examples` folder for more complex usage.


## Interoperability

In respect of [tiscript](http://www.codeproject.com/Articles/33662/TIScript-language-a-gentle-extension-of-JavaScript) functions calling:
```python
answer = self.call_function('hello', "hello, python")
```

Calling python from tiscript can be implemented as following:
```python
def GetNativeApi(): # called from on_script_call
  def on_add(a, b):
      return a + b

  def on_sub(a, b):
      raise Exception("sub(%d,%d) raised exception" % (a, b))
      
  api = { 'add': on_add,  # plain function
          'sub': on_sub,  # raise exception at script
          'mul': lambda a,b: a * b }   # lambdas supported too
  return api
```


***To be continued…***
