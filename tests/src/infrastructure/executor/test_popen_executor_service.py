import pytest

from lume.src.infrastructure.services.executor.popen_executor_service import (
    PopenExecutorService,
)
from lume.src.infrastructure.services.logger.fake_logger import FakeLogger


@pytest.mark.unit
def test_should_execute_a_popen_executor_service_successfully():

    fake_logger = FakeLogger()
    executor = PopenExecutorService(fake_logger)
    executor.execute(command="echo hello", cwd=".")
