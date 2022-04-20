"""
Service Interface for adapter provider
"""
from abc import ABC, abstractmethod
from MT5BotsFramework.interfaces.iaccount_info import IAccountInfo
from MT5BotsFramework.interfaces.iposition import IPosition
from MT5BotsFramework.interfaces.isymbol_info import ISymbolInfo


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
