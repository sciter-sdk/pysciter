"""Go sciter example port."""

import sciter

class MyEventHandler(sciter.EventHandler):

    def document_complete(self):
        print("content loaded.")
        
        pass

    def on_data_arrived(self, nm):
        print("data arrived, uri:", nm.uri, nm.dataSize)
        pass


class Frame(sciter.Window):
    def __init__(self):
        super().__init__(ismain=True, uni_theme=False, debug=True)
        pass

    def on_data_loaded(self, nm):
        print("data loaded, uri:", nm.uri, nm.dataSize)
        pass


    def load(self, url):
        self.set_title("Download Element Content")
        self.load_html(b'''<html><body><span id='url'>Url To Load</span><frame id='content'></frame></body></html>''', "/")

        # get root element
        root = self.get_root()

        # get span#url and frame#content:
        span = root.find_first('#url')
        content = root.find_first('#content')

        # replace span text with url provided
        text = span.get_text()
        span.set_text(url)
        print("span:", text)

        # install event handler to content frame to print data_arrived events
        self.handler = MyEventHandler(element=content)
        
        print("load content")
        content.request_html(url)
        pass
    pass

if __name__ == '__main__':
    import sys

    print("Sciter version:", ".".join(map(str, sciter.version())))

    if len(sys.argv) < 2:
        sys.exit("at least one Sciter compatible page url is needed")
    print(sys.argv[1])

    frame = Frame()
    frame.load(sys.argv[1])
    frame.expand()
    frame.run_app(False)
