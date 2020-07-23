from dataclasses import dataclass
from typing import List, Optional

from lume.config.check_os_list_or_str_item import check_os_list_or_str_item


@dataclass
class InstallConfig:
    run: List[str]
    cwd: Optional[str] = None

    @staticmethod
    def from_dict(kdict):

        run = check_os_list_or_str_item(kdict, "run")

        return InstallConfig(run=run if run else [], cwd=kdict.get("cwd"))
