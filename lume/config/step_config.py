import os
from dataclasses import dataclass
from typing import Dict, List, Optional

import yaml
from yaml.parser import ParserError

from lume.config.check_list_or_str_item import check_list_or_str_item
from lume.config.check_os_list_or_str_item import check_os_list_or_str_item


def read_env_from_file(filename):
    if not filename or not os.path.isfile(filename):
        return {}
    try:
        with open(filename) as file:
            envs = yaml.load(file, Loader=yaml.FullLoader)
            return envs
    except ParserError:
        return {}


@dataclass
class StepConfig:
    run: List[str]
    cwd: Optional[str] = None
    envs: Optional[Dict[str, str]] = None
    setup: Optional[List[str]] = None
    teardown: Optional[List[str]] = None
    setup_detach: Optional[Dict] = None
    wait_seconds: Optional[str] = None
    wait_http_200: Optional[str] = None
    overwrote_envs: Optional[List[str]] = None

    def add_shared_env(self, shared_envs: Dict[str, str]):
        self.overwrote_envs = list(set(shared_envs.keys()).intersection(set(self.envs)))
        self.envs = {**shared_envs, **self.envs}

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
        envs = kdict.get("envs", {})
        envs_from_file = read_env_from_file(kdict.get("envs_file"))
        envs.update(envs_from_file)

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
