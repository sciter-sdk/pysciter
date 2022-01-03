# Python bindings for Sciter

[![AppVeyor status](https://ci.appveyor.com/api/projects/status/rphv883klffw9em9/branch/master?svg=true)](https://ci.appveyor.com/project/pravic/pysciter)
[![Travis Status](https://www.travis-ci.com/sciter-sdk/pysciter.svg?branch=master)](https://www.travis-ci.com/sciter-sdk/pysciter)
[![PyPI](https://img.shields.io/pypi/v/pysciter.svg)](https://pypi.python.org/pypi/PySciter)
[![License](https://img.shields.io/pypi/l/pysciter.svg)](https://pypi.python.org/pypi/PySciter)
[![Join the forums at https://sciter.com/forums](https://img.shields.io/badge/forum-sciter.com-orange.svg)](https://sciter.com/forums)

Check [this page](https://sciter.com/developers/sciter-sdk-bindings/) for other language bindings (Delphi / D / Go / .NET / Python / Rust).

----


## Introduction

Sciter is an embeddable [multiplatform](https://sciter.com/sciter/crossplatform/) HTML/CSS/script engine with GPU accelerated rendering designed to render modern desktop application UI. It's a compact, single dll/dylib/so file (4-8 mb) engine without any additional dependencies.


## Screenshots

Check the [screenshot gallery](https://github.com/oskca/sciter#sciter-desktop-ui-examples) of the desktop UI examples.


## Description

Physically Sciter is a mono library which contains:

* [HTML and CSS](https://sciter.com/developers/for-web-programmers/) rendering engine based on the H-SMILE core used in [HTMLayout](https://terrainformatica.com/a-homepage-section/htmlayout/),
* JavaScript in [Sciter.JS](https://sciter.com/sciter-js-is-the-mainstream-primary-version-of-sciter/),
* JavaScript alike [Scripting engine](https://sciter.com/developers/sciter-docs/) – core of [TIScript](https://sciter.com/developers/for-web-programmers/tiscript-vs-javascript/) which by itself is based on [c-smile](https://c-smile.sourceforge.net/) engine,
* Persistent [Database](https://sciter.com/docs/content/script/Storage.htm) (a.k.a. [JSON DB](https://terrainformatica.com/2006/10/what-the-hell-is-that-json-db/)) based on excellent DB products of [Konstantin Knizhnik](http://garret.ru/databases.html).
* [Graphics](https://sciter.com/docs/content/sciter/Graphics.htm) module that uses native graphics primitives provided by supported platforms: Direct2D on Windows 7 and above, GDI+ on Windows XP, CoreGraphics on MacOS, Cairo on Linux/GTK. Yet there is an option to use built-in [Skia/OpenGL](https://skia.org/) backend on each platform.
* Network communication module, it relies on platform HTTP client primitives and/or [Libcurl](https://curl.haxx.se/).


Internally it contains the following modules:

* **CSS** – CSS parser and the collection of parsed CSS rules, etc.
* **HTML DOM** – HTML parser and DOM tree implementation.
* **layout managers** – collection of various layout managers – text layout, default block layout, flex layouts. Support of positioned floating elements is also here. This module does the layout calculations heavy lifting. This module is also responsible for the rendering of layouts.
* **input behaviors** – a collection of built-in behaviors – code behind "active" DOM elements: `<input>`, `<select>`, `<textarea>`, etc.
* **script module** – source-to-bytecode compiler and virtual machine (VM) with compacting garbage collector (GC). This module also contains runtime implementation of standard classes and objects: Array, Object, Function and others.
* **script DOM** – runtime classes that expose DOM and DOM view (a.k.a. window) to the script.
* **graphics abstraction layer** – abstract graphics implementation that isolates the modules mentioned above from the particular platform details:
    * Direct2D/DirectWrite graphics backend (Windows);
    * GDI+ graphics backend (Windows);
    * CoreGraphics backend (Mac OS X);
    * Cairo backend (GTK on all Linux platforms);
    * Skia/OpenGL backend (all platforms)
* **core primitives** – set of common primitives: string, arrays, hash maps and so on.


Sciter supports all standard elements defined in HTML5 specification [with some additions](https://sciter.com/developers/for-web-programmers/). CSS is extended to better support the Desktop UI development, e.g. flow and flex units, vertical and horizontal alignment, OS theming.

[Sciter SDK](https://sciter.com/download/) comes with a demo "browser" with a builtin DOM inspector, script debugger and documentation viewer:

![Sciter tools](https://sciter.com/wp-content/uploads/2015/10/dom-tree-in-inspector-640x438.png)

Check <https://sciter.com> website and its [documentation resources](https://sciter.com/developers/) for engine principles, architecture and more.


## Getting started:

1. Download the [Sciter.TIS or Sciter.JS SDK](https://sciter.com/download/) and extract it somewhere.
2. Add the corresponding target platform binaries to PATH (`bin.win/x64`, `bin.osx` or `bin.lnx/x64`) and install Sciter shared library to your [LIBRARY_PATH](https://github.com/sciter-sdk/go-sciter#getting-started).
3. Install pysciter: `python3 setup.py install` or `pip install pysciter`.
4. Run the minimal pysciter sample: `python3 examples/minimal.py`. Also you can run script from zip archive directly: `python3 ./archive.zip` :)


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

It looks similar to this:

![Minimal pysciter sample](https://i.imgur.com/ojcM5JJ.png)


### Interoperability

In respect of [tiscript](https://www.codeproject.com/Articles/33662/TIScript-language-a-gentle-extension-of-JavaScript) or JavaScript functions calling:
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

So, we can access our api now from TIScript:
```js
// `view` represents window where script is runnung.
// `stdout` stream is a standard output stream (shell or debugger console, for example)

var api = view.GetNativeApi();

// returned `api` object looks like {add: function(a,b) { return a + b; }};
stdout.println("2 + 3 = " + api.add(2, 3));
```

or from JavaScript:
```js
// `Window.this` represents the window where this script is running.
const api = Window.this.GetNativeApi();
console.log("2 + 3", api.add(2, 3));
````

_Check [pysciter/examples](https://github.com/sciter-sdk/pysciter/tree/master/examples) folder for more complex usage_.


## What is supported right now:

* [x] [sciter::window](https://github.com/c-smile/sciter-sdk/blob/master/include/sciter-x-window.hpp) which brings together window creation, host and event handlers.
* [x] [sciter::host](https://github.com/c-smile/sciter-sdk/blob/master/include/sciter-x-host-callback.h) extensible implementation with transparent script calls from python code.
* [x] [sciter::event_handler](https://github.com/c-smile/sciter-sdk/blob/master/include/sciter-x-behavior.h) with basic event handling (attached, document_complete, on_script_call), additional handlers will come.
* [x] [sciter::dom](https://github.com/c-smile/sciter-sdk/blob/master/include/sciter-x-dom.hpp) for HTML DOM access and manipulation methods.
* [x] [sciter::value](https://github.com/c-smile/sciter-sdk/blob/master/include/value.hpp) pythonic wrapper with `sciter::script_error` and `sciter::native_function` support.
* [ ] [sciter::behavior_factory](https://github.com/c-smile/sciter-sdk/blob/master/include/sciter-x-behavior.h) - global factory for native behaviors.
* [ ] [sciter::graphics](https://github.com/c-smile/sciter-sdk/blob/master/include/sciter-x-graphics.hpp) - platform independent graphics native interface (can be used in native behaviors).
* [ ] [sciter::request](https://github.com/c-smile/sciter-sdk/blob/master/include/sciter-x-request.hpp) - resource request object, used for custom resource downloading and handling.
* [ ] [sciter::video](https://github.com/c-smile/sciter-sdk/blob/master/include/sciter-x-video-api.h) - custom video rendering.
* [ ] [sciter::archive](https://github.com/c-smile/sciter-sdk/blob/master/include/sciter-x-host-callback.h) - Sciter's compressed archive produced by `sdk/bin/packfolder`.
* [ ] [sciter::msg](https://github.com/c-smile/sciter-sdk/blob/master/include/sciter-x-msg) - backend-independent input event processing.
* [ ] [sciter::om](https://github.com/c-smile/sciter-sdk/blob/master/include/sciter-om.h) - Sciter Object Model, extending Sciter by native code.
* [ ] [NSE](https://sciter.com/include-library-name-native-extensions/) - native Sciter extensions.

### Platforms:

* [x] Windows
* [x] OSX
* [x] Linux
* [x] Raspberry Pi

Python 3.x.


## License

Bindings library licensed under [MIT license](https://opensource.org/licenses/MIT). Sciter Engine has the [own license terms](https://sciter.com/prices/) and [end used license agreement](https://github.com/c-smile/sciter-sdk/blob/master/license.htm) for SDK usage.
