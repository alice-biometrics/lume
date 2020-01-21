from lume.src.domain.services.interface_logger import ILogger


class NotImplementedLogger(ILogger):
    def log(self, logging_level, message):
        pass
