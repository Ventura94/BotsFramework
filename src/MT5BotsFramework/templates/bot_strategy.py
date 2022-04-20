"""
Strategy Module. Contain the abstract class Strategy, to implement strategy bots.
"""
from typing import Literal
from abc import ABC, abstractmethod
from MT5BotsFramework.interfaces.iservice import IService
from MT5BotsFramework.providers.adapter import AdapterProvider


class BotStrategy(ABC):
    """
    Abstract class for strategy bot.
    """

    account_info: IAccountInfo = None
    position: IPosition = None
    symbol_info: ISymbolInfo = None

    def __init__(self, provider: IService) -> None:
        service = provider()
        self.position = service.position
        self.account_info = service.account_info
        self.symbol_info = service.symbol_info

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
