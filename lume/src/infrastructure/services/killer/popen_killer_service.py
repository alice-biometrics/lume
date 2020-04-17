from typing import Dict
from subprocess import Popen
from meiga import Result, Error, isSuccess
from lume.src.domain.services.interface_killer_service import IKillerService
from lume.src.domain.services.interface_logger import ILogger, COMMAND

from lume.src.application.use_cases.messages import get_colored_command_message


class PopenKillerService(IKillerService):
    def __init__(self, logger: ILogger):
        self.logger = logger

    def info(self) -> Dict:
        return {"name": self.__class__.__name__}

    def execute(self, process) -> Result[bool, Error]:
        if process and isinstance(process, Popen):
            message = get_colored_command_message(
                f"Killing {process.pid}", None, "auto", "teardown_detach"
            )
            self.logger.log(COMMAND, message)
            process.kill()
            message = get_colored_command_message(
                f"Killed {process.pid}", None, "auto", "teardown_detach"
            )
            self.logger.log(COMMAND, message)

        return isSuccess
