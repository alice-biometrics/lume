import pytest

from lume.src.application.cli.lume import get_config
from lume.src.application.use_cases.use_case_builder import UseCaseBuilder


@pytest.mark.unit
def test_build_use_case_lume_successfully():
    config = get_config("examples/lume-sample.yml").unwrap_or_throw()
    UseCaseBuilder.lume(config)
