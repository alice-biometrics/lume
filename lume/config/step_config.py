from dataclasses import dataclass
from typing import List, Optional, Dict
from lume.config.check_list_or_str_item import check_list_or_str_item


@dataclass
class StepConfig:
    run: List[str]
    cwd: Optional[str] = None
    envs: Optional[Dict[str, str]] = None
    setup: List[str] = None
    teardown: List[str] = None

    @staticmethod
    def from_dict(kdict):
        run = check_list_or_str_item(kdict, "run", required=True)
        setup = check_list_or_str_item(kdict, "setup", required=False)
        teardown = check_list_or_str_item(kdict, "teardown", required=False)
        return StepConfig(
            run=run,
            cwd=kdict.get("cwd"),
            envs=kdict.get("envs"),
            setup=setup,
            teardown=teardown,
        )
