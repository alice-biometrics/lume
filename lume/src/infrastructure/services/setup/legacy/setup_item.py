import os
from abc import abstractmethod, ABCMeta

from _bowie.utils.asserts import assert_value_in_config
from _bowie.utils.execute_commands import execute_commands
from _bowie.utils.logger import get_logger


class SetupItem(object):
    __metaclass__ = ABCMeta
    path = None
    config = None

    def __init__(self, config, dependencies_path):
        self.__assert_config(config)
        self.config = config
        name = self.config.get("name")
        self.path = os.path.join(dependencies_path, name)
        self.logger = get_logger()

    @abstractmethod
    def run(self):
        raise NotImplementedError

    @staticmethod
    def run_setup_command(command, work_path):
        if command is not None:
            execute_commands([command], cwd=work_path)

    @staticmethod
    def already_exists(path):
        return os.path.isdir(path)

    @staticmethod
    def __assert_config(config):
        assert_value_in_config("name", config)
        assert_value_in_config("url", config)
