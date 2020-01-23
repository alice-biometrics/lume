from typing import Dict

from meiga import Success

from lume.config import SetupConfig
from lume.src.domain.services.interface_logger import ILogger, INFO, WARNING
from lume.src.domain.services.interface_setup_service import ISetupService


class FakeSetupService(ISetupService):
    def __init__(self, setup_config: SetupConfig, logger: ILogger):
        self.setup_config = setup_config
        self.logger = logger

    def info(self) -> Dict:
        return {"name": self.__class__.__name__}

    def execute(self):

        if not self.setup_config:
            self.logger.log(WARNING, f"Empty config for setup")
            return Success()

        self.logger.log(INFO, f"setup: output: {self.setup_config.output}")

        for key, value in self.setup_config.deps.items():
            self.logger.log(INFO, f"{key} : {value}")
        return Success()
