import os
import shutil

import pytest
from meiga.assertions import assert_failure, assert_success

from lume.config import DependencyConfig
from lume.src.infrastructure.services.logger.emojis_logger import EmojisLogger
from lume.src.infrastructure.services.setup.setup_errors import (
    BadZipFileError,
    CrendentialsEnvError,
)
from lume.src.infrastructure.services.setup.setup_item_file import SetupItemFile

TEMPORARY_FOLDER = "test-deps"


@pytest.mark.unit
class TestSetupItemFile:
    def setup_method(self):
        shutil.rmtree(TEMPORARY_FOLDER, ignore_errors=True, onerror=None)

    def teardown_method(self):
        shutil.rmtree(TEMPORARY_FOLDER, ignore_errors=True, onerror=None)

    def should_download_a_valid_file_without_auth(self):
        file_setuper = SetupItemFile(base_path=TEMPORARY_FOLDER)
        dependency_config = DependencyConfig(
            type="file",
            url="https://raw.githubusercontent.com/alice-biometrics/lume/main/README.md",
            auth_required=False,
            credentials_env=None,
            unzip=False,
        )
        result = file_setuper.run("test-item", dependency_config, EmojisLogger())
        assert_success(result)
        assert os.path.exists(f"{TEMPORARY_FOLDER}/test-item/README.md")

    def should_download_a_valid_zip_without_auth(self):
        file_setuper = SetupItemFile(base_path=TEMPORARY_FOLDER)
        dependency_config = DependencyConfig(
            type="file",
            url="https://github.com/alice-biometrics/lume/archive/refs/heads/main.zip",
            auth_required=False,
            credentials_env=None,
            unzip=True,
        )
        result = file_setuper.run("test-item", dependency_config, EmojisLogger())
        assert_success(result)
        assert len(os.listdir(f"{TEMPORARY_FOLDER}/test-item")) > 0
        assert not os.path.exists(f"{TEMPORARY_FOLDER}/test-item/main.zip")

    def should_return_error_when_wrong_url_zip_file(self):
        file_setuper = SetupItemFile(base_path=TEMPORARY_FOLDER)
        dependency_config = DependencyConfig(
            type="file",
            url="https://file-examples.com/wp-content/uploads/2017/02/soyunarchivo.zip",
            auth_required=False,
            credentials_env=None,
            unzip=True,
        )
        result = file_setuper.run("test-item", dependency_config, EmojisLogger())
        assert_failure(result, value_is_instance_of=BadZipFileError)

    def should_return_error_when_credentials_not_provided(self):
        file_setuper = SetupItemFile(base_path=TEMPORARY_FOLDER)
        dependency_config = DependencyConfig(
            type="file",
            url="https://intranet.gradiant.org/nexus/repository/raw-dataset-biometrics/alice/gcs-credentials.json",
            auth_required=True,
            credentials_env="LOL",
            unzip=False,
        )
        result = file_setuper.run("test-item", dependency_config, EmojisLogger())
        assert_failure(result, value_is_instance_of=CrendentialsEnvError)
