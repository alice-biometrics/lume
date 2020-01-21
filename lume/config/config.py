from dataclasses import dataclass
from typing import Dict, List

from dataclasses_json import dataclass_json

from lume.config.install_config import InstallConfig
from lume.config.setup_config import SetupConfig
from lume.config.step_config import StepConfig


@dataclass_json
@dataclass
class Config:
    name: str = None
    install: InstallConfig = None
    setup: SetupConfig = None
    steps: Dict[str, StepConfig] = None

    def get_steps(self) -> List[str]:
        return list(self.steps.keys())

    def get_commands(self) -> List[str]:
        commands = []
        if self.install:
            commands.append("install")
        if self.setup:
            commands.append("setup")
        commands += self.get_steps()
        return commands
