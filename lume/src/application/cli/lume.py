import argparse
import os
import sys
import traceback

import yaml
from meiga import Result, Error, Success, Failure
from yaml.parser import ParserError

from lume import __version__
from lume.config import Config
from lume.config.config_file_not_found_error import ConfigFileNotFoundError
from lume.config.config_file_not_valid_error import ConfigFileNotValidError
from lume.src.application.use_cases.use_case_builder import UseCaseBuilder


def has_args(args):
    is_active = False
    for arg in vars(args):
        is_active = is_active or getattr(args, arg)
    return is_active


def get_config(filename: str = r"lume.yml") -> Result[Config, Error]:
    if not os.path.isfile(filename):
        return Failure(ConfigFileNotFoundError(filename))

    try:
        with open(filename) as file:
            lume_dict = yaml.load(file, Loader=yaml.FullLoader)
            config = Config.from_dict(lume_dict)
            return Success(config)
    except ParserError as e:
        message = f"Error loading {filename} file: {repr(e.__class__)} {e} | {traceback.format_exc()}"
        return Failure(ConfigFileNotValidError(message))


def on_failure(config_file):
    print(f"Cannot load lume configuration from: {config_file}")
    print(
        f"If you don't are using lume in the same directory as a lume.yml file, please use LUME_CONFIG_FILENAME env var to configure it"
    )


def main():
    config_file = os.environ.get("LUME_CONFIG_FILENAME", "lume.yml")
    config = get_config(filename=config_file).unwrap_or_else(
        on_failure=on_failure, failure_args=(config_file,)
    )

    if config:
        lume_use_case = UseCaseBuilder.lume(config=config)

        parser = argparse.ArgumentParser(
            prog="lume 🔥",
            description="Lume helps you with your daily dev operations and ease the CI & CD process.",
            formatter_class=argparse.RawDescriptionHelpFormatter,
        )

        parser.add_argument(
            "-v", "--version", action="store_true", help="show lume version number."
        )
        parser.add_argument(
            "-all",
            "--all-commands",
            action="store_true",
            dest="all_commands",
            help="run all commands",
        )

        for command in config.get_commands():
            parser.add_argument(
                f"-{command}",
                f"--{command}",
                action="store_true",
                dest=f"command_{command}",
                help=f"{command}",
            )

        args = parser.parse_args()

        if not has_args(args):
            parser.print_help()
        else:
            dict_args = vars(args)

            if args.version:
                print(f"lume 🔥 => {__version__}")
                return

            selected_actions = [
                action
                for action, selected in dict_args.items()
                if selected and action != "all_commands"
            ]
            if args.all_commands:
                all_steps_actions = [
                    action for action in dict_args.keys() if "command_" in action
                ]
                selected_actions += all_steps_actions

            selected_actions = [
                action.replace("command_", "") for action in selected_actions
            ]

            lume_use_case.execute(actions=selected_actions)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
