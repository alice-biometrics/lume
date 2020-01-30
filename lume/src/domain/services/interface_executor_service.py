from abc import ABCMeta, abstractmethod
from typing import Dict

from meiga import Result, Error, NotImplementedMethodError


class IExecutorService:
    __metaclass__ = ABCMeta

    @abstractmethod
    def info(self) -> Dict:
        return {}

    @abstractmethod
    def execute(self, command: str, cwd: str) -> Result[bool, Error]:
        return NotImplementedMethodError
