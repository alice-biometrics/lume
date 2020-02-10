from typing import Dict, List
from lume.config.install_config import InstallConfig
from lume.config.setup_config import SetupConfig
from lume.config.step_config import StepConfig


class Config:
    def __init__(self, yaml_dict: Dict = None):
        if yaml_dict is None:
            self.name = None
            self.install = None
            self.steps = {}
        else:
            self.name = yaml_dict.get("name")
            self.install = InstallConfig.from_dict(yaml_dict.get("install"))
            self.steps = {}
            for step_name, step in yaml_dict["steps"].items():
                if step_name == "setup":
                    self.steps[step_name] = SetupConfig.from_dict(step)
                else:
                    self.steps[step_name] = StepConfig.from_dict(step)

    def get_steps(self) -> List[str]:
        return list(self.steps.keys())

    def get_commands(self) -> List[str]:
        commands = []
        commands += self.get_steps()
        if self.install:
            commands.append("install")
        return commands
