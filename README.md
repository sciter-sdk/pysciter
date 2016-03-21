# Python bindings for Sciter

_Check [this page](http://sciter.com/developers/sciter-sdk-bindings/) for another languages._

----

Sciter is an embeddable [multiplatform](http://sciter.com/sciter/crossplatform/) HTML/CSS/script engine with GPU accelerated rendering designed to render modern desktop application UI. It's a compact, single dll/dylib/so file (4-8 mb), engine without any additional dependencies.

Check the [screenshot gallery](https://github.com/oskca/sciter#sciter-desktop-ui-examples) of the desktop UI examples.

Physically Sciter is a mono library which contains:

* [HTML and CSS](http://sciter.com/developers/for-web-programmers/) rendering engine based on the H-SMILE core used in [HTMLayout](http://www.terrainformatica.com/htmlayout/main.whtm),
* JavaScript alike [Scripting engine](http://sciter.com/developers/sciter-docs/) – core of [TIScript](http://sciter.com/developers/for-web-programmers/tiscript-vs-javascript/) which by itself is based on [c-smile](http://c-smile.sourceforge.net/) engine,
* Persistent [Database](http://sciter.com/docs/content/script/Storage.htm) (a.k.a. [JSON DB](http://terrainformatica.com/2006/10/what-the-hell-is-that-json-db/)) based on excellent DB products of [Konstantin Knizhnik](http://garret.ru/databases.html).
* [Graphics](http://sciter.com/docs/content/sciter/Graphics.htm) module using excellent AGG library of Maxim Shemanarev at [www.antigrain.com](http://antigrain.com).
* Network communication module, it relies on [Libcurl](http://curl.haxx.se/), the Great.

Sciter supports all standard elements defined in HTML5 specification [with some additions](http://sciter.com/developers/for-web-programmers/). CSS extended to better support Desktop UI development, e.g. flow and flex units, vertical and horizontal alignment, OS theming.

[Sciter SDK](http://sciter.com/download/) comes with demo "browser" with builtin DOM inspector, script debugger and documentation browser:

![Sciter tools](http://sciter.com/images/sciter-tools.png)

Check <http://sciter.com> website and its [documentation resources](http://sciter.com/developers/) for engine principles, architecture and more.


## Getting started:

_Right now, before PySciter will not be published on PYPI_

1. Download [Sciter SDK](http://sciter.com/download/) and extract it somewhere.
2. Add target platform binaries to PATH (`bin`, `bin.osx` or `bin.gtk`) and install Sciter shared library to your LIBRARY_PATH.
3. Install pysciter: `python3 setup.py install`.
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

* [x] [sciter::window](https://github.com/c-smile/sciter-sdk/blob/master/include/sciter-x-window.hpp) which brings together window creation, host and event handlers
* [x] [sciter::host](https://github.com/c-smile/sciter-sdk/blob/master/include/sciter-x-host-callback.h) extensible implementation with transparent script calls from python code
* [x] [sciter::event_handler](https://github.com/c-smile/sciter-sdk/blob/master/include/sciter-x-behavior.h) with basic event handling (attached, document_complete, on_script_call), additional handlers will come
* [x] [sciter::dom](https://github.com/c-smile/sciter-sdk/blob/master/include/sciter-x-dom.hpp) for HTML DOM access and manipulation methods
* [x] [sciter::value](https://github.com/c-smile/sciter-sdk/blob/master/include/value.hpp) pythonic wrapper with sciter::script_error and sciter::native_function support
* [ ] [sciter::graphics](https://github.com/c-smile/sciter-sdk/blob/master/include/sciter-x-graphics.hpp) - platform independent graphics native interface (can be used in native behaviors)
* [ ] [sciter::request](https://github.com/c-smile/sciter-sdk/blob/master/include/sciter-x-request.hpp) - resource request object, used for custom resource downloading and handling
* [ ] [sciter::video](https://github.com/c-smile/sciter-sdk/blob/master/include/sciter-x-video-api.h) - custom video rendering
* [ ] [sciter::archive](https://github.com/c-smile/sciter-sdk/blob/master/include/sciter-x-host-callback.h) - Sciter's compressed archive produced by sdk/bin/packfolder


### Platforms:

* [x] Windows
* [x] OSX
* [x] Linux

Python 3.x (2.7 in near future).

