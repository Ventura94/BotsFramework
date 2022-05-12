"""
Abstract class Strategy, to implement strategy bots.
"""
from abc import ABC, abstractmethod
from BotsFramework.interfaces.iservice import IService
from BotsFramework.interfaces.providers.iposition import IPosition
from BotsFramework.interfaces.providers.isymbol_info import ISymbolInfo
from BotsFramework.interfaces.providers.iaccount_info import IAccountInfo


class Bot(ABC):
    account_info: IAccountInfo = None
    position: IPosition = None
    symbol_info: ISymbolInfo = None

    def __init__(self, service_provider: IService) -> None:
        self.position = service_provider.position
        self.account_info = service_provider.account_info
        self.symbol_info = service_provider.symbol_info

    @staticmethod
    @abstractmethod
    def get_data() -> dict:
        """
        In this method, a dictionary with the clean data necessary
        to establish the strategy is returned.

        :return: Dictionary with the necessary data for the strategy.
        """

    @abstractmethod
    def strategy_bot(self) -> None:
        """
        In this method the strategy is implemented.

        :return: None
        """

    def start(self) -> None:
        """
        This is the method in charge of constantly implementing the strategy,
        it does not need to be overridden, it is only called in the main bot.

        :return: None
        """
        while True:
            self.strategy_bot()
