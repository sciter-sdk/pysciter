# Sciter bindings for Python

Sciter is an embeddable [multiplatform](http://sciter.com/sciter/crossplatform/) HTML/CSS/script engine designed to render modern desktop application UI. It's a **compact**, single dll/dylib/so file (4-8 mb), engine without any additional dependencies. 

Sciter supports all standard elements defined in HTML5 specification [with some additions](http://sciter.com/developers/for-web-programmers/). CSS extended to better support Desktop UI development, e.g. flow and flex units, vertical and horizontal alignment, OS theming. 

[Sciter SDK](http://sciter.com/download/) comes with demo "browser" with builtin DOM inspector, script debugger and documentation browser:

![Sciter tools](http://sciter.com/images/sciter-tools.png)

Check <http://sciter.com> website and its [documentation resources](http://sciter.com/developers/) for engine principles, architecture and more.


## Getting started:

_Right now, before PySciter will not be published on PYPI_

1. Download [Sciter SDK](http://sciter.com/download/) and extract it somewhere.
2. Add target platform binaries to PATH: `bin` (for Windows), `bin.osx` or `bin.gtk`
3. Install pysciter: `python3 setup.py install`
4. Run minimal pysciter sample: `python3 examples/minimal.py`. Also you can run script from zip archive directly: `python3 ./archive.zip` :)


## Brief look:

Minimal sciter app is extremely small:
```python
import sciter

if __name__ == '__main__':
    frame = sciter.Window(ismain=True, uni_theme=True)
    frame.load_file("minimal.htm")
    frame.expand()
    frame.run_app()
```

It looks similar like this:

![Minimal pysciter sample](http://i.imgur.com/ojcM5JJ.png)


### Interoperability

In respect of [tiscript](http://www.codeproject.com/Articles/33662/TIScript-language-a-gentle-extension-of-JavaScript) functions calling:
```python
answer = self.call_function('script_function', "hello, python!", "and", ["other", 3, "arguments"])
```

Calling python from script can be implemented as following:
```python
def GetNativeApi(): # called from sciter.EventHandler.on_script_call
  def on_add(a, b):
      return a + b

  def on_sub(a, b):
      raise Exception("sub(%d,%d) raised exception" % (a, b))
      
  api = { 'add': on_add,  # plain function
          'sub': on_sub,  # raise exception at script
          'mul': lambda a,b: a * b }   # lambdas supported too
  return api
```

So, we can access our api now:
```js
// `view` represents window where script is runnung.
// `stdout` stream is a standard output stream (shell or debugger console, for example)

var api = view.GetNativeApi();

// returned `api` object looks like {add: function(a,b) { return a + b; }}; 
stdout.println("2 + 3 = " + api.add(2, 3)); 
```

_Check [pysciter/examples](https://github.com/pravic/pysciter/tree/master/examples) folder for more complex usage_.


## What supported right now:

* [sciter::window](https://github.com/c-smile/sciter-sdk/blob/master/include/sciter-x-window.hpp) which brings together window creation, host and event handlers
* [sciter::host](https://github.com/c-smile/sciter-sdk/blob/master/include/sciter-x-host-callback.h) extensible implementation with transparent script calls from python code
* [sciter::event_handler](https://github.com/c-smile/sciter-sdk/blob/master/include/sciter-x-behavior.h) with basic event handling (attached, document_complete, on_script_call), additional handlers will come
* [sciter::dom](https://github.com/c-smile/sciter-sdk/blob/master/include/sciter-x-dom.hpp) for HTML DOM access and manipulation methods
* [sciter::value](https://github.com/c-smile/sciter-sdk/blob/master/include/value.hpp) pythonic wrapper with sciter::script_error and sciter::native_function support


### Platforms:

* [x] Windows
* [x] OSX
* [ ] Linux (in development)

Python 3.x (2.7 in near future).

