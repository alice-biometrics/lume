import os

from google.api_core.exceptions import NotFound
from google.cloud import storage
from meiga import Failure, Success, Result

from lume.config import DependencyConfig
from lume.src.domain.services.interface_logger import ILogger, INFO
from lume.src.infrastructure.services.setup.setup_errors import CrendentialsEnvError, CrendentialsFileError, \
    BlobNotFoundError
from lume.src.infrastructure.services.setup.setup_item import SetupItem
from lume.src.infrastructure.services.setup.setup_utils import unzip_file


class SetupItemBucket(SetupItem):

    def run(self, name: str, dependency_config: DependencyConfig, logger: ILogger) -> Result:
        dependency_path = os.path.join(self.base_path, name)
        if os.path.exists(dependency_path):
            logger.log(INFO, f"{self.__class__.__name__} - dependency {name} already exists")
            return Success()
        os.makedirs(dependency_path)

        if dependency_config.auth_required:
            credentials_path = os.environ.get(dependency_config.credentials_env)
            if credentials_path is None:
                return Failure(CrendentialsEnvError(dependency_config.credentials_env))
            if not os.path.exists(credentials_path):
                return Failure(CrendentialsFileError(credentials_path))
            storage_client = storage.Client.from_service_account_json(credentials_path)
        else:
            storage_client = storage.Client()

        try:
            self.__download_bucket(storage_client, dependency_path, dependency_config.url)
        except NotFound:
            return Failure(BlobNotFoundError(dependency_config.url))

        if dependency_config.unzip:
            try:
                unzip_file(dependency_path, dependency_config.url)
            except Exception as e:
                return Failure(name)

        return Success()



    @staticmethod
    def __download_bucket(storage_client: storage.Client, dst: str, url: str):
        filepath_parts = url.split("/")
        filename = filepath_parts[-1]
        bucket_name = "/".join(filepath_parts[2:-1])
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(filename)
        blob.download_to_filename(os.path.join(dst, filename))