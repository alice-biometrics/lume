from platform import processor
from sys import platform

from lume.config.check_list_or_str_item import check_list_or_str_item


def get_platform():
    if platform == "linux" or platform == "linux2":
        return "linux"
    elif platform == "darwin":
        if processor() == "arm":
            return "macos-arm"
        return "macos"
    elif platform == "win32":
        return "windows"


def concat(l1, l2):
    if l1 is None and l2 is None:
        return None
    elif l1 is None:
        l1 = []
    elif l2 is None:
        l2 = []
    s = l1 + l2
    return s


def check_os_list_or_str_item(kdict, key, required=False, suffix=""):
    kvalue = kdict.get(key)
    if not kvalue and required:
        raise TypeError(f"StepConfig must contains {key}{suffix} variable")

    if isinstance(kvalue, dict):
        platform = get_platform()
        platform_commands = check_list_or_str_item(kvalue, platform)
        all_commands = check_list_or_str_item(kvalue, "all")
        value = concat(platform_commands, all_commands)
    else:
        value = check_list_or_str_item(kdict, key)

    return value
