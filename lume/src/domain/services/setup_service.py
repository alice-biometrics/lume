from abc import ABC, abstractmethod

from meiga import Error, NotImplementedMethodError, Result


class SetupService(ABC):
    @abstractmethod
    def execute(self) -> Result[bool, Error]:
        return NotImplementedMethodError
