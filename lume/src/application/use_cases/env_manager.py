import os
from typing import Dict

from lume.src.domain.services.logger import ENVAR, ENVAR_WARNING, GLOBAL, Logger
from lume.src.infrastructure.services.logger.colors import Colors


class EnvManager:
    def __init__(self, logger: Logger):
        self.logger = logger

    def set(self, envs: Dict[str, str]) -> None:
        if envs:
            self.logger.log(
                GLOBAL, f"{Colors.OKGREEN}Set Global Environment Variables{Colors.ENDC}"
            )
        for envar, value in envs.items():
            env_original_value = os.environ.get(envar)
            os.environ[envar] = str(value)
            if env_original_value:
                self.logger.log(
                    ENVAR_WARNING,
                    f"env: overwrite {envar}={value} (Original {envar}={env_original_value})",
                )
            else:
                self.logger.log(ENVAR, f"env: set {envar}={value}")

    def unset(self, envs: Dict[str, str]) -> None:
        for envar in envs.keys():
            os.unsetenv(envar)

    def set_step(self, step):
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

    def unset_step(self, step):
        if not step:
            return
        for envar in step.envs.keys():
            os.unsetenv(envar)
