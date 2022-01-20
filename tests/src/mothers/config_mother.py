from lume.src.application.cli.lume import get_config


class ConfigMother:
    @staticmethod
    def any():
        return get_config("examples/lume-any.yml").unwrap_or_throw()

    @staticmethod
    def with_global_env():
        return get_config("examples/lume-sample.yml").unwrap_or_throw()
