from dataclasses import dataclass
from typing import List, Optional, Dict


@dataclass
class StepConfig:
    run: List[str]
    cwd: Optional[str] = None
    envs: Optional[Dict[str, str]] = None

    @staticmethod
    def from_dict(kdict):
        krun = kdict.get("run")
        if not krun:
            raise TypeError("StepConfig must contains run variable")
        if isinstance(krun, str):
            run = [krun]
        elif isinstance(krun, list):
            run = krun
        else:
            raise TypeError(
                "StepConfig must contains run variable (Only list and str is supported)"
            )

        return StepConfig(run=run, cwd=kdict.get("cwd"), envs=kdict.get("envs"))

    # setup: List[str] = None
    # teardown: List[str] = None