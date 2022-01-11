import os
from typing import Optional

from meiga import Failure, Success

from lume.config import SetupConfig
from lume.src.domain.services.logger import INFO, WARNING, Logger
from lume.src.domain.services.setup_service import SetupService
from lume.src.infrastructure.services.setup.setup_errors import (
    ItemTypeNotSupportedError,
)
from lume.src.infrastructure.services.setup.setup_item_bucket import SetupItemBucket
from lume.src.infrastructure.services.setup.setup_item_file import SetupItemFile


class BucketSetupService(SetupService):
    def __init__(self, setup_config: Optional[SetupConfig], logger: Logger):
        if not setup_config:
            return

        self.setup_config = setup_config
        self.logger = logger
        self.set_base_path(setup_config.output)
        self.item_factory = {
            "file": SetupItemFile(setup_config.output),
            "bucket": SetupItemBucket(setup_config.output),
        }

    def execute(self):
        if not self.setup_config:
            self.logger.log(WARNING, "Empty config for setup")
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
