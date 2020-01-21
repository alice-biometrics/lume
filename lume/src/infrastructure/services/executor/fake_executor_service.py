from typing import List, Dict

from meiga import Result, Error, isSuccess

from lume.src.domain.services.interface_executor_service import IExecutorService


class FakeExecutorService(IExecutorService):
    def info(self) -> Dict:
        return {"name": self.__class__.__name__}

    def execute(self, commands: List[str]) -> Result[bool, Error]:
        print("executing")
        return isSuccess
