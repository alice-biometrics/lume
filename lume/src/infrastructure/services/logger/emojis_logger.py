import emoji
from lume.src.domain.services.interface_logger import (
    ILogger,
    INFO,
    WARNING,
    ERROR,
    HIGHLIGHT,
)

LOGGING_LEVEL = {
    HIGHLIGHT: emoji.emojize("🔥"),
    INFO: emoji.emojize("👩‍💻 >>"),
    ERROR: emoji.emojize("❌ >>"),
    WARNING: emoji.emojize("🧐 >>"),
}


class EmojisLogger(ILogger):
    def log(self, logging_level, message):
        print(f"{LOGGING_LEVEL[logging_level]} {message.rstrip()}")
