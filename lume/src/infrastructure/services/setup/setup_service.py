from typing import Dict
import os

from meiga import Success, Failure

from lume.config import SetupConfig
from lume.src.domain.services.interface_logger import ILogger, INFO, WARNING
from lume.src.domain.services.interface_setup_service import ISetupService
from lume.src.infrastructure.services.setup.setup_errors import (
    ItemTypeNotSupportedError,
)
from lume.src.infrastructure.services.setup.setup_item_bucket import SetupItemBucket
from lume.src.infrastructure.services.setup.setup_item_file import SetupItemFile


class SetupService(ISetupService):
    def __init__(self, setup_config: SetupConfig, logger: ILogger):
        if not setup_config:
            return

        self.setup_config = setup_config
        self.logger = logger
        self.set_base_path(setup_config.output)
        self.item_factory = {
            "file": SetupItemFile(setup_config.output),
            "bucket": SetupItemBucket(setup_config.output),
        }

    def info(self) -> Dict:
        return {"name": self.__class__.__name__}

    def execute(self):

        if not self.setup_config:
            self.logger.log(WARNING, f"Empty config for setup")
            return

        self.logger.log(INFO, f"setup: output: {self.setup_config.output}")

        for key, value in self.setup_config.deps.items():

            self.logger.log(INFO, f"{key} : {value}")
            if value.type not in self.item_factory.keys():
                return Failure(
                    ItemTypeNotSupportedError(value.type, self.item_factory.keys())
                )

            result = self.item_factory[value.type].run(key, value, self.logger)
            if result.is_success:
                self.logger.log(INFO, f"{key}: Download successfully")
            else:
                return result

        return Success()

    @staticmethod
    def set_base_path(path):
        if not os.path.exists(path):
            os.makedirs(path)
