from lume.config import Config
from lume.src.application.use_cases.lume_use_case import LumeUseCase
from lume.src.infrastructure.services.executor.popen_executor_service import (
    PopenExecutorService,
)
from lume.src.infrastructure.services.logger.emojis_logger import EmojisLogger
from lume.src.infrastructure.services.setup.setup_service import SetupService
from lume.src.infrastructure.services.executor.detach_popen_executor_service import (
    DetachPopenExecutorService,
)
from lume.src.infrastructure.services.killer.popen_killer_service import (
    PopenKillerService,
)


class UseCaseBuilder:
    @staticmethod
    def lume(config: Config):

        default_logger = EmojisLogger()
        default_executor_service = PopenExecutorService(logger=default_logger)
        default_detach_executor_service = DetachPopenExecutorService(
            logger=default_logger
        )
        default_detach_killer_service = PopenKillerService(logger=default_logger)
        setup_config = config.steps["setup"] if "setup" in config.steps else None
        default_setup_service = SetupService(
            setup_config=setup_config, logger=default_logger
        )

        return LumeUseCase(
            config=config,
            executor_service=default_executor_service,
            detach_executor_service=default_detach_executor_service,
            detach_killer_service=default_detach_killer_service,
            setup_service=default_setup_service,
            logger=default_logger,
        )
