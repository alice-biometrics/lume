from dataclasses import dataclass
from dataclasses_json import dataclass_json
from typing import Dict

from lume.config.dependency_config import DependencyConfig


@dataclass_json
@dataclass
class SetupConfig:
    deps: Dict[str, DependencyConfig]
    output: str = "deps"
