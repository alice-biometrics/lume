import pytest

from lume.src.application.use_cases.lume_use_case import LumeUseCase
from lume.src.domain.services.logger import GLOBAL
from lume.src.infrastructure.services.executor.fake_executor_service import (
    FakeExecutorService,
)
from lume.src.infrastructure.services.killer.fake_killer_service import (
    FakeKillerService,
)
from lume.src.infrastructure.services.logger.colors import Colors
from lume.src.infrastructure.services.logger.fake_logger import FakeLogger
from lume.src.infrastructure.services.setup.fake_setup_service import FakeSetupService
from tests.src.mothers.config_mother import ConfigMother


def assert_logging_messages(logging_messages: list, with_global_envs: bool):
    first_logging_message = logging_messages[0]
    if with_global_envs:
        assert first_logging_message == (
            GLOBAL,
            f"{Colors.OKGREEN}Set Global Environment Variables{Colors.ENDC}",
        )


@pytest.mark.unit
@pytest.mark.parametrize(
    "config,logging_messages_with_global_envs",
    [(ConfigMother.any(), False), (ConfigMother.with_global_env(), True)],
)
def test_should_repr_as_expected_an_error_with_message(
    config, logging_messages_with_global_envs
):

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

    lume_use_case.execute(config.get_commands())
    assert_logging_messages(
        fake_logger.get_logging_messages(), logging_messages_with_global_envs
    )
