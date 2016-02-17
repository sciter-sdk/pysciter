"""Minimalistic PySciter sample for Windows."""

import sciter

# main frame
class Frame(sciter.Window):
    def __init__(self):
        super().__init__(ismain=True, uni_theme=True)
        pass


def main():
    frame = Frame()
    frame.load_file("examples/minimal.htm")
    frame.set_title("PySciter")
    frame.expand()
    frame.run_app()

main()
