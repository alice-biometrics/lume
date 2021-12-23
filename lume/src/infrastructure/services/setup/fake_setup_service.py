from meiga import Success

from lume.config import SetupConfig
from lume.src.domain.services.logger import INFO, WARNING, Logger
from lume.src.domain.services.setup_service import SetupService


class FakeSetupService(SetupService):
    def __init__(self, setup_config: SetupConfig, logger: Logger):
        self.setup_config = setup_config
        self.logger = logger

    def execute(self):

        if not self.setup_config:
            self.logger.log(WARNING, "Empty config for setup")
            return Success()

        self.logger.log(INFO, f"setup: output: {self.setup_config.output}")

        for key, value in self.setup_config.deps.items():
            self.logger.log(INFO, f"{key} : {value}")
        return Success()
