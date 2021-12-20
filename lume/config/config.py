from typing import Dict, List

import yaml

from lume.config.install_config import InstallConfig
from lume.config.setup_config import SetupConfig
from lume.config.step_config import StepConfig, read_env_from_file


class Config:
    def __init__(self, yaml_dict: Dict = None):
        if yaml_dict is None:
            self.name = None
            self.settings = {"show_exit_code": False}
            self.install = None
            self.steps = {}
        else:
            self.name = yaml_dict.get("name")
            self.settings = {
                "show_exit_code": yaml_dict.get("settings", {}).get(
                    "show_exit_code", False
                )
            }

            shared_envs = yaml_dict.get("envs", {})
            envs_from_file = read_env_from_file(yaml_dict.get("envs_file"))
            shared_envs.update(envs_from_file)

            if yaml_dict.get("install"):
                self.install = InstallConfig.from_dict(yaml_dict.get("install"))
            else:
                self.install = InstallConfig(run=[])
            self.install.add_shared_env(shared_envs)

            self.steps = {}
            for step_name, step in yaml_dict["steps"].items():
                if step_name == "setup":
                    self.steps[step_name] = SetupConfig.from_dict(step)
                else:
                    self.steps[step_name] = StepConfig.from_dict(step)
                    self.steps[step_name].add_shared_env(shared_envs)

            self.add_other_steps(yaml_dict, shared_envs)

    def get_steps(self) -> List[str]:
        return list(self.steps.keys())

    def get_commands(self) -> List[str]:
        commands = []
        commands += self.get_steps()
        if self.install:
            commands.append("install")
        return commands

    def add_other_steps(self, yaml_dict, shared_envs):
        other_steps = yaml_dict.get("other_steps", dict())
        for key, filename in other_steps.items():
            with open(filename) as file:
                yaml_dict = yaml.load(file, Loader=yaml.FullLoader)
                other_shared_envs = yaml_dict.get("envs", {})
                envs_from_file = read_env_from_file(yaml_dict.get("envs_file"))
                other_shared_envs.update(envs_from_file)
                shared_envs.update(other_shared_envs)
                for step_name, step in yaml_dict["steps"].items():
                    step_name = f"{key}:{step_name}"
                    self.steps[step_name] = StepConfig.from_dict(step)
                    self.steps[step_name].add_shared_env(shared_envs)
