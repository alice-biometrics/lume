from abc import ABC, abstractmethod

from meiga import Error, NotImplementedMethodError, Result


class KillerService(ABC):
    @abstractmethod
    def execute(self, process) -> Result[bool, Error]:
        return NotImplementedMethodError
