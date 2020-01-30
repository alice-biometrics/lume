import shutil
import pytest
import os

from lume.config import DependencyConfig, SetupConfig
from lume.src.infrastructure.services.logger.emojis_logger import EmojisLogger
from lume.src.infrastructure.services.setup.setup_errors import (
    ItemTypeNotSupportedError,
)
from lume.src.infrastructure.services.setup.setup_service import SetupService


@pytest.mark.unit
def test_should_download_dependency_properly():
    dependency_config = DependencyConfig(
        type="file",
        url="https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
        auth_required=False,
        credentials_env=None,
        unzip=False,
    )
    setup_config = SetupConfig(
        deps={"test-item": dependency_config}, output="test-deps"
    )
    setup_service = SetupService(setup_config, EmojisLogger())
    result = setup_service.execute()
    assert result.is_success
    assert os.path.exists("test-deps/test-item/dummy.pdf")
    shutil.rmtree("test-deps", ignore_errors=False, onerror=None)


@pytest.mark.unit
def test_should_return_error_from_item_setuper():
    dependency_config = DependencyConfig(
        type="file",
        url="https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
        auth_required=True,
        credentials_env="SOME_CREDENTIAL",
        unzip=False,
    )
    setup_config = SetupConfig(
        deps={"test-item": dependency_config}, output="test-deps"
    )
    setup_service = SetupService(setup_config, EmojisLogger())
    result = setup_service.execute()
    assert result.is_failure
    shutil.rmtree("test-deps", ignore_errors=False, onerror=None)


@pytest.mark.unit
def test_should_return_error_when_type_is_not_supported():
    dependency_config = DependencyConfig(
        type="some-type",
        url="https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
        auth_required=False,
        credentials_env=None,
        unzip=False,
    )
    setup_config = SetupConfig(
        deps={"test-item": dependency_config}, output="test-deps"
    )
    setup_service = SetupService(setup_config, EmojisLogger())
    result = setup_service.execute()
    assert result.is_failure
    assert isinstance(result.value, ItemTypeNotSupportedError)
    shutil.rmtree("test-deps", ignore_errors=False, onerror=None)
