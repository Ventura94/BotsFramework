import unittest
from core.strategy import Strategy


class BotTest(Strategy):
    conf_file: str = "test_strategy_conf.json"

    def get_data(self):
        return {'low': 10.0, 'close': 20}

    def strategy_bot(self):
        data = super(BotTest, self).strategy_bot()


class StrategyTest(unittest.TestCase):

    def setUp(self):
        self.bot = BotTest()
        self.bot.strategy_bot()

    def test_bot_load_conf(self):
        """
        Check that the strategy configuration file is loaded correctly.
        """
        self.assertEqual(self.bot.controller.conf.get('symbol'), "USDCAD")
        self.assertEqual(self.bot.controller.conf.get('account'), 5619236)
        self.assertEqual(self.bot.controller.conf.get('volume'), 0.01)
        self.assertEqual(self.bot.controller.conf.get('deviation'), 20)
        self.assertEqual(self.bot.controller.conf.get('magic'), 123456)
        self.assertEqual(self.bot.controller.conf.get('comment'), "V3N2R4")


if __name__ == '__main__':
    unittest.main()
