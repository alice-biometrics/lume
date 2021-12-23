from lume.src.domain.services.logger import Logger


class NotImplementedLogger(Logger):
    def log(self, logging_level, message):
        pass
