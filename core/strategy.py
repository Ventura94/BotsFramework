"""
Strategy Module. Contain the abstract class Strategy, to implement strategy bots.
"""

from abc import ABC, abstractmethod
from core.controller import Controller


class Strategy(ABC):
    """
    Abstract class for strategy bot.
    """

    def __init__(self):
        self.controller = Controller(self.conf_file)

    @property
    @abstractmethod
    def conf_file(self) -> str:
        """
        Property to load configuration file
        """
        ...

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
