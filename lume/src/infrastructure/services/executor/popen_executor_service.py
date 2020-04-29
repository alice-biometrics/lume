from subprocess import Popen, PIPE
from typing import Dict

from meiga import Result, Error, isSuccess, isFailure
from lume.src.domain.services.interface_executor_service import IExecutorService
from lume.src.domain.services.interface_logger import ILogger, ERROR, INFO, WARNING


class PopenExecutorService(IExecutorService):
    def __init__(self, logger: ILogger):
        self.logger = logger

    def info(self) -> Dict:
        return {"name": self.__class__.__name__}

    def execute(self, command: str, cwd: str) -> Result[bool, Error]:

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
