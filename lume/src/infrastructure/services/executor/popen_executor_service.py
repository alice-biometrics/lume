from subprocess import Popen, PIPE
from typing import Dict

from meiga import Result, Error, isSuccess, isFailure
from lume.src.domain.services.interface_executor_service import IExecutorService
from lume.src.domain.services.interface_logger import ILogger, ERROR, INFO


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

        if return_code != 0:
            self.logger.log(ERROR, f"Error running '>> {command}'")
            return isFailure

        return isSuccess
