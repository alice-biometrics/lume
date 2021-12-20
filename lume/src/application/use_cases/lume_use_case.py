import os
import time
from typing import List, Tuple

import requests
from meiga import Error, Failure, Result, Success, isFailure, isSuccess
from meiga.decorators import meiga

from lume.config import Config
from lume.src.application.use_cases.messages import get_colored_command_message
from lume.src.domain.services.interface_executor_service import IExecutorService
from lume.src.domain.services.interface_killer_service import IKillerService
from lume.src.domain.services.interface_logger import (
    COMMAND,
    ENVAR,
    ENVAR_WARNING,
    ERROR,
    HIGHLIGHT,
    INFO,
    WAITING,
    WARNING,
    ILogger,
)
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


SETUP_DETACH_DEFAULT_LOG_FILENAME = "setup_detach.log"


class LumeUseCase:
    def __init__(
        self,
        config: Config,
        executor_service: IExecutorService,
        detach_executor_service: IExecutorService,
        detach_killer_service: IKillerService,
        setup_service: ISetupService,
        logger: ILogger,
    ):
        self.config = config
        self.executor_service = executor_service
        self.detach_executor_service = detach_executor_service
        self.detach_killer_service = detach_killer_service
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
                cwd = (
                    self.get_cwd(step)
                    .handle(on_failure=on_error_with_cwd, failure_args=(self, step))
                    .unwrap_or_return()
                )
                self.setup_env(step)
                processes = (
                    self.run_setup_detach(step, cwd)
                    .handle(on_failure=self.run_teardown, failure_args=(cwd, step))
                    .unwrap_or([])
                )
                self.run_setup(step, cwd).handle(
                    on_failure=self.run_teardown_detach, failure_args=processes
                ).handle(
                    on_failure=self.run_teardown, failure_args=(cwd, step)
                ).unwrap_or_return()
                self.run_commands(step, cwd, processes).unwrap_or_return()
                self.run_teardown_detach(processes)
                self.run_teardown(cwd, step)

        return isSuccess

    def setup_env(self, action):
        if action == "install":
            step = self.config.install
        else:
            step = self.config.steps.get(action)

        if step is None or not step.envs:
            return
        for envar, value in step.envs.items():
            env_original_value = os.environ.get(envar)
            os.environ[envar] = str(value)
            if env_original_value:
                self.logger.log(
                    ENVAR_WARNING,
                    f"env: overwrite {envar}={value} (Original {envar}={env_original_value})",
                )
            else:
                if envar in step.overwrote_envs:
                    self.logger.log(
                        ENVAR_WARNING,
                        f"env: overwrite {envar}={value} (Also available on shared envs on lume.yml)",
                    )
                else:
                    self.logger.log(ENVAR, f"env: set {envar}={value}")

    @meiga
    def run_setup(self, step, cwd) -> Result:
        setup_commands = self.get_setup_commands(step).unwrap_or([])
        for setup_command in setup_commands:
            message = get_colored_command_message(
                setup_command, cwd, step, prefix="setup"
            )
            self.logger.log(COMMAND, message)
            self.executor_service.execute(setup_command, cwd).unwrap_or_return()
        return isSuccess

    @meiga
    def run_setup_detach(self, step, cwd) -> Result[List, Error]:
        setup_detach_commands, log_filename = self.get_setup_detach_commands(
            step
        ).unwrap_or(([], SETUP_DETACH_DEFAULT_LOG_FILENAME))
        processes = []
        for setup_detach_command in setup_detach_commands:
            message = get_colored_command_message(
                setup_detach_command, cwd, step, prefix="setup-detach"
            )
            self.logger.log(COMMAND, message)
            process = self.detach_executor_service.execute(
                setup_detach_command, cwd, log_filename
            ).unwrap()
            if process:
                processes.append(process)
        return Success(processes)

    def run_teardown_detach(self, processes):
        if processes:
            for process in processes:
                self.detach_killer_service.execute(process)

    def wait_if_necessary(self, action):
        if action == "install":
            return
        else:
            step = self.config.steps.get(action)
            if not step.wait_seconds and not step.wait_http_200:
                return
            if step.wait_seconds:
                self.logger.log(WAITING, f"Waiting {step.wait_seconds} seconds")
                time.sleep(step.wait_seconds)

            if step.wait_http_200:
                self.logger.log(WAITING, f"Waiting for 200 -> {step.wait_http_200}")
                wait_seconds_retry = float(
                    os.environ.get("LUME_WAIT_HTTP_200_WAIT_SECONDS_RETRY", 1)
                )
                num_max_attempts = int(
                    os.environ.get("LUME_WAIT_HTTP_200_NUM_MAX_ATTEMPTS", 20)
                )

                is_ok = False
                num_attempts = 0
                for i in range(num_max_attempts):
                    num_attempts += 1
                    try:
                        response = requests.get(step.wait_http_200)
                        status = response.status_code
                        status_message = f"{status}        \033[F"
                        if status == 200:
                            is_ok = True
                            break
                        else:
                            status_message = f"Unexpected return code -> {status} | {response.text} \033[F"
                    except:  # noqa E722
                        status_message = "Connection Error\033[F"

                    self.logger.log(
                        INFO, f"  Attempt {num_attempts} -> {status_message}"
                    )
                    time.sleep(wait_seconds_retry)

                time_elapsed = round((wait_seconds_retry * num_attempts), 2)
                if is_ok:
                    self.logger.log(
                        INFO,
                        f"  Received a 200 after {num_attempts} attempts in ~{time_elapsed} seconds",
                    )
                else:
                    self.logger.log(
                        WARNING,
                        f"  Not received any 200 after {num_attempts} attempts in ~{time_elapsed} seconds",
                    )

        return

    @meiga
    def run_commands(self, step, cwd, processes) -> Result:
        self.wait_if_necessary(step)
        commands = (
            self.get_commands(step)
            .handle(on_failure=on_empty_config, failure_args=(self, step))
            .unwrap_or([])
        )
        for command in commands:
            message = get_colored_command_message(command, cwd, step)
            self.logger.log(COMMAND, message)
            self.executor_service.execute(command, cwd).handle(
                on_failure=self.run_teardown_detach, failure_args=processes
            ).handle(
                on_failure=self.run_teardown, failure_args=(cwd, step)
            ).unwrap_or_return()

        return isSuccess

    def run_teardown(self, cwd, step):
        teardown_commands = self.get_teardown_commands(step).unwrap_or([])
        for teardown_command in teardown_commands:
            message = get_colored_command_message(
                teardown_command, cwd, step, prefix="teardown"
            )
            self.logger.log(COMMAND, message)
            self.executor_service.execute(teardown_command, cwd)

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

    def get_setup_detach_commands(self, action) -> Result[Tuple[List[str], str], Error]:
        if action == "install":
            return isFailure
        else:
            step = self.config.steps.get(action)
            if not step:
                return Failure(EmptyConfigError())
            setup_detach = step.setup_detach
            if not setup_detach or not setup_detach.get("run"):
                return isFailure

        return Success(
            (
                setup_detach.get("run"),
                setup_detach.get("log_filename", SETUP_DETACH_DEFAULT_LOG_FILENAME),
            )
        )

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
