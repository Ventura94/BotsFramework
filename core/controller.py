"""
 MetaTrader5 controller module.
"""
import json
import os

import MetaTrader5
from MetaTrader5 import TradePosition  # pylint: disable=no-name-in-module
from MT5BotFramework.exceptions.meta_trader_errors import (
    TypeOrderError,
    InitializeError,
)
import decimal


class Controller:
    """
    Controller MetaTrader5 bot class.

    :param strategy_conf_file: String with the name of the strategy configuration file.
    """

    last_ticket = 0
    conf = {}

    def __init__(self) -> None:
        if not MetaTrader5.initialize():  # pylint: disable=maybe-no-member
            MetaTrader5.shutdown()  # pylint: disable=maybe-no-member
            raise InitializeError("Error launching MetaTrader")

    def prepare_to_open_positions(self, type_order: str) -> dict:
        """
        Method that forms the dictionary with which to open position.

        :param type_order: Type of order to be placed, accepts only "buy" or "sell".
        :raise TypeOrderError: Fired when an unaccepted order type is submitted.
        :return: Dictionary with the configuration of the command to be opened.
        """
        if self.conf.get("custom_lot", False):
            self.conf["volume"] = self.lot()

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
            "type_filling": self.conf.get(
                "type_filling", MetaTrader5.ORDER_FILLING_RETURN
            ),
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
        positions = MetaTrader5.positions_get(  # pylint: disable=maybe-no-member
            ticket=ticket
        )
        if positions:
            for position in positions:
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

    @staticmethod
    def lot() -> float:
        balance = MetaTrader5.account_info().balance
        if balance > 40:
            result = (balance / 40) / 100
        else:
            result = 0.01
        return float(
            decimal.Decimal(result).quantize(
                decimal.Decimal(".01"), rounding=decimal.ROUND_DOWN
            )
        )
