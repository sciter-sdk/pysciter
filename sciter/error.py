"""Sciter error classes."""


class SciterError(Exception):
    """Base class for Sciter exceptions."""
    pass


class ScriptError(SciterError):
    """Raised by runtime from calling script when script error occured (e.g. bad syntax)."""
    def __init__(self, message, script=None):
        super().__init__(self, message.replace("\r", "\n"))
        self.message = message
        self.script = script

    def __repr__(self):
        return '%s("%s") at "%s"' % (type(self).__name__, self.message.replace("\r", "\n").rstrip(), self.script if self.script else "<>")

    def __str__(self):
        return type(self).__name__ + ": " + self.message.replace("\r", "\n").rstrip()
    pass


class ScriptException(ScriptError):
    """Raised by script by throwing or returning Error instance."""
    def __init__(self, message, script=None):
        super().__init__(message, script)
        pass
