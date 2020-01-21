import os

from future.utils import iteritems

from _bowie.modules.setup.setup_item_git import SetupItemGit
from _bowie.modules.setup.setup_item_file import SetupItemFile
from _bowie.utils.asserts import assert_value_in_config
from _bowie.utils.io import makedir
from _bowie.utils.logger import get_logger


DEPS_FOLDER = 'deps'


class Setuper:
    def __init__(self, config):
        self.logger = get_logger()
        self.__assert_config(config)
        self.setup_config = config.get('setup')
        if self.setup_config:
            self.dependencies_path = os.path.join(config['general']['project_path'],
                                                  DEPS_FOLDER)
            makedir(self.dependencies_path)

    def run(self):
        self.logger.info(self.__class__.__name__)
        for key, setup_item_config in iteritems(self.setup_config):
            setup_stage = self.__create_setup_item(setup_item_config, self.dependencies_path)
            setup_stage.run()

    @staticmethod
    def __create_setup_item(setup_item_config, dependencies_path):
        assert_value_in_config('type', setup_item_config)
        setup_type = setup_item_config['type']

        if setup_type == 'git':
            return SetupItemGit(setup_item_config, dependencies_path)
        if setup_type == 'file':
            return SetupItemFile(setup_item_config, dependencies_path)

        raise ValueError('SetupItem type {} does not exist'.format(type))

    @staticmethod
    def __assert_config(setup_config):
        assert_value_in_config('general', setup_config)
        assert_value_in_config('project_path', setup_config['general'])
