from abc import ABC, abstractmethod


class RegistryFromRequest(ABC):
    """Interface to register new items"""

    @abstractmethod
    def request(self):
        """Request new items"""
        pass

    @abstractmethod
    def filter_new(self):
        """Filter the items which are not yed in db"""
        pass
