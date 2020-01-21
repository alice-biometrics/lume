from meiga import Error


class ConfigFileNotFoundError(Error):
    def __init__(self, filename):
        self.message = f"Lume config file does not exist ({filename})"
