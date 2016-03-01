"""Simple DOM example (Go sciter example port)."""

import sciter, sys

if __name__ == "__main__":
    frame = sciter.Window(ismain=True, uni_theme=False)
    frame.set_title("Inserting example")

    # load simple html
    frame.load_html(b"""<html>html</html>""")

    # create div and link as child of root node (<html>)
    div = sciter.Element.create("div", "hello, world")

    root = frame.get_root()
    root.insert(div, 0)

    # show window and run app
    frame.run_app()
