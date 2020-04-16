from typing import Dict

from meiga import Result, Error, isSuccess

from lume.src.domain.services.interface_killer_service import IKillerService


class FakeKillerService(IKillerService):
    def info(self) -> Dict:
        return {"name": self.__class__.__name__}

    def execute(self, process: str) -> Result[bool, Error]:
        print("executing")
        return isSuccess
