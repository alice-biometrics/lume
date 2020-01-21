from lume.config import Config
from lume.src.application.use_cases.lume_use_case import LumeUseCase
from lume.src.infrastructure.services.executor.fake_executor_service import (
    FakeExecutorService,
)
from lume.src.infrastructure.services.logger.print_logger import PrintLogger
from lume.src.infrastructure.services.setup.fake_setup_service import FakeSetupService


class UseCaseBuilder:
    @staticmethod
    def lume(config: Config):

        default_executor_service = FakeExecutorService()
        default_logger = PrintLogger()
        default_setup_service = FakeSetupService(
            setup_config=config.setup, logger=default_logger
        )

        return LumeUseCase(
            config=config,
            executor_service=default_executor_service,
            setup_service=default_setup_service,
            logger=default_logger,
        )
