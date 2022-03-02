"""
This module performs copy trading with telegram messages.
"""

from abc import ABC, abstractmethod
from MT5BotFramework.core.controller import Controller
from MT5BotFramework.exceptions.meta_trader_errors import AuthorizedError


class TelegramCopyProvider(ABC):
    """
    Bot Telegram copy trading.
    """

    def __init__(self):
        self.controller = Controller()
        self.controller.conf = self.conf

    @property
    @abstractmethod
    def conf(self) -> dict:
        """
        Property to load configuration
        """
        ...

    @staticmethod
    @abstractmethod
    def message_to_order(message: str) -> dict:
        """
        Method that cleans the message received from Telegram
        and converts it into a dictionary with the necessary parameters for a command

        :param message: Telegram message
        :return: Dictionary with the necessary parameters for a command
        """

    def send_order(self, message: str) -> str:
        """
        Method in charge of sending the positions to MetaTrader 5.
        Returns a string with the result of the order.
        Receive the direct message from Telagram, this method
        automatically takes care of cleaning it with the message_to_order() method.

        :param str message: Telegram message.
        """
        try:
            order = self.message_to_order(message)
        except ValueError as error:
            return f"{error}"
        except AuthorizedError as error:
            return f"{error}"
        except KeyError as error:
            return f"{error}"
        return self.order(order)

    @abstractmethod
    def order(self, order: dict) -> str:
        """
        This method is to define the logic of the bot.

        :param order: Order dict.
        :return: Order result.
        """
