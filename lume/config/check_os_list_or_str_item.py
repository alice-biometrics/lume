from platform import machine
from sys import platform

from lume.config.check_list_or_str_item import check_list_or_str_item


def get_platform():
    if platform == "linux" or platform == "linux2":
        return "linux"
    elif platform == "darwin":
        if machine() == "arm64":
            return "macos-arm"
        return "macos"
    elif platform == "win32":
        return "windows"


def concat_list(list_of_lists_of_commands: list) -> list:
    if all(v is None for v in list_of_lists_of_commands):
        return None

    result = list()
    for list_of_commands in list_of_lists_of_commands:
        if list_of_commands is None:
            list_of_commands = list()
        result += list_of_commands
    return result


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
        current_platform = get_platform()
        platform_commands = check_list_or_str_item(kvalue, current_platform)
        all_pre_commands = check_list_or_str_item(kvalue, "all-pre")
        all_post_commands = check_list_or_str_item(kvalue, "all-post")
        all_commands = check_list_or_str_item(kvalue, "all")
        value = concat_list(
            [all_pre_commands, platform_commands, all_commands, all_post_commands]
        )
    else:
        value = check_list_or_str_item(kdict, key)

    return value
