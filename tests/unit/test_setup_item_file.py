import pytest
import os
import shutil

from lume.config import DependencyConfig
from lume.src.infrastructure.services.logger.emojis_logger import EmojisLogger
from lume.src.infrastructure.services.setup.setup_errors import (
    BadZipFileError,
    CrendentialsEnvError,
)
from lume.src.infrastructure.services.setup.setup_item_file import SetupItemFile


@pytest.mark.unit
def test_should_download_a_valid_file_without_auth():
    file_setuper = SetupItemFile(base_path="test_deps")
    dependency_config = DependencyConfig(
        type="file",
        url="https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
        auth_required=False,
        credentials_env=None,
        unzip=False,
    )
    result = file_setuper.run("test-item", dependency_config, EmojisLogger())
    assert result.is_success
    assert os.path.exists("test_deps/test-item/dummy.pdf")
    shutil.rmtree("test_deps", ignore_errors=False, onerror=None)


@pytest.mark.unit
def test_should_download_a_valid_zip_without_auth():
    file_setuper = SetupItemFile(base_path="test_deps")
    dependency_config = DependencyConfig(
        type="file",
        url="https://file-examples.com/wp-content/uploads/2017/02/zip_2MB.zip",
        auth_required=False,
        credentials_env=None,
        unzip=True,
    )
    result = file_setuper.run("test-item", dependency_config, EmojisLogger())
    assert result.is_success
    assert len(os.listdir("test_deps/test-item")) > 0
    assert not os.path.exists("test_deps/test-item/zip_2MB.zip")
    shutil.rmtree("test_deps", ignore_errors=False, onerror=None)


@pytest.mark.unit
def test_should_return_error_when_wrong_url_zip_file():
    file_setuper = SetupItemFile(base_path="test_deps")
    dependency_config = DependencyConfig(
        type="file",
        url="https://file-examples.com/wp-content/uploads/2017/02/soyunarchivo.zip",
        auth_required=False,
        credentials_env=None,
        unzip=True,
    )
    result = file_setuper.run("test-item", dependency_config, EmojisLogger())
    assert result.is_failure
    assert isinstance(result.value, BadZipFileError)
    shutil.rmtree("test_deps", ignore_errors=False, onerror=None)


@pytest.mark.unit
def test_should_return_error_when_credentials_not_provided():
    file_setuper = SetupItemFile(base_path="test_deps")
    dependency_config = DependencyConfig(
        type="file",
        url="https://intranet.gradiant.org/nexus/repository/raw-dataset-biometrics/alice/gcs-credentials.json",
        auth_required=True,
        credentials_env="LOL",
        unzip=False,
    )
    result = file_setuper.run("test-item", dependency_config, EmojisLogger())
    assert result.is_failure
    assert isinstance(result.value, CrendentialsEnvError)
    shutil.rmtree("test_deps", ignore_errors=False, onerror=None)
