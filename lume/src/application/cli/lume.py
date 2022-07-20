import argparse
import os
import platform
import shutil
import sys
import time
import traceback

import yaml
from meiga import Error, Failure, Result, Success, isFailure, isSuccess

from lume import __version__
from lume.config import Config
from lume.config.check_os_list_or_str_item import get_platform
from lume.config.config_file_not_found_error import ConfigFileNotFoundError
from lume.config.config_file_not_valid_error import ConfigFileNotValidError
from lume.config.required_env_error import RequiredEnvError
from lume.src.application.use_cases.use_case_builder import UseCaseBuilder
from lume.src.infrastructure.services.logger.colors import Colors


def has_args(args):
    is_active = False
    for arg in vars(args):
        if arg == "no_strict":
            continue
        is_active = is_active or getattr(args, arg)
    return is_active


def get_config(filename: str = r"lume.yml") -> Result[Config, Error]:
    if not os.path.isfile(filename):
        return Failure(ConfigFileNotFoundError(filename))

    try:
        with open(filename) as file:
            lume_dict = yaml.load(file, Loader=yaml.FullLoader)
            config = Config(lume_dict)
            return Success(config)
    except Exception as e:  # noqa
        message = f"Error loading {filename} file: {repr(e.__class__)} {e} | {traceback.format_exc()}"
        return Failure(ConfigFileNotValidError(message))


def on_config_failure(result: Result, config_file: str):
    print(f"❌  Cannot load lume configuration from: {config_file}")
    print(
        "❌  If you aren't using lume in the same directory as a lume.yml file, please use LUME_CONFIG_FILENAME env var to configure it"
    )
    if isinstance(result.value, ConfigFileNotValidError):
        print(f"❌  {Colors.FAIL}{result.value}{Colors.ENDC}")


def on_execution_failure(result: Result):
    if isinstance(result.value, RequiredEnvError):
        unmeet_required_env_messages = result.value.unmeet_required_env_messages
        for env, description in unmeet_required_env_messages.items():
            print(
                f"❌  {Colors.FAIL}{env}{Colors.ENDC} environment variable is mandatory ➜ {description}"
            )
        print(
            f"❌  Please, review required env variables defined in {Colors.OKGREEN}lume.yml{Colors.ENDC} ({Colors.OKBLUE}required_env{Colors.ENDC})"
        )


def get_parser(config):
    parser = argparse.ArgumentParser(
        prog="lume 🔥",
        description="Lume helps you with your daily dev operations and ease the CI & CD process.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.add_argument(
        "-v",
        "-version",
        "--version",
        action="store_true",
        help="show lume version number.",
    )
    parser.add_argument(
        "-all",
        "--all-commands",
        action="store_true",
        dest="all_commands",
        help="run all commands",
    )
    parser.add_argument(
        "-check", "--check", type=str, help="check if lume command is available or not"
    )
    for command in config.get_commands():
        parser.add_argument(
            f"-{command}",
            f"--{command}",
            action="store_true",
            dest=f"command_{command}",
            help=f"{command}",
        )
    parser.add_argument(
        "--no-strict",
        action="store_true",
        dest="no_strict",
        help="No fails if not exist",
    )
    return parser


def str2bool(value: str) -> bool:
    return value.lower() in [
        "true",
        "1",
        "t",
        "y",
        "yes",
        "yeah",
        "yup",
        "certainly",
        "uh-huh",
    ]


def get_strict_mode(args):
    no_strict_mode = str2bool(os.getenv("LUME_NO_STRICT", "false"))
    if args.no_strict or no_strict_mode:
        return False
    else:
        return True


def check_command_availability(strict_mode, not_known, parser, config_file) -> Result:
    if len(not_known) > 0:
        not_supported_message = f"lume 🔥: Given commands are not supported ({not_known}). Please, check your lume file ({config_file})"

        if not strict_mode:
            print(not_supported_message)
            print(
                "lume 🌈: As you define the '--no-strict' (or use `LUME_NO_STRICT` envvar) option everything is ok and return code is 0"
            )
            return isSuccess
        else:
            parser.print_help()
            print(f"\n{not_supported_message}")
            return isFailure


def check_given_command(given_command: str, config: Config):
    if given_command not in config.get_commands():
        print(f"lume 🔥 => `{given_command}` is not available command ❌ ")
        return 1
    else:
        print(f"lume 🔥 => `{given_command}` is an available command ✅ ")
        return 0


def main():
    start = time.time()
    header = f" 🔥 lume {__version__} ({get_platform()} -- Python {platform.python_version()}) "
    columns = shutil.get_terminal_size().columns
    result = isFailure
    exit_code = 1
    suffix = "(exit code 1)"
    prefix = f"{Colors.FAIL} Failed"

    config_file = os.environ.get("LUME_CONFIG_FILENAME", "lume.yml")
    config = get_config(filename=config_file).unwrap_or_else(
        on_failure=on_config_failure, failure_args=(Result.__id__, config_file)
    )

    if config:
        parser = get_parser(config)
        args, not_known = parser.parse_known_args()
        strict_mode = get_strict_mode(args)
        config.update_strict_mode(strict_mode)
        lume_use_case = UseCaseBuilder.lume(config=config)

        if not has_args(args):
            result = check_command_availability(
                strict_mode, not_known, parser, config_file
            )
        else:
            dict_args = vars(args)

            if args.version:
                print(f"lume 🔥 => {__version__}")
                return 0

            if args.check:
                return check_given_command(args.check, config)

            print(header.center(columns - 10, "="))

            selected_actions = [
                action
                for action, selected in dict_args.items()
                if selected and action != "all_commands"
                if selected and action != "no_strict"
            ]

            if args.all_commands:
                all_steps_actions = [
                    action
                    for action in dict_args.keys()
                    if "command_" in action
                    and action not in ["command_install", "command_uninstall"]
                ]
                selected_actions += all_steps_actions

            selected_actions = [
                action.replace("command_", "") for action in selected_actions
            ]
            result = lume_use_case.execute(steps=selected_actions).handle(
                on_failure=on_execution_failure, failure_args=(Result.__id__)
            )
            lume_use_case.clear_env()

        if result.is_success:
            exit_code = 0
            suffix = "(exit code 0)"
            prefix = f"{Colors.OKGREEN} Succeed"

        if not config.settings["show_exit_code"]:
            suffix = ""
    else:
        suffix = ""

    end = time.time()
    elapsed_time = end - start

    footer = f"{prefix} in {elapsed_time:.2f} seconds {suffix} {Colors.ENDC}".center(
        len(header), "="
    )
    print(footer.center(columns, "="))

    sys.exit(exit_code)
