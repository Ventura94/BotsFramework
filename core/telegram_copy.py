from abc import ABC, abstractmethod
from .controller import Controller


class TelegramCopy(ABC):

    def __init__(self):
        self.controller = Controller()

    @staticmethod
    @abstractmethod
    def message_to_order(message: str) -> dict:
        """
        Method that cleans the message received from Telegram
        and converts it into a dictionary with the necessary parameters for a command

        :param message: Telegram message
        :return: Dictionary with the necessary parameters for a command
        """
        pass

    @abstractmethod
    def send_order(self, message: str) -> str:
        """
        Method in charge of sending the positions to MetaTrader 5.
        Returns a string with the result of the order.
        Receive the direct message from Telagram, this method
        automatically takes care of cleaning it with the message_to_order() method.

        :param str message: Telegram message.
        """
        pass
