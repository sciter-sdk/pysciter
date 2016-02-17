"""Sciter error classes."""


class SciterError(Exception):
    """Base class for Sciter exceptions."""
    pass


class ScriptError(SciterError):
    """Raised from calling script."""
    def __init__(self, message, script=None):
        SciterError.__init__(self, message.replace("\r", "\n"))
        self.message = message
        self.script = script
