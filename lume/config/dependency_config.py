from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class DependencyConfig:
    type: str
    url: str
    auth_required: bool
    credentials_env: str
    unzip: bool
    overwrite: bool = False
