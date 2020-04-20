from abc import ABCMeta, abstractmethod

CRITICAL = 50
FATAL = CRITICAL
ERROR = 40
COMMAND = 60
ENVAR = 70
ENVAR_WARNING = 80
WAITING = 90
WARNING = 30
WARN = WARNING
INFO = 20
DEBUG = 10
NOTSET = 0
HIGHLIGHT = 100


class ILogger:

    __metaclass__ = ABCMeta

    @abstractmethod
    def log(self, logging_level: int, message: str):
        return NotImplementedError
