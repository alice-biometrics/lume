from meiga import Error


class CrendentialsEnvError(Error):
    def __init__(self, env_name):
        self.message = f"Environment variable ({env_name}) is not defined properly"


class BadZipFileError(Error):
    def __init__(self, resource_name):
        self.message = (
            f"Error decompressing ({resource_name}). Please ensure the url exists"
        )


class BlobNotFoundError(Error):
    def __init__(self, url):
        self.message = f"Blob not found ({url})"


class ItemTypeNotSupportedError(Error):
    def __init__(self, current_type, supported_types):
        self.message = (
            f"Item type ({current_type}) is not supported. Try with ({supported_types})"
        )
