from subprocess import Popen, PIPE
from typing import Dict

from meiga import Result, Error, isSuccess, isFailure

from lume.src.domain.services.interface_executor_service import IExecutorService

# TODO pythonize this function
# It's possible to add a custom "PIPE" handler to the logger and pass that handler to
# Popen's stdout and stderr
from lume.src.domain.services.interface_logger import ILogger, WARNING, ERROR, INFO


def get_and_log_process_std(process, logger):
    """ Capture and log the stdout and stderr of a running process
    This allows process that take a while to finish (i.e. pytest) to avoid waiting for
    process.communicate() and log intermediate outputs.
    """
    output = err = ""
    while True:
        current_output = process.stdout.readline().decode()
        current_err = None
        if current_output:
            logger.debug(current_output)
            output += current_output
        else:
            current_err = process.stderr.readline().decode()
            if current_err:
                logger.warning(current_err)
                err += current_err
        if not current_output and not current_err:
            break
    return output, err


class PopenExecutorService(IExecutorService):
    def __init__(
        self, logger: ILogger, use_communicate=True, raise_runtime_error=False
    ):
        self.logger = logger
        self.use_communicate = use_communicate
        self.raise_runtime_error = raise_runtime_error

    def info(self) -> Dict:
        return {"name": self.__class__.__name__}

    def execute(self, command: str, cwd: str) -> Result[bool, Error]:

        if not cwd:
            cwd = "."

        process = Popen(command, stdout=PIPE, stderr=PIPE, cwd=cwd, shell=True)

        if self.use_communicate:
            output, err = process.communicate()
        else:
            output, err = get_and_log_process_std(process, self.logger)

        if isinstance(output, bytes):
            output = output.decode("utf-8")
        if isinstance(err, bytes):
            err = err.decode("utf-8")
        return_code = process.poll()

        output = output.rstrip()

        if output != "":
            self.logger.log(INFO, f"{output}")

        if return_code == 0:
            if err:
                self.logger.log(WARNING, err)
        else:
            # something weird happened
            if err:
                self.logger.log(ERROR, err)
            # but may have not been written to stderr
            # i.e. flake8 fails with return code 1 but writes to stout
            else:
                self.logger.log(ERROR, output)

            if self.raise_runtime_error:
                raise RuntimeError(
                    "Command '{}' has failed with return_code '{}'".format(
                        command, return_code
                    )
                )
            return isFailure

        return isSuccess
