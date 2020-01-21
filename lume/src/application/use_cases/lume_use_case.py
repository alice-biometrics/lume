from typing import List

from meiga import Result, Error, Success, Failure
from meiga.decorators import meiga

from lume.config import Config
from lume.src.domain.services.interface_executor_service import IExecutorService
from lume.src.domain.services.interface_logger import ILogger, INFO, WARNING
from lume.src.domain.services.interface_setup_service import ISetupService


class EmptyConfigError(Error):
    pass


def on_empty_config(self, action):
    self.logger.log(WARNING, f"Empty config for {action}")


class LumeUseCase:
    def __init__(
        self,
        config: Config,
        executor_service: IExecutorService,
        setup_service: ISetupService,
        logger: ILogger,
    ):
        self.config = config
        self.executor_service = executor_service
        self.setup_service = setup_service
        self.logger = logger

    @meiga
    def execute(self, actions: List[str]):

        for action in actions:
            self.logger.log(INFO, f"Action: {action}")

            if action == "setup":
                self.setup_service.execute()
            else:
                commands = (
                    self.get_commands(action)
                    .handle(on_failure=on_empty_config, failure_args=(self, action))
                    .unwrap_or([])
                )
                for command in commands:
                    self.logger.log(INFO, f"{action} >> {command}")
                    self.executor_service.execute(command)

    def get_commands(self, action) -> Result[List[str], Error]:
        if action == "install":
            if not self.config.install:
                return Failure(EmptyConfigError())
            commands = self.config.install.run
        else:
            step = self.config.steps.get(action)
            if not step:
                return Failure(EmptyConfigError())
            commands = step.run

        return Success(commands)
