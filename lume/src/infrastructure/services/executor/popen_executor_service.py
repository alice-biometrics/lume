from subprocess import PIPE, Popen

from meiga import Error, Result, isFailure, isSuccess

from lume.src.domain.services.executor_service import (
    DEFAULT_EXECUTOR_LOG_FILENAME,
    ExecutorService,
)
from lume.src.domain.services.logger import ERROR, INFO, WARNING, Logger


class PopenExecutorService(ExecutorService):
    def __init__(self, logger: Logger):
        self.logger = logger

    def execute(
        self, command: str, cwd: str, log_filename: str = DEFAULT_EXECUTOR_LOG_FILENAME
    ) -> Result[bool, Error]:

        if not cwd:
            cwd = "."

        process = Popen(command, stdout=PIPE, stderr=PIPE, cwd=cwd, shell=True)

        while True:
            output = process.stdout.readline()
            return_code = process.poll()
            if return_code is not None:
                break
            if output:
                log_output = output.rstrip().decode("utf-8")
                if log_output != "":
                    self.logger.log(INFO, f"{log_output}")

        for output_err in iter(process.stderr.readline, b""):
            if output_err:
                logging_level = ERROR if return_code != 0 else WARNING
                log_output = output_err.rstrip().decode("utf-8")
                if log_output != "":
                    self.logger.log(logging_level, f"{log_output}")

        if return_code != 0:
            return isFailure

        return isSuccess
