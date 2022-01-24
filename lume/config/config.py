import os
from typing import Dict, List

import yaml
from meiga import BoolResult, Failure, isSuccess

from lume.config.get_envs import get_envs
from lume.config.install_config import InstallConfig
from lume.config.required_env_error import RequiredEnvError
from lume.config.setup_config import SetupConfig
from lume.config.step_config import StepConfig
from lume.config.uninstall_config import UninstallConfig


class Config:
    def __init__(self, lume_dict: Dict):
        self.name = lume_dict.get("name")
        self.settings = {
            "show_exit_code": lume_dict.get("settings", {}).get("show_exit_code", False)
        }

        self.required_env = lume_dict.get("required_env")
        self.shared_envs = get_envs(lume_dict)
        self._set_install_step(lume_dict)
        self._set_uninstall_step(lume_dict)
        self.strict_mode = True
        self.steps = {}
        for step_name, step in lume_dict["steps"].items():
            if step_name == "setup":
                self.steps[step_name] = SetupConfig(**step)
            else:
                self.steps[step_name] = StepConfig.from_dict(step)
                self.steps[step_name].add_shared_env(self.shared_envs)

        self.add_other_steps(lume_dict)

    def update_strict_mode(self, strict_mode: bool):
        self.strict_mode = strict_mode

    def _set_install_step(self, yaml_dict: dict):
        if yaml_dict.get("install"):
            self.install = InstallConfig.from_dict(yaml_dict.get("install"))
        else:
            self.install = InstallConfig(run=[])
        self.install.add_shared_env(self.shared_envs)

    def _set_uninstall_step(self, yaml_dict: dict):
        if yaml_dict.get("uninstall"):
            self.uninstall = UninstallConfig.from_dict(yaml_dict.get("uninstall"))
        else:
            self.uninstall = UninstallConfig(run=[])
        self.uninstall.add_shared_env(self.shared_envs)

    def check_requirements(self) -> BoolResult:
        if self.required_env and self.strict_mode:
            unmeet_required_env_messages = dict()
            for env, description in self.required_env.items():
                if env not in os.environ:
                    unmeet_required_env_messages[env] = description
            if len(unmeet_required_env_messages) > 0:
                return Failure(RequiredEnvError(unmeet_required_env_messages))
        return isSuccess

    def get_steps(self) -> List[str]:
        return list(self.steps.keys())

    def get_commands(self) -> List[str]:
        commands = []
        commands += self.get_steps()
        if self.install:
            commands.append("install")
        if self.uninstall:
            commands.append("uninstall")
        return commands

    def add_other_steps(self, yaml_dict):
        other_steps = yaml_dict.get("other_steps", dict())
        for key, filename in other_steps.items():
            with open(filename) as file:
                yaml_dict = yaml.load(file, Loader=yaml.FullLoader)
                other_shared_envs = get_envs(yaml_dict)
                self.shared_envs.update(other_shared_envs)
                for step_name, step in yaml_dict["steps"].items():
                    step_name = f"{key}:{step_name}"
                    self.steps[step_name] = StepConfig.from_dict(step)
                    self.steps[step_name].add_shared_env(self.shared_envs)
