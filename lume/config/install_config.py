from dataclasses import dataclass
from typing import List, Optional
from lume.config.check_list_or_str_item import check_list_or_str_item


@dataclass
class InstallConfig:
    run: List[str]
    cwd: Optional[str] = None

    @staticmethod
    def from_dict(kdict):
        run = check_list_or_str_item(kdict, "run", required=True)

        return InstallConfig(run=run, cwd=kdict.get("cwd"))
