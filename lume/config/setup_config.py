from typing import Dict

from pydantic import BaseModel

from lume.config.dependency_config import DependencyConfig


class SetupConfig(BaseModel):
    deps: Dict[str, DependencyConfig]
    output: str = "deps"
