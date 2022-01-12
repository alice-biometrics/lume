from typing import Dict, List, Optional

from pydantic import BaseModel

from lume.config.check_os_list_or_str_item import check_os_list_or_str_item
from lume.config.get_envs import get_envs


class InstallConfig(BaseModel):
    run: List[str]
    cwd: Optional[str] = None
    envs: Dict[str, str] = dict()
    overwrote_envs: List[str] = list()

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
