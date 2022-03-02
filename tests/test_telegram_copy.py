import unittest
from MT5BotFramework.core.telegram_copy import TelegramCopyProvider
import MetaTrader5


class TelegramCopyProviderBot(TelegramCopyProvider):
    """
    Telegram Copy Provider Bot Test
    """

    conf = dict(type_filling=MetaTrader5.ORDER_FILLING_FOK)

    @staticmethod
    def message_to_order(message: str) -> dict:
        pass

    def order(self, order: dict) -> str:
        pass


class TelegramCopyProviderTest(unittest.TestCase):
    """
    Test TelegramCopyProvider
    """

    def setUp(self):
        self.provider = TelegramCopyProviderBot()

    def test_message_to_order(self):
        pass


if __name__ == "__main__":
    unittest.main()
