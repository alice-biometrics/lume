from abc import ABC, abstractmethod
from typing import Optional

from meiga import Error, NotImplementedMethodError, Result

DEFAULT_EXECUTOR_LOG_FILENAME = "lume.executor.log"


class ExecutorService(ABC):
    @abstractmethod
    def execute(
        self, command: str, cwd: str, log_filename: Optional[str] = None
    ) -> Result[bool, Error]:
        return NotImplementedMethodError
