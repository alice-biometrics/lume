import os
from zipfile import BadZipFile

from google.api_core.exceptions import Forbidden, NotFound
from google.auth.exceptions import DefaultCredentialsError
from google.cloud import storage
from meiga import Failure, Result, Success

from lume.config import DependencyConfig
from lume.src.domain.services.logger import INFO, Logger
from lume.src.infrastructure.services.setup.setup_errors import (
    BadZipFileError,
    BlobNotFoundError,
    CrendentialsEnvError,
)
from lume.src.infrastructure.services.setup.setup_item import SetupItem
from lume.src.infrastructure.services.setup.setup_utils import unzip_file


class SetupItemBucket(SetupItem):
    def run(
        self, name: str, dependency_config: DependencyConfig, logger: Logger
    ) -> Result:
        dependency_path = os.path.join(self.base_path, name)
        if not os.path.exists(dependency_path):
            os.makedirs(dependency_path)
        elif dependency_config.overwrite:
            logger.log(
                INFO,
                f"{self.__class__.__name__} - dependency {name} already exists. Overwriting...",
            )
        else:
            logger.log(
                INFO,
                f"{self.__class__.__name__} - dependency {name} already exists. Skipping...",
            )
            return Success()

        if dependency_config.auth_required:
            credentials_path = os.environ.get(dependency_config.credentials_env)  # type: ignore
            if credentials_path is None or not os.path.exists(credentials_path):
                try:
                    storage_client = storage.Client()
                except DefaultCredentialsError as exc:
                    return Failure(
                        CrendentialsEnvError(
                            dependency_config.credentials_env, info=str(exc)
                        )
                    )
            else:
                storage_client = storage.Client.from_service_account_json(
                    credentials_path
                )
        else:
            storage_client = storage.Client()
        try:
            self.__download_bucket(
                storage_client, dependency_path, dependency_config.url
            )
        except NotFound:
            return Failure(BlobNotFoundError(dependency_config.url))
        except Forbidden as exc:
            return Failure(
                CrendentialsEnvError(dependency_config.credentials_env, info=str(exc))
            )

        if dependency_config.unzip:
            try:
                unzip_file(dependency_path, dependency_config.url)
            except BadZipFile:
                return Failure(BadZipFileError(name))

        return Success()

    @staticmethod
    def __download_bucket(storage_client: storage.Client, dst: str, url: str):
        filepath_parts = url.replace("gs://", "").split("/")
        filename = filepath_parts[-1]
        bucket_name = filepath_parts[0]
        bucket_filepath = "/".join(filepath_parts[1:])
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(bucket_filepath)
        blob.download_to_filename(os.path.join(dst, filename))
