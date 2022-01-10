import pytest
from meiga.assertions import assert_failure, assert_success

from lume.config.config_file_not_found_error import ConfigFileNotFoundError
from lume.src.application.cli.lume import get_config


@pytest.mark.unit
@pytest.mark.parametrize(
    "filename",
    [
        "examples/lume-sample.yml",
        "examples/advanced-lume-sample.yml",
        "examples/lume-required-env-with-env.yml",
        "examples/lume-required-env-without-env.yml",
        "examples/lume-sample-os-command-specific.yml",
    ],
)
def test_load_config_successfully(filename):
    result = get_config(filename)
    assert_success(result)


@pytest.mark.unit
def test_fail_when_config_with_invalid_filename():
    invalid_filename = "lume.invalid.yml"
    result = get_config(invalid_filename)
    assert_failure(result, value_is_instance_of=ConfigFileNotFoundError)
