import pytest

from lume.config import Config
from lume.src.application.use_cases.lume_use_case import LumeUseCase
from lume.src.domain.services.interface_logger import WARNING, INFO
from lume.src.infrastructure.services.executor.fake_executor_service import (
    FakeExecutorService,
)
from lume.src.infrastructure.services.logger.fake_logger import FakeLogger
from lume.src.infrastructure.services.setup.fake_setup_service import FakeSetupService


@pytest.mark.unit
@pytest.mark.parametrize("given_command", ["install", "setup"])
def test_should_repr_as_expected_an_error_with_message(given_command):

    given_empty_config = Config()
    fake_executor_service = FakeExecutorService()
    fake_logger = FakeLogger()
    fake_setup_service = FakeSetupService(
        setup_config=given_empty_config.steps.get("setup"), logger=fake_logger
    )

    lume_use_case = LumeUseCase(
        config=given_empty_config,
        executor_service=fake_executor_service,
        setup_service=fake_setup_service,
        logger=fake_logger,
    )

    lume_use_case.execute([f"{given_command}"])

    first_logging_message = fake_logger.get_logging_messages()[0]
    second_logging_message = fake_logger.get_logging_messages()[1]

    assert first_logging_message == (INFO, f"Action: {given_command}")
    assert second_logging_message == (WARNING, f"Empty config for {given_command}")
