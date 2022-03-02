"""
Test strategy module
"""

import unittest
from MT5BotFramework.core.strategy import Strategy
import MetaTrader5


class BotTest(Strategy):
    """
    Bot test.
    """

    conf = dict(
        symbol="USDCAD",
        account=5619236,
        volume=0.01,
        deviation=20,
        magic=123456,
        comment="V3N2R4",
        type_filling=MetaTrader5.ORDER_FILLING_FOK,
    )

    @staticmethod
    def get_data() -> dict:
        return {"low": 10.0, "close": 20}

    def strategy_bot(self) -> None:
        pass


class StrategyTest(unittest.TestCase):
    """
    Test Strategy
    """

    def setUp(self):
        self.bot = BotTest()
        self.bot.strategy_bot()

    def test_bot_load_conf(self):
        """
        Check that the strategy configuration file is loaded correctly.
        """
        self.assertEqual(self.bot.controller.conf.get("symbol"), "USDCAD")
        self.assertEqual(self.bot.controller.conf.get("account"), 5619236)
        self.assertEqual(self.bot.controller.conf.get("volume"), 0.01)
        self.assertEqual(self.bot.controller.conf.get("deviation"), 20)
        self.assertEqual(self.bot.controller.conf.get("magic"), 123456)
        self.assertEqual(self.bot.controller.conf.get("comment"), "V3N2R4")


if __name__ == "__main__":
    unittest.main()
