import pytest
import os
import shutil

from meiga.assertions import assert_success, assert_failure

from lume.config import DependencyConfig
from lume.src.infrastructure.services.logger.emojis_logger import EmojisLogger
from lume.src.infrastructure.services.setup.setup_errors import (
    CrendentialsEnvError,
    BlobNotFoundError,
)
from lume.src.infrastructure.services.setup.setup_item_bucket import SetupItemBucket


@pytest.mark.skip
@pytest.mark.unit
def test_should_download_a_valid_bucket_with_auth():
    file_setuper = SetupItemBucket(base_path="test_deps")
    dependency_config = DependencyConfig(
        type="bucket",
        url="gs://aliceonboarding/-AmBH6e1JnNcFPej9Bcvp5EJRCI=.jpg",
        auth_required=True,
        credentials_env="GCS_CREDENTIALS",
        unzip=False,
    )
    result = file_setuper.run("test-item", dependency_config, EmojisLogger())

    assert_success(result)
    assert os.path.exists("test_deps/test-item/-AmBH6e1JnNcFPej9Bcvp5EJRCI=.jpg")
    shutil.rmtree("test_deps", ignore_errors=False, onerror=None)


@pytest.mark.skip
@pytest.mark.unit
def test_should_return_error_when_wrong_bucket_name():
    shutil.rmtree("test_deps", ignore_errors=True, onerror=None)

    file_setuper = SetupItemBucket(base_path="test_deps")
    dependency_config = DependencyConfig(
        type="bucket",
        url="gs://soyunbucket/-AmBH6e1JnNcFPej9Bcvp5EJRCI=.jpg",
        auth_required=True,
        credentials_env="GCS_CREDENTIALS",
        unzip=False,
    )
    result = file_setuper.run("test-item", dependency_config, EmojisLogger())
    assert_failure(result)
    assert isinstance(result.value, BlobNotFoundError)
    shutil.rmtree("test_deps", ignore_errors=True, onerror=None)


@pytest.mark.skip
@pytest.mark.unit
def test_should_return_error_when_credentials_not_define():
    shutil.rmtree("test_deps", ignore_errors=True, onerror=None)

    file_setuper = SetupItemBucket(base_path="test_deps")
    dependency_config = DependencyConfig(
        type="bucket",
        url="gs://aliceonboarding/-AmBH6e1JnNcFPej9Bcvp5EJRCI=.jpg",
        auth_required=True,
        credentials_env="SOME_CREDENTIAL",
        unzip=False,
    )
    result = file_setuper.run("test-item", dependency_config, EmojisLogger())
    assert_failure(result)
    assert isinstance(result.value, CrendentialsEnvError)
    shutil.rmtree("test_deps", ignore_errors=True, onerror=None)


@pytest.mark.skip
@pytest.mark.unit
def test_should_return_error_when_credentials_path_not_exists():
    shutil.rmtree("test_deps", ignore_errors=True, onerror=None)

    os.environ["ERROR_CREDENTIALS"] = "/home/user/some_path/credentials.json"
    file_setuper = SetupItemBucket(base_path="test_deps")
    dependency_config = DependencyConfig(
        type="bucket",
        url="gs://aliceonboarding/-AmBH6e1JnNcFPej9Bcvp5EJRCI=.jpg",
        auth_required=True,
        credentials_env="ERROR_CREDENTIALS",
        unzip=False,
    )
    result = file_setuper.run("test-item", dependency_config, EmojisLogger())
    assert_failure(result)
    assert isinstance(result.value, CrendentialsEnvError)
    shutil.rmtree("test_deps", ignore_errors=True, onerror=None)


# @pytest.mark.unit
# def test_should_return_error_when_credentials_not_provided():
#     file_setuper = SetupItemFile(base_path="test_deps")
#     dependency_config = DependencyConfig(
#         type="file",
#         url="https://intranet.gradiant.org/nexus/repository/raw-dataset-biometrics/alice/gcs-credentials.json",
#         auth_required=True,
#         credentials_env="LOL",
#         unzip=False
#     )
#     result = file_setuper.run("test-item", dependency_config, EmojisLogger())
#     assert result.is_failure
#     assert isinstance(result.value, CrendentialsEnvError)
#     shutil.rmtree("test_deps", ignore_errors=False, onerror=None)
#
