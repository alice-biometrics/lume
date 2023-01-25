import os
import shutil

import pytest
from meiga.assertions import assert_failure, assert_success

from lume.config import DependencyConfig
from lume.src.infrastructure.services.logger.emojis_logger import EmojisLogger
from lume.src.infrastructure.services.setup.setup_errors import (
    BlobNotFoundError,
    CrendentialsEnvError,
)
from lume.src.infrastructure.services.setup.setup_item_bucket import SetupItemBucket

TEMPORARY_FOLDER = "test-deps"
VALID_FILE_FROM_BUCKET = "gs://lume-tests/file.txt"
VALID_FILE_FROM_BUCKET_FOLDER = "gs://lume-tests/sample_folder/file_in_folder.txt"


@pytest.mark.skipif(
    "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ,
    reason="GOOGLE_APPLICATION_CREDENTIALS must be defined",
)
@pytest.mark.unit
class TestSetupItemBucket:
    def setup_method(self):
        shutil.rmtree(TEMPORARY_FOLDER, ignore_errors=True, onerror=None)

    def should_download_a_valid_bucket_with_auth(self):
        file_setuper = SetupItemBucket(base_path=TEMPORARY_FOLDER)
        dependency_config = DependencyConfig(
            type="bucket",
            url=VALID_FILE_FROM_BUCKET,
            auth_required=True,
            credentials_env="GOOGLE_APPLICATION_CREDENTIALS",
            unzip=False,
        )
        result = file_setuper.run("test-item", dependency_config, EmojisLogger())
        assert_success(result)
        assert os.path.exists(f"{TEMPORARY_FOLDER}/test-item/file.txt")

        # now downloads the file overwriting the previous one
        dependency_config.overwrite = True
        result = file_setuper.run("test-item", dependency_config, EmojisLogger())
        assert_success(result)
        assert os.path.exists(f"{TEMPORARY_FOLDER}/test-item/file.txt")

    def should_download_a_valid_file_in_bucket_folder_with_auth(self):
        file_setuper = SetupItemBucket(base_path=TEMPORARY_FOLDER)
        dependency_config = DependencyConfig(
            type="bucket",
            url=VALID_FILE_FROM_BUCKET_FOLDER,
            auth_required=True,
            credentials_env="GOOGLE_APPLICATION_CREDENTIALS",
            unzip=False,
        )
        result = file_setuper.run("test-item", dependency_config, EmojisLogger())
        assert_success(result)
        assert os.path.exists(f"{TEMPORARY_FOLDER}/test-item/file_in_folder.txt")

        # now downloads the file overwriting the previous one
        dependency_config.overwrite = True
        result = file_setuper.run("test-item", dependency_config, EmojisLogger())
        assert_success(result)
        assert os.path.exists(f"{TEMPORARY_FOLDER}/test-item/file_in_folder.txt")

    def should_return_error_when_wrong_bucket_name(self):
        file_setuper = SetupItemBucket(base_path=TEMPORARY_FOLDER)
        dependency_config = DependencyConfig(
            type="bucket",
            url="gs://sfaasfasffasfas/myfile.md",
            auth_required=True,
            credentials_env="GOOGLE_APPLICATION_CREDENTIALS",
            unzip=False,
        )
        result = file_setuper.run("test-item", dependency_config, EmojisLogger())
        assert_failure(result, value_is_instance_of=BlobNotFoundError)

    def should_return_error_when_credentials_not_define(self):
        file_setuper = SetupItemBucket(base_path=TEMPORARY_FOLDER)
        dependency_config = DependencyConfig(
            type="bucket",
            url="gs://mybucket/myfile.md",
            auth_required=True,
            credentials_env="SOME_CREDENTIAL",
            unzip=False,
        )
        result = file_setuper.run("test-item", dependency_config, EmojisLogger())
        assert_failure(result, value_is_instance_of=CrendentialsEnvError)

    def should_return_error_when_credentials_path_not_exists(self):
        os.environ["ERROR_CREDENTIALS"] = "/home/user/some_path/credentials.json"
        file_setuper = SetupItemBucket(base_path=TEMPORARY_FOLDER)
        dependency_config = DependencyConfig(
            type="bucket",
            url="gs://mybucket/myfile.md",
            auth_required=True,
            credentials_env="ERROR_CREDENTIALS",
            unzip=False,
        )
        result = file_setuper.run("test-item", dependency_config, EmojisLogger())
        assert_failure(result, value_is_instance_of=CrendentialsEnvError)
