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
from MT5BotsFramework.exceptions.mt5_errors import PositionException, InitializeException


class Controller:
    """
    Controller MetaTrader5 bot class.
    """

    def __init__(self, bot_id: int) -> None:
        if not MetaTrader5.initialize(  # pylint: disable=maybe-no-member
                login=Status().account,
                password=Status().password,
                server=Status().server,
        ):
            MetaTrader5.shutdown()  # pylint: disable=maybe-no-member
            raise InitializeException(MetaTrader5.last_error())
        self.request_config = Status().register_request_config(bot_id)

    def __prepare_to_open_positions(
            self,
    ) -> Dict[str, Union[str, int, decimal.Decimal]]:
        """
        Method that forms the dictionary with which to open position.
        """
        request = {
            "action": self.request_config.action,
            "symbol": self.request_config.symbol,
            "volume": self.request_config.volume,
            "type": self.request_config.order_type,
            "price": self.request_config.price,
            "tp": self.request_config.tp,
            "sl": self.request_config.sl,
            "deviation": self.request_config.deviation,
            "magic": self.request_config.magic,
            "comment": self.request_config.comment,
            "type_time": Status().type_time,
            "type_filling": Status().type_filling,
        }
        if request.get("tp") is None:
            del request["tp"]
        if request.get("sl") is None:
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
        symbol = position.symbol
        if position.type == MetaTrader5.ORDER_TYPE_BUY:
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
            "action": self.request_config.action,
            "symbol": symbol,
            "position": ticket,
            "price": price,
            "volume": volume,
            "type": order_type,
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
            symbol=self.request_config.symbol
        )
        if positions:
            results = []
            for position in positions:
                request = self.__prepare_to_close_positions(position)
                results.append(self.__send_to_metatrader(request))
            return results
        raise PositionException(f" Not found positions for symbol {self.request_config.symbol}")

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
        raise ValueError(f"Error {last_result.comment}")

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
