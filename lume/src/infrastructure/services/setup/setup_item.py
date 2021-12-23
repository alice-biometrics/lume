from abc import ABCMeta, abstractmethod

from meiga import Result

from lume.config import DependencyConfig
from lume.src.domain.services.logger import Logger


class SetupItem(object):
    __metaclass__ = ABCMeta
    base_path = None

    def __init__(self, base_path: str):
        self.base_path = base_path

    @abstractmethod
    def run(
        self, name: str, dependency_config: DependencyConfig, logger: Logger
    ) -> Result:
        raise NotImplementedError
