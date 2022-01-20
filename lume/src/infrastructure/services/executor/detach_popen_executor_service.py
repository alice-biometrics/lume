from subprocess import Popen

from meiga import Error, Result, Success

from lume.src.domain.services.executor_service import (
    DEFAULT_EXECUTOR_LOG_FILENAME,
    ExecutorService,
)
from lume.src.domain.services.logger import INFO, Logger


class DetachPopenExecutorService(ExecutorService):
    def __init__(self, logger: Logger):
        self.logger = logger

    def execute(
        self, command: str, cwd: str, log_filename: str = DEFAULT_EXECUTOR_LOG_FILENAME
    ) -> Result[bool, Error]:

        if not cwd:
            cwd = "."

        log = open(log_filename, "w")
        process = Popen("exec " + command, stdout=log, stderr=log, cwd=cwd, shell=True)

        self.logger.log(INFO, f"Open process (pid={process.pid}) >> {log_filename}")

        return Success(process)
