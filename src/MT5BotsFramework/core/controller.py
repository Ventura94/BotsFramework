"""
 MetaTrader5 controller module.
"""

import decimal
import MetaTrader5
from MT5BotsFramework.status import Status
from MetaTrader5 import TradePosition  # pylint: disable=no-name-in-module


class Controller:
    """
    Controller MetaTrader5 bot class.
    """

    last_ticket = 0

    def __init__(self) -> None:
        if not MetaTrader5.initialize():  # pylint: disable=maybe-no-member
            MetaTrader5.shutdown()  # pylint: disable=maybe-no-member
            raise Warning("Error launching MetaTrader")
        self.status = Status()

    def __prepare_to_open_positions(self) -> dict:
        """
        Method that forms the dictionary with which to open position.
        """
        request = {
            "action": self.status.action,
            "symbol": self.status.symbol,
            "volume": self.status.volume,
            "type": self.status.order_type,
            "price": self.status.price,
            "tp": self.status.tp,
            "sl": self.status.sl,
            "deviation": self.status.deviation,
            "magic": self.status.magic,
            "comment": self.status.comment,
            "type_time": self.status.type_time,
            "type_filling": self.status.type_filling,
        }
        if self.status.tp is None:
            del request['tp']
        if self.status.sl is None:
            del request['sl']
        return request

    def open_market_positions(self) -> str:
        """
        Open a position at market price.
        """
        request = self.__prepare_to_open_positions()
        return self.__send_to_metatrader(request)

    def __prepare_to_close_positions(self, position: TradePosition) -> dict:
        """
        Method that forms the dictionary with which to close position.

        :param position: Position to close
        :return: Dictionary with the configuration of the command to be opened.
        """

        ticket = position.ticket
        volume = position.volume
        self.status.symbol = position.symbol
        self.status.update_to_close_order()
        request = {
            "action": self.status.action,
            "symbol": self.status.symbol,
            "position": ticket,
            "price": self.status.price,
            "volume": volume,
            "type": self.status.order_type,
        }
        return request

    @staticmethod
    def get_position_by_ticket(ticket: int) -> TradePosition:
        position = MetaTrader5.positions_get(  # pylint: disable=maybe-no-member
            ticket=ticket
        )
        if position:
            return position[0]
        return None

    def close_positions_by_ticket(self, ticket: int) -> str:
        """
        Close a position for your ticket.

        :return: Closing result.
        """
        position = self.get_position_by_ticket(ticket)
        if position:
            request = self.__prepare_to_close_positions(position)
            return self.__send_to_metatrader(request)
        return "There are no positions to close"

    def close_all_symbol_positions(self) -> str:
        """
        Close all positions of a symbol.
        """
        positions = MetaTrader5.positions_get(  # pylint: disable=maybe-no-member
            symbol=self.status.symbol
        )
        if positions:
            results = []
            for position in positions:
                request = self.__prepare_to_close_positions(position)
                results.append(self.__send_to_metatrader(request))
            return f"Report close order: {results}"
        return f"There are no {self.status.symbol} positions to close"

    def __send_to_metatrader(self, request: dict) -> str:
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

    # def lot(self) -> float:
    #     """Calculate lot"""
    #     balance = MetaTrader5.account_info().balance  # pylint: disable=maybe-no-member
    #     balance_to_lot = self.conf.get("balance_to_lot", 40)
    #     if balance > balance_to_lot:
    #         result = (balance / balance_to_lot) / 100
    #     else:
    #         result = 0.01
    #     return float(
    #         decimal.Decimal(result).quantize(
    #             decimal.Decimal(".01"), rounding=decimal.ROUND_DOWN
    #         )
    #     )
