from abc import ABC, abstractmethod


class IService(ABC):
    @property
    @abstractmethod
    def account_info(self):
        ...

    @property
    @abstractmethod
    def position(self):
        ...

    @property
    @abstractmethod
    def symbol_info(self):
        ...
