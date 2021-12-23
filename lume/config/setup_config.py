from typing import Dict, Optional

from pydantic import BaseModel

from lume.config.dependency_config import DependencyConfig


class SetupConfig(BaseModel):
    deps: Dict[str, DependencyConfig]
    output: Optional[str] = "deps"
