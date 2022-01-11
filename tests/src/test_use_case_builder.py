import os
import shutil

import pytest
from meiga.assertions import assert_failure, assert_success

from lume.config.required_env_error import RequiredEnvError
from lume.src.application.cli.lume import get_config
from lume.src.application.use_cases.use_case_builder import UseCaseBuilder


@pytest.mark.unit
@pytest.mark.parametrize(
    "filename",
    [
        "examples/lume-sample.yml",
        "examples/lume-sample-setup-without-auth.yml",
        "examples/lume-required-env-with-env.yml",
        "examples/lume-sample-os-command-specific.yml",
    ],
)
def test_build_and_execute_lume_use_case_successfully(filename):
    config = get_config(filename).unwrap_or_throw()
    use_case = UseCaseBuilder.lume(config)
    result = use_case.execute(config.get_commands())
    assert_success(result)
    shutil.rmtree("deps", ignore_errors=True, onerror=None)


@pytest.mark.unit
def test_fail_executing_lume_use_case_when_required_env_is_not_given():
    config = get_config("examples/lume-required-env-without-env.yml").unwrap_or_throw()
    use_case = UseCaseBuilder.lume(config)
    result = use_case.execute(["install"])
    assert_failure(result, value_is_instance_of=RequiredEnvError)


@pytest.mark.unit
@pytest.mark.skipif(
    "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ,
    reason="GOOGLE_APPLICATION_CREDENTIALS must be defined",
)
def test_build_and_execute_lume_use_case_when_requires_gcs_auth_successfully():
    config = get_config("examples/lume-sample-setup-with-auth.yml").unwrap_or_throw()
    use_case = UseCaseBuilder.lume(config)
    result = use_case.execute(config.get_commands())
    assert_success(result)
    shutil.rmtree("deps", ignore_errors=True, onerror=None)
