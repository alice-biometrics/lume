from typing import Dict

from meiga import Error


class RequiredEnvError(Error):
    def __init__(self, unmeet_required_env_messages: Dict[str, str]):
        self.unmeet_required_env_messages = unmeet_required_env_messages
