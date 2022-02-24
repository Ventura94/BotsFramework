from abc import ABC, abstractmethod
from core.controller import Controller


class Strategy(ABC):

    def __init__(self):
        self.controller = Controller(self.conf_file)

    @property
    @abstractmethod
    def conf_file(self) -> str:
        ...

    @abstractmethod
    def get_data(self) -> dict:
        """
        In this method, a dictionary with the clean data necessary to establish the strategy is returned.

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
        :return:
        """
        while True:
            self.strategy_bot()
