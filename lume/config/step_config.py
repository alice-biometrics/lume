from dataclasses import dataclass
from typing import List, Optional, Dict


@dataclass
class StepConfig:
    run: List[str]
    cwd: Optional[str] = None
    envs: Optional[Dict[str, str]] = None
    setup: List[str] = None
    teardown: List[str] = None

    @staticmethod
    def from_dict(kdict):
        run = StepConfig.check_list_or_str_item(kdict, "run", required=True)
        setup = StepConfig.check_list_or_str_item(kdict, "setup", required=False)
        teardown = StepConfig.check_list_or_str_item(kdict, "teardown", required=False)
        return StepConfig(
            run=run,
            cwd=kdict.get("cwd"),
            envs=kdict.get("envs"),
            setup=setup,
            teardown=teardown,
        )

    @staticmethod
    def check_list_or_str_item(kdict, key, required=False):
        kvalue = kdict.get(key)
        if not kvalue and required:
            raise TypeError(f"StepConfig must contains {key} variable")

        if isinstance(kvalue, str):
            value = [kvalue]
        elif isinstance(kvalue, list):
            value = kvalue
        else:
            if required:
                raise TypeError(
                    f"StepConfig must contains {key} variable (Only list and str is supported)"
                )
            else:
                value = None
        return value
