"""Minimalistic PySciter sample for Windows."""

import sciter

if __name__ == '__main__':
    frame = sciter.Window(ismain=True, uni_theme=True)
    frame.load_file("examples/minimal.htm")
    frame.run_app()
