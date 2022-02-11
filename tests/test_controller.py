"""
Bot test module.
"""
import unittest
import MetaTrader5
from core.controller import Controller
from exceptions.meta_trader_errors import TypeOrderError
from setting import TYPE_FILLING


class ControllerTest(unittest.TestCase):
    """
    Controller test class.
    """

    def setUp(self):
        strategy_conf_file = 'test_strategy_conf.json'
        self.controller = Controller(strategy_conf_file=strategy_conf_file)

    def test_load_config(self):
        """
        Check that the strategy configuration file is loaded correctly.
        """

        self.assertEqual(self.controller.conf['symbol'], "USDCAD")
        self.assertEqual(self.controller.conf['account'], 5619236)
        self.assertEqual(self.controller.conf['volume'], 0.01)
        self.assertEqual(self.controller.conf['deviation'], 20)
        self.assertEqual(self.controller.conf['magic'], 123456)
        self.assertEqual(self.controller.conf['comment'], "V3N2R4")

    def test_prepare_to_open_positions(self):
        buy = self.controller.prepare_to_open_positions("buy")
        self.assertEqual(
            buy['type'],
            MetaTrader5.ORDER_TYPE_BUY
        )
        sell = self.controller.prepare_to_open_positions("sell")
        self.assertEqual(
            sell['type'],
            MetaTrader5.ORDER_TYPE_SELL
        )
        self.assertRaises(
            TypeOrderError,
            self.controller.prepare_to_open_positions,
            "anything but a kind of position",
        )

    def test_open_market_positions(self):
        self.assertEqual(
            self.controller.open_market_positions("buy"),
            "Request executed"
        )
        self.assertEqual(
            self.controller.open_market_positions("sell"),
            "Request executed"
        )
        self.assertRaises(
            TypeOrderError,
            self.controller.open_market_positions,
            "anything but a kind of position",
        )

    def test_prepare_to_close_positions(self):
        self.controller.open_market_positions("buy")
        positions: tuple = MetaTrader5.positions_get(  # pylint: disable=maybe-no-member
            symbol=self.controller.conf['symbol']
        )
        for position in positions:
            result = self.controller.prepare_to_close_positions(position)
            self.assertNotEqual(
                position.type,
                result['type']
            )

    def test_close_all_symbol_positions(self):
        self.controller.open_market_positions("buy")
        self.controller.open_market_positions("buy")
        self.controller.open_market_positions("buy")
        self.assertEqual(
            self.controller.close_all_symbol_positions()[:19],
            "Report close order:"
        )
        self.assertEqual(
            self.controller.close_all_symbol_positions(),
            f"There are no {self.controller.conf['symbol']} positions to close"
        )

    def tearDown(self):
        positions: tuple = MetaTrader5.positions_get(  # pylint: disable=maybe-no-member
            symbol=self.controller.conf['symbol']
        )
        if positions:
            self.controller.close_all_symbol_positions()


if __name__ == '__main__':
    unittest.main()
