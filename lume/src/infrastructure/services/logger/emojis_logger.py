import emoji

from lume.src.domain.services.logger import (
    COMMAND,
    ENVAR,
    ENVAR_WARNING,
    ERROR,
    GLOBAL,
    HIGHLIGHT,
    INFO,
    WAITING,
    WARNING,
    Logger,
)
from lume.src.infrastructure.services.logger.colors import Colors

LOGGING_LEVEL = {
    HIGHLIGHT: emoji.emojize("🟩"),
    COMMAND: emoji.emojize("💻"),
    GLOBAL: emoji.emojize("🌐"),
    INFO: "",
    ERROR: emoji.emojize("💩"),
    WARNING: emoji.emojize("⚠️"),
    ENVAR: emoji.emojize("  🔸"),
    ENVAR_WARNING: emoji.emojize("  🔸"),
    WAITING: emoji.emojize("⏱ "),
}


class EmojisLogger(Logger):
    def log(self, logging_level, message):
        start, end = self.color_provider(logging_level)
        print(f"{start}{LOGGING_LEVEL[logging_level]} {message.rstrip()}{end}")

    @staticmethod
    def color_provider(logging_level):
        start = ""
        end = ""
        if logging_level == ERROR:
            start = Colors.FAIL
        elif logging_level == WARNING or logging_level == ENVAR_WARNING:
            start = Colors.WARNING
        elif logging_level == HIGHLIGHT:
            start = Colors.OKBLUE

        if start != "":
            end = Colors.ENDC

        return start, end
