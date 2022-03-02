"""
Bot test module.
"""
import unittest
import MetaTrader5
from MT5BotFramework.core.controller import Controller
from MT5BotFramework.exceptions.meta_trader_errors import TypeOrderError


class ControllerTest(unittest.TestCase):
    """
    Test Controller module.
    """

    def setUp(self):

        self.controller = Controller()
        self.controller.conf = dict(
            symbol="USDCAD",
            account=5619236,
            volume=0.01,
            deviation=20,
            magic=123456,
            comment="V3N2R4",
            type_filling=MetaTrader5.ORDER_FILLING_FOK,
        )

    def test_load_config(self):
        """
        Check that the strategy configuration file is loaded correctly.
        """
        self.assertEqual(self.controller.conf.get("symbol"), "USDCAD")
        self.assertEqual(self.controller.conf.get("account"), 5619236)
        self.assertEqual(self.controller.conf.get("volume"), 0.01)
        self.assertEqual(self.controller.conf.get("deviation"), 20)
        self.assertEqual(self.controller.conf.get("magic"), 123456)
        self.assertEqual(self.controller.conf.get("comment"), "V3N2R4")

    def test_prepare_to_open_positions(self):
        """
        Test prepare to open positions.
        """
        buy = self.controller.prepare_to_open_positions("buy")
        self.assertEqual(buy["type"], MetaTrader5.ORDER_TYPE_BUY)
        sell = self.controller.prepare_to_open_positions("sell")
        self.assertEqual(sell["type"], MetaTrader5.ORDER_TYPE_SELL)
        self.assertRaises(
            TypeOrderError,
            self.controller.prepare_to_open_positions,
            "anything but a kind of position",
        )

    def test_open_market_positions(self):
        """
        Test open market positions.
        """
        self.assertEqual(
            self.controller.open_market_positions("buy"), "Request executed"
        )
        self.assertEqual(
            self.controller.open_market_positions("sell"), "Request executed"
        )
        self.assertRaises(
            TypeOrderError,
            self.controller.open_market_positions,
            "anything but a kind of position",
        )

    def test_prepare_to_close_positions(self):
        """
        Test prepare to close positions.
        """
        self.controller.open_market_positions("buy")
        positions = MetaTrader5.positions_get(  # pylint: disable=maybe-no-member
            symbol=self.controller.conf.get("symbol")
        )
        for position in positions:
            result = self.controller.prepare_to_close_positions(position)
            self.assertNotEqual(position.type, result.get("type"))

    def test_close_all_symbol_positions(self):
        """
        Test close all symbol for positions.
        """
        self.controller.open_market_positions("buy")
        self.controller.open_market_positions("buy")
        self.controller.open_market_positions("buy")
        self.assertEqual(
            self.controller.close_all_symbol_positions()[:19], "Report close order:"
        )
        self.assertEqual(
            self.controller.close_all_symbol_positions(),
            f"There are no {self.controller.conf.get('symbol')} positions to close",
        )

    def tearDown(self):
        positions: tuple = MetaTrader5.positions_get(  # pylint: disable=maybe-no-member
            symbol=self.controller.conf.get("symbol")
        )
        if positions:
            self.controller.close_all_symbol_positions()

    if __name__ == "__main__":
        unittest.main()
