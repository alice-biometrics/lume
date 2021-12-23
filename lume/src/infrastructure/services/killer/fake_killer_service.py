from meiga import Error, Result, isSuccess

from lume.src.domain.services.killer_service import KillerService


class FakeKillerService(KillerService):
    def execute(self, process: str) -> Result[bool, Error]:
        print("executing")
        return isSuccess
