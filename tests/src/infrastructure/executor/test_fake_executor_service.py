import pytest

from lume.src.infrastructure.services.executor.fake_executor_service import (
    FakeExecutorService,
)


@pytest.mark.unit
def test_should_execute_a_fake_executor_service_successfully():
    executor = FakeExecutorService()
    executor.execute(command="echo hello", cwd=".")
