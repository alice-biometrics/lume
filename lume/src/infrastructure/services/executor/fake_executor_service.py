from meiga import Error, Result, isSuccess

from lume.src.domain.services.executor_service import (
    DEFAULT_EXECUTOR_LOG_FILENAME,
    ExecutorService,
)


class FakeExecutorService(ExecutorService):
    def execute(
        self, command: str, cwd: str, log_filename: str = DEFAULT_EXECUTOR_LOG_FILENAME
    ) -> Result[bool, Error]:
        print("executing")
        return isSuccess
