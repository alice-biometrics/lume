import git

from _bowie.modules.setup.setup_item import SetupItem
from _bowie.utils.io import makedir


class SetupItemGit(SetupItem):
    def __init__(self, config, dependencies_path):
        super(SetupItemGit, self).__init__(config, dependencies_path)

    def run(self):
        dependency_name = self.config.get('name')
        self.logger.info('{} - dependency {}'.format(self.__class__.__name__, dependency_name))
        if self.already_exists(self.path):
            self.logger.info('{} - dependency {} already exists'.format(self.__class__.__name__, dependency_name))
            return
        makedir(self.path)
        url = self.config.get('url')
        dst = self.path
        tag = self.config.get('tag')
        self.__clone_repository(url, dst, tag)
        command = self.config.get('command')
        SetupItem.run_setup_command(command, dst)

    @staticmethod
    def __clone_repository(url, dst, tag):
        if tag:
            git.Repo.clone_from(url, dst, branch=tag)
        else:
            git.Repo.clone_from(url, dst)
