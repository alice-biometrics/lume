from lume.config import Config
from lume.src.application.use_cases.lume_use_case import LumeUseCase
from lume.src.infrastructure.services.executor.popen_executor_service import (
    PopenExecutorService,
)
from lume.src.infrastructure.services.logger.emojis_logger import EmojisLogger
from lume.src.infrastructure.services.setup.setup_service import SetupService


class UseCaseBuilder:
    @staticmethod
    def lume(config: Config):

        default_logger = EmojisLogger()
        default_executor_service = PopenExecutorService(logger=default_logger)
        default_setup_service = SetupService(
            setup_config=config.setup, logger=default_logger
        )

        return LumeUseCase(
            config=config,
            executor_service=default_executor_service,
            setup_service=default_setup_service,
            logger=default_logger,
        )
