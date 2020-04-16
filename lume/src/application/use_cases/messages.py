from lume.src.infrastructure.services.logger.colors import Colors


def get_colored_command_message(command, cwd, step, prefix=None):
    message = (
        f"{Colors.OKBLUE}{step}{Colors.ENDC} {Colors.BOLD}>> {command}{Colors.ENDC}"
        if not cwd
        else f"{Colors.OKBLUE}{step}{Colors.ENDC} {Colors.HEADER}[cwd={cwd}]{Colors.ENDC} {Colors.BOLD}>> {command}{Colors.ENDC}"
    )
    if prefix:
        message = f"{Colors.WARNING}{prefix}{Colors.ENDC} | {message}"
    return message
