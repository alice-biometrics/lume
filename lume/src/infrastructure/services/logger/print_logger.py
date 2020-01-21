from lume.src.domain.services.interface_logger import ILogger


class PrintLogger(ILogger):
    def log(self, logging_level, message):
        print(f"{logging_level}: {message}")
