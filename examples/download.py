"""Download http content (Go sciter example port)."""

import sciter

class ContentEventHandler(sciter.EventHandler):
    """<div#content> event handler."""

    def document_complete(self):
        print("content loaded.")
        pass

    def on_data_arrived(self, nm):
        print("data arrived, uri:", nm.uri, nm.dataSize, "bytes")
        pass
    pass

class Frame(sciter.Window):
    def __init__(self):
        super().__init__(ismain=True, uni_theme=False, debug=True)
        pass

    def on_data_load(self, nm):
        # called on every html/img/css/etc resource download request
        pass

    def on_data_loaded(self, nm):
        # called on every downloaded resource 
        print("data loaded, uri:", nm.uri, nm.dataSize, "bytes")
        pass

    def load(self, url):
        self.set_title("Download Element Content")
        self.load_html(b'''<html><body><p>Url to load: <span id='url'>placed here</span></p><div id='content' style='size: *'></div></body></html>''', "/")

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
        self.handler = ContentEventHandler(element=content)
        
        # make http request to download url and place result as inner of #content
        print("load content")
        content.request_html(url)
        pass
    pass

if __name__ == '__main__':
    import sys

    print("Sciter version:", sciter.version(as_str=True))

    if len(sys.argv) < 2:
        sys.exit("at least one Sciter compatible page url is needed")
    print(sys.argv[1])

    frame = Frame()
    frame.load(sys.argv[1])
    frame.expand()
    frame.run_app(False)
