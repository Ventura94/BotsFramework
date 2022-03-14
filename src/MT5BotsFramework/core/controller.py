"""
 MetaTrader5 controller module.
"""

import decimal
import MetaTrader5
from MetaTrader5 import TradePosition  # pylint: disable=no-name-in-module

from MT5BotFramework.settings import Settings


class Controller:
    """
    Controller MetaTrader5 bot class.
    :param strategy_conf_file: String with the name of the strategy configuration file.
    """

    last_ticket = 0

    def __init__(self) -> None:
        if not MetaTrader5.initialize():  # pylint: disable=maybe-no-member
            MetaTrader5.shutdown()  # pylint: disable=maybe-no-member
            raise Warning("Error launching MetaTrader")
        self.settings = Settings()

    def prepare_to_open_positions(self) -> dict:
        """
        Method that forms the dictionary with which to open position.
        """
        self.settings.open_order_redefine()
        request = {
            "action": self.settings.action,
            "symbol": self.settings.symbol,
            "volume": self.settings.volume,
            "type": self.settings.order_type,
            "price": self.settings.price,
            "deviation": self.settings.deviation,
            "magic": self.settings.magic,
            "comment": self.settings.comment,
            "type_time": self.settings.type_time,
            "type_filling": self.settings.type_filling,
        }
        return request

    def open_market_positions(self) -> str:
        """
        Open a position at market price.
        """

        request = self.prepare_to_open_positions()
        return self.send_to_metatrader(request)

    def prepare_to_close_positions(self, position: TradePosition) -> dict:
        """
        Method that forms the dictionary with which to close position.

        :param position: Position to close
        :return: Dictionary with the configuration of the command to be opened.
        """

        ticket = position.ticket
        volume = position.volume
        self.settings.symbol = position.symbol
        self.settings.close_order_redefine(order_type=position.type)
        request = {
            "action": self.settings.action,
            "symbol": self.settings.symbol,
            "position": ticket,
            "price": self.settings.price,
            "volume": volume,
            "type": self.settings.order_type,
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

    def close_all_symbol_positions(self) -> str:
        """
        Close all positions of a symbol.
        """
        positions = MetaTrader5.positions_get(  # pylint: disable=maybe-no-member
            symbol=self.settings.symbol
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

    def lot(self) -> float:
        """Calculate lot"""
        balance = MetaTrader5.account_info().balance  # pylint: disable=maybe-no-member
        balance_to_lot = self.conf.get("balance_to_lot", 40)
        if balance > balance_to_lot:
            result = (balance / balance_to_lot) / 100
        else:
            result = 0.01
        return float(
            decimal.Decimal(result).quantize(
                decimal.Decimal(".01"), rounding=decimal.ROUND_DOWN
            )
        )
