import os

import yaml
from yaml.parser import ParserError


def get_envs(yaml_dict: dict) -> dict:
    envs = get_envs_from_dict(yaml_dict)
    envs_from_file = get_envs_from_file(yaml_dict)
    envs.update(envs_from_file)
    return envs


def read_env_from_file(filename):
    if not filename or not os.path.isfile(filename):
        return {}
    try:
        with open(filename) as file:
            envs = yaml.load(file, Loader=yaml.FullLoader)
            return envs
    except ParserError:
        return {}


def get_envs_from_dict(yaml_dict: dict):
    envs = yaml_dict.get(
        "env", dict()
    )  # official (it matches with GitHub actions syntax)
    if not envs:
        envs = yaml_dict.get(
            "envs", dict()
        )  # fallback to be compatible with old versions of lume.yml
    return envs


def get_envs_from_file(yaml_dict: dict):
    envs = read_env_from_file(yaml_dict.get("env_file"))  # official
    if not envs:
        envs = read_env_from_file(
            yaml_dict.get("envs_file")
        )  # fallback to be compatible with old versions of lume.yml
    return envs
