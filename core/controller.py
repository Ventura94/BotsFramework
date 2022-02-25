"""
 MetaTrader5 controller module.
"""
import json
import os

import MetaTrader5
from MetaTrader5 import TradePosition  # pylint: disable=no-name-in-module
from MT5BotFramework.setting import STRATEGY_DIR, TYPE_FILLING
from MT5BotFramework.exceptions.meta_trader_errors import InitializeError, TypeOrderError


class Controller:
    """
    Controller MetaTrader5 bot class.

    :param strategy_conf_file: String with the name of the strategy configuration file.
    """

    last_ticket = 0

    def __init__(self, strategy_conf_file: str = None) -> None:
        self.conf = self.conf_load_file(strategy_conf_file)
        if not MetaTrader5.initialize():  # pylint: disable=maybe-no-member
            MetaTrader5.shutdown()  # pylint: disable=maybe-no-member
            raise InitializeError("Error launching MetaTrader")

    @staticmethod
    def conf_load_file(strategy_conf_file: str = None) -> dict:
        """
        Load the bot strategy configuration.

        :param strategy_conf_file: String with the name of the strategy configuration file.
        :return: Dictionary with the content of the strategy configuration.
        """
        if not strategy_conf_file:
            return {}
        conf_path = os.path.join(STRATEGY_DIR, strategy_conf_file)
        with open(conf_path, encoding="utf8") as json_file:
            data = json.load(json_file)
            return data

    def prepare_to_open_positions(self, type_order: str) -> dict:
        """
        Method that forms the dictionary with which to open position.

        :param type_order: Type of order to be placed, accepts only "buy" or "sell".
        :raise TypeOrderError: Fired when an unaccepted order type is submitted.
        :return: Dictionary with the configuration of the command to be opened.
        """

        if type_order.lower() == "buy":
            order = MetaTrader5.ORDER_TYPE_BUY
            price = MetaTrader5.symbol_info_tick(  # pylint: disable=maybe-no-member
                self.conf.get("symbol")
            ).ask
        elif type_order.lower() == "sell":
            order = MetaTrader5.ORDER_TYPE_SELL
            price = MetaTrader5.symbol_info_tick(  # pylint: disable=maybe-no-member
                self.conf.get("symbol")
            ).bid
        else:
            raise TypeOrderError(
                'The type of order sent is not accepted, it must be "buy" or "sell"'
            )
        request = {
            "action": MetaTrader5.TRADE_ACTION_DEAL,
            "symbol": self.conf.get("symbol"),
            "volume": self.conf.get("volume", 0.01),
            "type": order,
            "price": price,
            "deviation": self.conf.get("deviation", 20),
            "magic": self.conf.get("magic", 0),
            "comment": self.conf.get("comment", "V3N2R4"),
            "type_time": MetaTrader5.ORDER_TIME_GTC,
            "type_filling": TYPE_FILLING,
        }
        return request

    def open_market_positions(self, type_order: str, **kwargs) -> str:
        """
        Open a position at market price.

        :param type_order: Type of order to be placed, accepts only "buy" or "sell".
        :param kwargs: Configuration this order.
        :return: String with the result of sending the order to MetaTrader5.
        """

        self.conf.update(kwargs)
        request = self.prepare_to_open_positions(type_order)
        return self.send_to_metatrader(request)

    @staticmethod
    def prepare_to_close_positions(position: TradePosition) -> dict:
        """
        Method that forms the dictionary with which to close position.

        :param position: Position to close
        :return: Dictionary with the configuration of the command to be opened.
        """
        symbol = position.symbol
        type_order = position.type
        ticket = position.ticket
        volume = position.volume
        if type_order == MetaTrader5.ORDER_TYPE_BUY:
            order_type = MetaTrader5.ORDER_TYPE_SELL
            price = MetaTrader5.symbol_info_tick(  # pylint: disable=maybe-no-member
                symbol
            ).bid
        else:
            order_type = MetaTrader5.ORDER_TYPE_BUY
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

    def close_positions_by_ticket(self, ticket: int) -> str:
        """
        Close a position for your ticket.

        :return: Closing result.
        """
        position = MetaTrader5.positions_get(  # pylint: disable=maybe-no-member
            ticket=ticket
        )
        if position:
            request = self.prepare_to_close_positions(position)
            return self.send_to_metatrader(request)
        return "There are no positions to close"

    def close_all_symbol_positions(self, **kwargs) -> str:
        """
        Close all positions of a symbol.
        """
        self.conf.update(kwargs)
        positions = MetaTrader5.positions_get(  # pylint: disable=maybe-no-member
            symbol=self.conf.get("symbol")
        )
        if positions:
            results = []
            for position in positions:
                request = self.prepare_to_close_positions(position)
                results.append(self.send_to_metatrader(request))
            return f"Report close order: {results}"
        return f"There are no {self.conf.get('symbol')} positions to close"

    def send_to_metatrader(self, request: dict) -> str:
        """
        Send order to metatrader.

        :param dict request: Request data to metatrader.
        """
        count = 0
        result = None
        while count < 3:
            result = MetaTrader5.order_send(request)  # pylint: disable=maybe-no-member
            if result.retcode == MetaTrader5.TRADE_RETCODE_DONE:
                self.last_ticket = result.order
                return result.comment
            count += 1
        return result.comment
