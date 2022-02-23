"""
Bot test module.
"""
import unittest
import MetaTrader5
from core.controller import Controller
from exceptions.meta_trader_errors import TypeOrderError
from setting import TYPE_FILLING


class ControllerTest(unittest.TestCase):

    def setUp(self):
        strategy_conf_file = 'test_strategy_conf.json'
        self.controller = Controller(strategy_conf_file=strategy_conf_file)
        self.controller_not_config = Controller()
        self.dict_conf = dict(
            symbol="USDCAD",
            account=5619236,
            volume=0.01,
            deviation=20,
            magic=123456,
            comment="V3N2R4",
        )

    def test_load_config(self):
        """
        Check that the strategy configuration file is loaded correctly.
        """
        self.assertEqual(self.controller.conf.get('symbol'), "USDCAD")
        self.assertEqual(self.controller.conf.get('account'), 5619236)
        self.assertEqual(self.controller.conf.get('volume'), 0.01)
        self.assertEqual(self.controller.conf.get('deviation'), 20)
        self.assertEqual(self.controller.conf.get('magic'), 123456)
        self.assertEqual(self.controller.conf.get('comment'), "V3N2R4")

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

    def test_open_market_positions_not_conf(self):
        self.assertEqual(
            self.controller_not_config.open_market_positions(type_order="buy", **self.dict_conf),
            "Request executed"
        )
        self.assertEqual(
            self.controller_not_config.open_market_positions(type_order="sell", **self.dict_conf),
            "Request executed"
        )

    def test_prepare_to_close_positions(self):
        self.controller.open_market_positions("buy")
        positions: tuple = MetaTrader5.positions_get(  # pylint: disable=maybe-no-member
            symbol=self.controller.conf.get('symbol')
        )
        for position in positions:
            result = self.controller.prepare_to_close_positions(position)
            self.assertNotEqual(
                position.type,
                result.get('type')
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
            f"There are no {self.controller.conf.get('symbol')} positions to close"
        )

    def tearDown(self):
        positions: tuple = MetaTrader5.positions_get(  # pylint: disable=maybe-no-member
            symbol=self.controller.conf.get('symbol')
        )
        if positions:
            self.controller.close_all_symbol_positions()

    if __name__ == '__main__':
        unittest.main()
