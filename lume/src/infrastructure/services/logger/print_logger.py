from lume.src.domain.services.logger import Logger


class PrintLogger(Logger):
    def log(self, logging_level, message):
        print(f"{logging_level}: {message}")
