from lume.src.application.cli.lume import get_config


class ConfigMother:
    @staticmethod
    def any():
        return get_config("examples/lume-any.yml").unwrap_or_throw()
