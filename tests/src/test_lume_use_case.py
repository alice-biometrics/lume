import pytest

from lume.src.application.use_cases.lume_use_case import LumeUseCase
from lume.src.domain.services.logger import HIGHLIGHT
from lume.src.infrastructure.services.executor.fake_executor_service import (
    FakeExecutorService,
)
from lume.src.infrastructure.services.killer.fake_killer_service import (
    FakeKillerService,
)
from lume.src.infrastructure.services.logger.fake_logger import FakeLogger
from lume.src.infrastructure.services.setup.fake_setup_service import FakeSetupService
from tests.src.mothers.config_mother import ConfigMother


@pytest.mark.unit
@pytest.mark.parametrize("given_command", ["install", "uninstall", "setup"])
def test_should_repr_as_expected_an_error_with_message(given_command):

    config = ConfigMother.any()
    fake_executor_service = FakeExecutorService()
    fake_detach_executor_service = FakeExecutorService()
    fake_detach_killer_service = FakeKillerService()
    fake_logger = FakeLogger()
    fake_setup_service = FakeSetupService(
        setup_config=config.steps.get("setup"), logger=fake_logger
    )

    lume_use_case = LumeUseCase(
        config=config,
        executor_service=fake_executor_service,
        detach_executor_service=fake_detach_executor_service,
        detach_killer_service=fake_detach_killer_service,
        setup_service=fake_setup_service,
        logger=fake_logger,
    )

    lume_use_case.execute([f"{given_command}"])

    first_logging_message = fake_logger.get_logging_messages()[0]

    assert first_logging_message == (HIGHLIGHT, f"Step: {given_command}")
