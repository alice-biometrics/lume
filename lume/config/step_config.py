from typing import Dict, List, Optional

from pydantic import BaseModel

from lume.config.check_list_or_str_item import check_list_or_str_item
from lume.config.check_os_list_or_str_item import check_os_list_or_str_item
from lume.config.get_envs import get_envs


class StepConfig(BaseModel):
    run: List[str]
    cwd: Optional[str] = None
    envs: Dict[str, str] = dict()
    setup: Optional[List[str]] = None
    teardown: Optional[List[str]] = None
    setup_detach: Optional[Dict] = None
    wait_seconds: Optional[int] = None
    wait_http_200: Optional[str] = None
    overwrote_envs: List[str] = list()

    def add_shared_env(self, shared_envs: Dict[str, str]):
        if shared_envs and self.envs:
            self.overwrote_envs = list(
                set(shared_envs.keys()).intersection(set(self.envs))
            )

    @staticmethod
    def from_dict(kdict):
        run = check_os_list_or_str_item(kdict, "run", required=True)
        setup = check_os_list_or_str_item(kdict, "setup", required=False)
        teardown = check_os_list_or_str_item(kdict, "teardown", required=False)
        setup_detach = kdict.get("setup_detach")
        if setup_detach:
            setup_detach["run"] = check_list_or_str_item(
                setup_detach, "run", required=True, suffix=" (setup_detach)"
            )
        envs = get_envs(kdict)
        return StepConfig(
            run=run,
            cwd=kdict.get("cwd"),
            envs=envs,
            setup=setup,
            teardown=teardown,
            setup_detach=setup_detach,
            wait_seconds=kdict.get("wait_seconds"),
            wait_http_200=kdict.get("wait_http_200"),
        )
