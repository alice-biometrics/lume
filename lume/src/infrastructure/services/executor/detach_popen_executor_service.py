from subprocess import Popen
from typing import Dict

from meiga import Result, Error, Success
from lume.src.domain.services.interface_executor_service import IExecutorService
from lume.src.domain.services.interface_logger import ILogger, INFO


class DetachPopenExecutorService(IExecutorService):
    def __init__(self, logger: ILogger):
        self.logger = logger

    def info(self) -> Dict:
        return {"name": self.__class__.__name__}

    def execute(
        self, command: str, cwd: str, log_filename="setup_detach.log"
    ) -> Result[bool, Error]:

        if not cwd:
            cwd = "."

        log = open(log_filename, "w")
        process = Popen("exec " + command, stdout=log, stderr=log, cwd=cwd, shell=True)

        self.logger.log(INFO, f"Open process (pid={process.pid}) >> {log_filename}")

        return Success(process)
