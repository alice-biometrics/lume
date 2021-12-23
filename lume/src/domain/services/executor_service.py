from abc import ABC, abstractmethod

from meiga import Error, NotImplementedMethodError, Result


class ExecutorService(ABC):
    @abstractmethod
    def execute(self, command: str, cwd: str) -> Result[bool, Error]:
        return NotImplementedMethodError
