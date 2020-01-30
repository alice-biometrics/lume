import os
from typing import List

from meiga import Result, Error, Success, Failure
from meiga.decorators import meiga

from lume.config import Config
from lume.src.domain.services.interface_executor_service import IExecutorService
from lume.src.domain.services.interface_logger import ILogger, INFO, WARNING, ERROR
from lume.src.domain.services.interface_setup_service import ISetupService


class EmptyConfigError(Error):
    pass


class ActionNotFoundError(Error):
    pass


class CwdIsNotADirectoryError(Error):
    pass


def on_empty_config(self, action):
    self.logger.log(WARNING, f"Empty config for {action}")


def on_error_with_cwd(self, action):
    self.logger.log(
        WARNING, f"Given execution directory (cwd) for {action} action is not valid"
    )


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
                result = self.setup_service.execute()
                if result.is_failure:
                    self.logger.log(ERROR, f"Setup: {result.value}")
                result.unwrap_or_throw()
            else:
                commands = (
                    self.get_commands(action)
                    .handle(on_failure=on_empty_config, failure_args=(self, action))
                    .unwrap_or([])
                )

                result = self.get_cwd(action).handle(
                    on_failure=on_error_with_cwd, failure_args=(self, action)
                )

                if result.is_failure:
                    continue

                cwd = result.unwrap()
                for command in commands:
                    message = (
                        f"{action} >> {command}"
                        if not cwd
                        else f"{action} [cwd={cwd}] >> {command}"
                    )
                    self.logger.log(INFO, message)
                    self.executor_service.execute(command, cwd).unwrap_or_throw()

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

    def get_cwd(self, action) -> Result[str, Error]:
        if action == "install":
            if not self.config.install:
                return Success(None)
            cwd = self.config.install.cwd
            if cwd and not os.path.isdir(cwd):
                return Failure(CwdIsNotADirectoryError())
            return Success(cwd)
        else:
            if not self.config.steps:
                return Success(None)
            step = self.config.steps.get(action)
            if step:
                cwd = step.cwd
                if cwd and not os.path.isdir(cwd):
                    return Failure(CwdIsNotADirectoryError())
                return Success(cwd)
            else:
                return Failure(ActionNotFoundError())
