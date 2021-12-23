from typing import Optional

from pydantic import BaseModel


class DependencyConfig(BaseModel):
    type: str
    url: str
    auth_required: bool
    unzip: bool
    credentials_env: Optional[str] = None
    overwrite: Optional[bool] = False
