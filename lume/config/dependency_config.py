from typing import Optional

from pydantic import BaseModel


class DependencyConfig(BaseModel):
    type: str
    url: str
    unzip: bool
    auth_required: Optional[bool] = False
    credentials_env: Optional[str] = None
    overwrite: Optional[bool] = False
