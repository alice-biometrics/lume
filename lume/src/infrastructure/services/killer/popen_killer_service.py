from subprocess import Popen

from meiga import Error, Result, isSuccess

from lume.src.application.use_cases.messages import get_colored_command_message
from lume.src.domain.services.killer_service import KillerService
from lume.src.domain.services.logger import COMMAND, Logger


class PopenKillerService(KillerService):
    def __init__(self, logger: Logger):
        self.logger = logger

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
