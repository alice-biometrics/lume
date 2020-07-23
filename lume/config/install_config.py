from dataclasses import dataclass
from typing import List, Optional
from lume.config.check_list_or_str_item import check_list_or_str_item
from sys import platform


def get_platform():
    if platform == "linux" or platform == "linux2":
        return "linux"
    elif platform == "darwin":
        return "macos"
    elif platform == "win32":
        return "windows"


def check_os_list_or_str_item(kdict, required=False, suffix=""):
    kvalue = kdict.get("run")
    if not kvalue and required:
        raise TypeError(f"StepConfig must contains run {suffix} variable")

    if isinstance(kvalue, dict):
        platform = get_platform()
        platform_commands = check_list_or_str_item(kvalue, platform)
        all_commands = check_list_or_str_item(kvalue, "all")
        value = platform_commands + all_commands
    else:
        value = check_list_or_str_item(kdict, "run")
    return value


@dataclass
class InstallConfig:
    run: List[str]
    cwd: Optional[str] = None

    @staticmethod
    def from_dict(kdict):

        run = check_os_list_or_str_item(kdict, "run")

        return InstallConfig(run=run if run else [], cwd=kdict.get("cwd"))
