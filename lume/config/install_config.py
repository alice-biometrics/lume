from dataclasses import dataclass
from typing import Dict, List, Optional

from lume.config.check_os_list_or_str_item import check_os_list_or_str_item


@dataclass
class InstallConfig:
    run: List[str]
    cwd: Optional[str] = None
    envs: Optional[Dict[str, str]] = None
    overwrote_envs: Optional[List[str]] = None

    def add_shared_env(self, shared_envs: Dict[str, str]):
        self.overwrote_envs = list(set(shared_envs.keys()).intersection(set(self.envs)))
        self.envs = {**shared_envs, **self.envs}

    @staticmethod
    def from_dict(kdict):
        run = check_os_list_or_str_item(kdict, "run")
        return InstallConfig(
            run=run if run else [], cwd=kdict.get("cwd"), envs=kdict.get("envs", {})
        )
