import pytest

from lume.src.application.use_cases.messages import get_colored_command_message


@pytest.mark.unit
@pytest.mark.parametrize(
    "prefix",
    [
        "my_prefix",
        None,
    ],
)
def test_load_config_successfully(prefix):
    message = get_colored_command_message(
        command="my-command", cwd="my-cwd", step="my-step", prefix=prefix
    )
    assert isinstance(message, str)
