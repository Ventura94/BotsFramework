"""
 MetaTrader5 controller module.
"""
import json
import os
import time

import MetaTrader5
from MetaTrader5 import TradePosition
from setting import STRATEGY_DIR, TYPE_FILLING
from exceptions.MetaTraderError import InitializeError, TypeOrderError


class Controller:
    """
    Controller MetaTrader5 bot class.

    :param strategy_conf_file: String with the name of the strategy configuration file.
    """

    def __init__(self, strategy_conf_file: str) -> None:
        self.conf: dict = self.conf_load_file(strategy_conf_file)
        if not MetaTrader5.initialize():  # pylint: disable=maybe-no-member
            MetaTrader5.shutdown()  # pylint: disable=maybe-no-member
            raise InitializeError("Error launching MetaTrader")

    @staticmethod
    def conf_load_file(strategy_conf_file: str) -> dict:
        """
        Load the bot strategy configuration.

        :param strategy_conf_file: String with the name of the strategy configuration file.
        :return: Dictionary with the content of the strategy configuration.
        """
        conf_path = os.path.join(
            STRATEGY_DIR, strategy_conf_file
        )
        with open(conf_path) as json_file:
            data: dict = json.load(json_file)
            return data

    def prepare_to_open_positions(self, type_order: str) -> dict:
        """
        Method that forms the dictionary with which to open position.

        :param type_order: Type of order to be placed, accepts only "buy" or "sell".
        :raise TypeOrderError: Fired when an unaccepted order type is submitted.
        :return: Dictionary with the configuration of the command to be opened.
        """
        type_order = type_order.lower()
        if type_order == "buy":
            order = MetaTrader5.ORDER_TYPE_BUY
            price = MetaTrader5.symbol_info_tick(  # pylint: disable=maybe-no-member
                self.conf['symbol']
            ).ask
        elif type_order == "sell":
            order = MetaTrader5.ORDER_TYPE_SELL
            price = MetaTrader5.symbol_info_tick(  # pylint: disable=maybe-no-member
                self.conf['symbol']
            ).bid
        else:
            raise TypeOrderError('The type of order sent is not accepted, it must be "buy" or "sell"')
        request: dict = {
            "action": MetaTrader5.TRADE_ACTION_DEAL,
            "symbol": self.conf['symbol'],
            "volume": self.conf['volume'],
            "type": order,
            "price": price,
            "deviation": self.conf['deviation'],
            "magic": self.conf['magic'],
            "comment": self.conf['comment'],
            "type_time": MetaTrader5.ORDER_TIME_GTC,
            "type_filling": TYPE_FILLING,
        }
        return request

    def open_market_positions(self, type_order: str) -> str:
        """

        :param type_order: Type of order to be placed, accepts only "buy" or "sell".
        :return:
        """
        request = self.prepare_to_open_positions(type_order)
        return self.send_to_metatrader(request)

    @staticmethod
    def prepare_to_close_positions(position: TradePosition) -> dict:
        """

        :param position:
        :return:
        """
        symbol: str = position.symbol
        type_order: int = position.type
        ticket: int = position.ticket
        volume: float = position.volume
        if type_order == MetaTrader5.ORDER_TYPE_BUY:
            order_type: int = MetaTrader5.ORDER_TYPE_SELL
            price = MetaTrader5.symbol_info_tick(  # pylint: disable=maybe-no-member
                symbol
            ).bid
        else:
            order_type: int = MetaTrader5.ORDER_TYPE_BUY
            price = MetaTrader5.symbol_info_tick(  # pylint: disable=maybe-no-member
                symbol
            ).ask
        request = {
            "action": MetaTrader5.TRADE_ACTION_DEAL,
            "symbol": symbol,
            "position": ticket,
            "price": price,
            "volume": volume,
            "type": order_type,
        }
        return request

    def close_all_symbol_positions(self) -> str:
        """
        Close all positions of a symbol.
        """
        positions: tuple = MetaTrader5.positions_get(  # pylint: disable=maybe-no-member
            symbol=self.conf['symbol']
        )
        if positions:
            results: list = []
            for position in positions:
                request = self.prepare_to_close_positions(position)
                results.append(self.send_to_metatrader(request))
            return f"Report close order: {results}"

    @staticmethod
    def send_to_metatrader(request: dict) -> str:
        """
        Send order to metatrader.

        :param dict request: Request data to metatrader.
        """
        count: int = 0
        result: str = ""
        while count < 3:
            result = MetaTrader5.order_send(request)  # pylint: disable=maybe-no-member
            if result.retcode == MetaTrader5.TRADE_RETCODE_DONE:
                return "The order was placed successfully."
            count += 1
        return f'Error placing the order. Result: {result}'
