import os
from zipfile import BadZipFile

import requests
from meiga import Failure, Result, Success
from requests.auth import HTTPBasicAuth

from lume.config import DependencyConfig
from lume.src.domain.services.logger import INFO, Logger
from lume.src.infrastructure.services.setup.setup_errors import (
    BadZipFileError,
    CrendentialsEnvError,
)
from lume.src.infrastructure.services.setup.setup_item import SetupItem
from lume.src.infrastructure.services.setup.setup_utils import unzip_file


class SetupItemFile(SetupItem):
    def run(
        self, name: str, dependency_config: DependencyConfig, logger: Logger
    ) -> Result:
        dependency_path = os.path.join(self.base_path, name)
        if os.path.exists(dependency_path):
            logger.log(
                INFO, f"{self.__class__.__name__} - dependency {name} already exists"
            )
            return Success()
        os.makedirs(dependency_path, exist_ok=True)

        if not dependency_config.auth_required:
            auth = None
        else:
            credentials_var = os.environ.get(dependency_config.credentials_env)
            if credentials_var is None:
                return Failure(CrendentialsEnvError(dependency_config.credentials_env))
            username, password = credentials_var.split(":")
            auth = HTTPBasicAuth(username, password)

        self.__download_file(dependency_path, dependency_config.url, auth)

        if dependency_config.unzip:
            try:
                unzip_file(dependency_path, dependency_config.url)
            except BadZipFile:
                return Failure(BadZipFileError(name))

        return Success()

    @staticmethod
    def __download_file(dst: str, url: str, auth: HTTPBasicAuth = None):
        r = requests.get(url, auth=auth, stream=True)
        dst_filename = os.path.split(url)[-1]
        with open(os.path.join(dst, dst_filename), "wb") as f:
            f.write(r.content)
