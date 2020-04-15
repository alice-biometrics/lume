import os
from typing import List

from meiga import Result, Error, Success, Failure, isSuccess, isFailure
from meiga.decorators import meiga

from lume.config import Config
from lume.src.domain.services.interface_executor_service import IExecutorService
from lume.src.domain.services.interface_logger import (
    ILogger,
    WARNING,
    ERROR,
    HIGHLIGHT,
    COMMAND,
    ENVAR,
    ENVAR_WARNING,
)
from lume.src.domain.services.interface_setup_service import ISetupService

from lume.src.infrastructure.services.logger.colors import Colors


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
    def execute(self, steps: List[str]):

        for step in steps:
            self.logger.log(HIGHLIGHT, f"Step: {step}")

            if step == "setup":
                result = self.setup_service.execute()
                if result.is_failure:
                    self.logger.log(ERROR, f"Setup: {result.value}")
                result.unwrap_or_return()
            else:

                setup_commands = self.get_setup_commands(step).unwrap_or([])
                teardown_commands = self.get_teardown_commands(step).unwrap_or([])

                commands = (
                    self.get_commands(step)
                    .handle(on_failure=on_empty_config, failure_args=(self, step))
                    .unwrap_or([])
                )

                cwd = (
                    self.get_cwd(step)
                    .handle(on_failure=on_error_with_cwd, failure_args=(self, step))
                    .unwrap_or_return()
                )

                for setup_command in setup_commands:
                    message = self.get_colored_command_message(
                        setup_command, cwd, step, prefix="setup"
                    )
                    self.logger.log(COMMAND, message)
                    self.executor_service.execute(setup_command, cwd).unwrap_or_return()

                for command in commands:
                    message = self.get_colored_command_message(command, cwd, step)
                    self.logger.log(COMMAND, message)
                    self.executor_service.execute(command, cwd).handle(
                        on_failure=self.run_teardown,
                        failure_args=(teardown_commands, cwd, step),
                    ).unwrap_or_return()

                self.run_teardown(teardown_commands, cwd, step)

        return isSuccess

    def run_teardown(self, teardown_commands, cwd, step):
        for teardown_command in teardown_commands:
            message = self.get_colored_command_message(
                teardown_command, cwd, step, prefix="teardown"
            )
            self.logger.log(COMMAND, message)
            self.executor_service.execute(teardown_command, cwd).unwrap_or_return()

    def get_colored_command_message(self, command, cwd, step, prefix=None):
        message = (
            f"{Colors.OKBLUE}{step}{Colors.ENDC} {Colors.BOLD}>> {command}{Colors.ENDC}"
            if not cwd
            else f"{Colors.OKBLUE}{step}{Colors.ENDC} {Colors.HEADER}[cwd={cwd}]{Colors.ENDC} {Colors.BOLD}>> {command}{Colors.ENDC}"
        )
        if prefix:
            message = f"{Colors.WARNING}{prefix}{Colors.ENDC} | {message}"
        return message

    def get_commands(self, action) -> Result[List[str], Error]:
        if action == "install":
            if not self.config.install:
                return Failure(EmptyConfigError())
            commands = self.config.install.run
        else:
            step = self.config.steps.get(action)
            self.setup_env(step)
            if not step:
                return Failure(EmptyConfigError())
            commands = step.run

        return Success(commands)

    def get_setup_commands(self, action) -> Result[List[str], Error]:
        if action == "install":
            return isFailure
        else:
            step = self.config.steps.get(action)
            if not step:
                return Failure(EmptyConfigError())
            setup_commands = step.setup
            if not setup_commands:
                return isFailure

        return Success(setup_commands)

    def get_teardown_commands(self, action) -> Result[List[str], Error]:
        if action == "install":
            return isFailure
        else:
            step = self.config.steps.get(action)
            if not step:
                return Failure(EmptyConfigError())
            teardown_commands = step.teardown
            if not teardown_commands:
                return isFailure

        return Success(teardown_commands)

    def setup_env(self, step):
        if not step.envs:
            return
        for envar, value in step.envs.items():
            env_original_value = os.environ.get(envar)
            os.environ[envar] = value
            if env_original_value:
                self.logger.log(
                    ENVAR_WARNING,
                    f"envvar: overwrite {envar}={value} (Original {envar}={env_original_value})",
                )
            else:
                self.logger.log(ENVAR, f"envvar: set {envar}={value}")

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
