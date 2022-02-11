"""
Bot test module.
"""
import unittest
import MetaTrader5
from core.controller import Controller
from exceptions.MetaTraderError import TypeOrderError
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
        request: dict = {
            "action": MetaTrader5.TRADE_ACTION_DEAL,
            "symbol": self.controller.conf['symbol'],
            "volume": self.controller.conf['volume'],
            "deviation": self.controller.conf['deviation'],
            "magic": self.controller.conf['magic'],
            "comment": self.controller.conf['comment'],
            "type_time": MetaTrader5.ORDER_TIME_GTC,
            "type_filling": TYPE_FILLING,
        }
        buy = self.controller.prepare_to_open_positions("buy")
        request.update({"type": MetaTrader5.ORDER_TYPE_BUY, })
        self.assertEqual(
            buy['action'],
            request['action']
        )
        self.assertEqual(
            buy['symbol'],
            request['symbol']
        )
        self.assertEqual(
            buy['volume'],
            request['volume']
        )
        self.assertEqual(
            buy['type'],
            request['type']
        )
        self.assertEqual(
            buy['deviation'],
            request['deviation']
        )
        self.assertEqual(
            buy['magic'],
            request['magic']
        )
        self.assertEqual(
            buy['comment'],
            request['comment']
        )
        self.assertEqual(
            buy['type_time'],
            request['type_time']
        )
        self.assertEqual(
            buy['type_filling'],
            request['type_filling']
        )
        sell = self.controller.prepare_to_open_positions("sell")
        request.update({"type": MetaTrader5.ORDER_TYPE_SELL, })
        self.assertEqual(
            sell['action'],
            request['action']
        )
        self.assertEqual(
            sell['symbol'],
            request['symbol']
        )
        self.assertEqual(
            sell['volume'],
            request['volume']
        )
        self.assertEqual(
            sell['type'],
            request['type']
        )
        self.assertEqual(
            sell['deviation'],
            request['deviation']
        )
        self.assertEqual(
            sell['magic'],
            request['magic']
        )
        self.assertEqual(
            sell['comment'],
            request['comment']
        )
        self.assertEqual(
            sell['type_time'],
            request['type_time']
        )
        self.assertEqual(
            sell['type_filling'],
            request['type_filling']
        )
        self.assertRaises(
            TypeOrderError,
            self.controller.prepare_to_open_positions,
            "anything but a kind of position",
        )

    def test_open_market_positions(self):
        self.assertEqual(
            self.controller.open_market_positions("buy"),
            "The order was placed successfully."
        )
        self.assertEqual(
            self.controller.open_market_positions("sell"),
            "The order was placed successfully."
        )
        self.assertRaises(
            TypeOrderError,
            self.controller.open_market_positions,
            "anything but a kind of position",
        )

    def test_prepare_to_close_positions(self):
        request = {
            "action": MetaTrader5.TRADE_ACTION_DEAL,
            "symbol": self.controller.conf['symbol'],
            "volume": self.controller.conf['volume'],
        }
        self.controller.open_market_positions("buy")
        positions: tuple = MetaTrader5.positions_get(  # pylint: disable=maybe-no-member
            symbol=self.controller.conf['symbol']
        )
        for position in positions:
            result = self.controller.prepare_to_close_positions(position)
            self.assertEqual(
                result['volume'],
                request['volume']
            )
            self.assertEqual(
                result['symbol'],
                request['symbol']
            )
            self.assertEqual(
                result['action'],
                request['action']
            )

    def test_close_all_symbol_positions(self):
        self.controller.open_market_positions("buy")
        self.controller.open_market_positions("buy")
        self.controller.open_market_positions("buy")
        self.assertEqual(
            self.controller.close_all_symbol_positions()[:19],
            "Report close order:"
        )

    def tearDown(self):
        positions: tuple = MetaTrader5.positions_get(  # pylint: disable=maybe-no-member
            symbol=self.controller.conf['symbol']
        )
        if positions:
            self.controller.close_all_symbol_positions()


if __name__ == '__main__':
    unittest.main()
