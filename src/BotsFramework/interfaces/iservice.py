"""
Service Interface for adapter provider
"""
from abc import ABC, abstractmethod
from BotsFramework.interfaces.providers.iaccount_info import IAccountInfo
from BotsFramework.interfaces.providers.iposition import IPosition
from BotsFramework.interfaces.providers.isymbol_info import ISymbolInfo


class IService(ABC):
    """
    Service Interface
    """

    @property
    @abstractmethod
    def account_info(self) -> IAccountInfo:
        """
        Account Info
        :return: Account info object.
        """

    @property
    @abstractmethod
    def position(self) -> IPosition:
        """Positions"""

    @property
    @abstractmethod
    def symbol_info(self) -> ISymbolInfo:
        """
        Symbol Info
        """
