import os
import shutil

import pytest
from meiga.assertions import assert_failure, assert_success

from lume.config import Config, DependencyConfig, SetupConfig
from lume.src.infrastructure.services.logger.emojis_logger import EmojisLogger
from lume.src.infrastructure.services.logger.fake_logger import FakeLogger
from lume.src.infrastructure.services.setup.setup_errors import (
    ItemTypeNotSupportedError,
)
from lume.src.infrastructure.services.setup.setup_service import BucketSetupService

TEMPORARY_FOLDER = "test-deps"


@pytest.mark.unit
class TestSetupService:
    def should_download_dependency_properly(self):
        shutil.rmtree(TEMPORARY_FOLDER, ignore_errors=True, onerror=None)
        dependency_config = DependencyConfig(
            type="file",
            url="https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
            auth_required=False,
            credentials_env=None,
            unzip=False,
        )
        setup_config = SetupConfig(
            deps={"test-item": dependency_config}, output=TEMPORARY_FOLDER
        )
        setup_service = BucketSetupService(setup_config, EmojisLogger())
        result = setup_service.execute()
        assert_success(result)
        assert os.path.exists(f"{TEMPORARY_FOLDER}/test-item/dummy.pdf")
        shutil.rmtree(TEMPORARY_FOLDER, ignore_errors=True, onerror=None)

    def should_return_error_from_item_setuper(self):
        dependency_config = DependencyConfig(
            type="file",
            url="https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
            auth_required=True,
            credentials_env="SOME_CREDENTIAL",
            unzip=False,
        )
        setup_config = SetupConfig(
            deps={"test-item": dependency_config}, output=TEMPORARY_FOLDER
        )
        setup_service = BucketSetupService(setup_config, EmojisLogger())
        result = setup_service.execute()
        assert_failure(result)

    def should_return_error_when_type_is_not_supported(self):
        dependency_config = DependencyConfig(
            type="some-type",
            url="https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf",
            auth_required=False,
            credentials_env=None,
            unzip=False,
        )
        setup_config = SetupConfig(
            deps={"test-item": dependency_config}, output=TEMPORARY_FOLDER
        )
        setup_service = BucketSetupService(setup_config, EmojisLogger())
        result = setup_service.execute()
        assert_failure(result, value_is_instance_of=ItemTypeNotSupportedError)

    def should_work_fine_even_none_setup_config_is_given(self):
        given_empty_config = Config()
        fake_logger = FakeLogger()
        _ = BucketSetupService(
            setup_config=given_empty_config.steps.get("config"), logger=fake_logger
        )
