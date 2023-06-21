from typing import Dict, List, Union

from pydantic import BaseModel, Field

from lume.config.check_os_list_or_str_item import check_os_list_or_str_item
from lume.config.get_envs import get_envs


class InstallConfig(BaseModel):
    run: List[str] = Field()
    cwd: Union[str, None] = Field(default=None)
    envs: Dict[str, str] = Field(default=dict())
    overwrote_envs: List[str] = Field(default=list())

    def add_shared_env(self, shared_envs: Dict[str, str]):
        if shared_envs and self.envs:
            self.overwrote_envs = list(
                set(shared_envs.keys()).intersection(set(self.envs))
            )

    @staticmethod
    def from_dict(kdict):
        run = check_os_list_or_str_item(kdict, "run")
        envs = get_envs(kdict)
        return InstallConfig(run=run if run else [], cwd=kdict.get("cwd"), envs=envs)
