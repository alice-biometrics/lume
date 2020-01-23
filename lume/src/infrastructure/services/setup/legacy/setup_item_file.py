import os
import zipfile

import shutil

from _bowie.modules.setup.setup_item import SetupItem
from _bowie.utils.request_utils import download_file
from _bowie.utils.io import makedir
from _bowie.utils.request_credentials import get_credentials
from _bowie.utils.io import remove


class SetupItemFile(SetupItem):
    def __init__(self, config, dependencies_path):
        super(SetupItemFile, self).__init__(config, dependencies_path)

    def run(self):
        dependency_name = self.config.get('name')
        self.logger.info('{} - dependency {}'.format(self.__class__.__name__, dependency_name))
        if self.already_exists(self.path):
            self.logger.info('{} - dependency {} already exists'.format(self.__class__.__name__, dependency_name))
            return
        makedir(self.path)
        url = self.config.get('url')
        dst = self.path
        self.__download_file(url, dst)

        unzip = self.config.get('unzip')
        if unzip and unzip.lower() == 'true':
            self.__unzip_file(dst)

        command = self.config.get('command')
        self.run_setup_command(command, dst)

    def __unzip_file(self, dst):
        file_name = self.config['url'].split('/')[-1]
        path_zipfile = os.path.join(dst, file_name)
        zip_ref = zipfile.ZipFile(path_zipfile, 'r')
        zip_ref.extractall(dst)
        zip_ref.close()
        os.remove(path_zipfile)

        if self.__contain_one_folder(dst):
            content = os.listdir(dst)
            name_path = content[0]
            self.__move_content(os.path.join(dst, name_path), dst)
            remove(os.path.join(dst, name_path))

    def __download_file(self, url, dst):
        auth_required = self.config.get('auth_required')
        if not auth_required or auth_required.lower() == 'false':
            download_file(url, dst)
        else:
            env = self.config.get('credentials_env')
            if env:
                user, password = get_credentials(env)
            else:
                user, password = get_credentials()
            download_file(url, dst, user, password)

    @staticmethod
    def __contain_one_folder(path):
        content = os.listdir(path)
        if len(content) == 1 and os.path.isdir(os.path.join(path, content[0])):
            return True
        return False

    @staticmethod
    def __move_content(unzip_directory_path, dst):
        unzip_directory_path_content = os.listdir(unzip_directory_path)
        for item_name in unzip_directory_path_content:
            shutil.move(os.path.join(unzip_directory_path, item_name), dst)
