"""
 MetaTrader5 controller module.
"""

import decimal
from typing import List, Dict, Union
import MetaTrader5
from MetaTrader5 import (  # pylint: disable=no-name-in-module
    TradePosition,
    OrderSendResult,
)
from MT5BotsFramework.status import Status
from MT5BotsFramework.exceptions.mt5_errors import (
    InitializeException,
    PositionException,
)


class Controller:
    """
    Controller MetaTrader5 bot class.
    """

    def __init__(self) -> None:
        if not MetaTrader5.initialize():  # pylint: disable=maybe-no-member
            MetaTrader5.shutdown()  # pylint: disable=maybe-no-member
            raise InitializeException("Error launching MetaTrader")
        self.status = Status()

    def __prepare_to_open_positions(
            self,
    ) -> Dict[str, Union[str, int, decimal.Decimal]]:
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
            del request["tp"]
        if self.status.sl is None:
            del request["sl"]
        return request

    def open_market_positions(self) -> OrderSendResult:
        """
        Open a position at market price.
        """
        request = self.__prepare_to_open_positions()
        return self.__send_to_metatrader(request)

    @staticmethod
    def get_balance() -> decimal.Decimal:
        """
        Get balance of the account.

        :return: Balance of the account.
        """
        return (
            MetaTrader5.MetaTrader5.account_info().balance  # pylint: disable=maybe-no-member
        )

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
        """
        Get position by ticket.
        :param ticket: Ticket of the position.
        :return: TradePosition object.
        """
        position = MetaTrader5.positions_get(  # pylint: disable=maybe-no-member
            ticket=ticket
        )
        if position:
            return position[0]
        raise PositionException("Position not found")

    def close_positions_by_ticket(self, ticket: int) -> str:
        """
        Close a position for your ticket.

        :return: Closing result.
        """
        position = self.get_position_by_ticket(ticket)
        request = self.__prepare_to_close_positions(position)
        return self.__send_to_metatrader(request)

    def close_all_symbol_positions(self) -> List[OrderSendResult]:
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
            return results
        raise PositionException(f" Not found positions for symbol {self.status.symbol}")

    def get_profit_by_ticket(self, ticket: int) -> decimal.Decimal:
        """
        Get profit by ticket.

        :param ticket: Ticket of the position.
        :return: Profit of the position.
        """
        position = self.get_position_by_ticket(ticket)
        return position.profit

    @staticmethod
    def __send_to_metatrader(
            request: Dict[str, Union[str, int, decimal.Decimal]]
    ) -> OrderSendResult:
        """
        Send order to metatrader.

        :param dict request: Request data to metatrader.
        """
        last_result = None
        for _ in range(3):
            result = MetaTrader5.order_send(request)  # pylint: disable=maybe-no-member
            if result.retcode == MetaTrader5.TRADE_RETCODE_DONE:
                return result
            last_result = result
        return last_result

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
