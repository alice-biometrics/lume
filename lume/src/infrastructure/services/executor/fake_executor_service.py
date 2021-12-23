from meiga import Error, Result, isSuccess

from lume.src.domain.services.executor_service import ExecutorService


class FakeExecutorService(ExecutorService):
    def execute(self, command: str, cwd: str) -> Result[bool, Error]:
        print("executing")
        return isSuccess
