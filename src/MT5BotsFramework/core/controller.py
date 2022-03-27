"""
 MetaTrader5 controller module.
"""

import decimal
from typing import List, Dict, Union, Literal
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

    action = MetaTrader5.TRADE_ACTION_DEAL
    order_type = None
    symbol = None
    volume = 0.01
    sl = None
    tp = None
    deviation = 20
    magic = 0
    comment = "V3N2R4"

    def __init__(self) -> None:
        if not MetaTrader5.initialize(  # pylint: disable=maybe-no-member
                login=Status().account,
                password=Status().password,
                server=Status().server,
        ):
            MetaTrader5.shutdown()  # pylint: disable=maybe-no-member
            raise InitializeException(MetaTrader5.last_error())

    def order_type_define(self, order_type: Literal["buy", "sell"]) -> None:
        """
        Define type order.
        :param order_type: Buy or Sell
        :return: None
        """
        order_type = order_type.lower()
        if order_type == "buy":
            self.order_type = MetaTrader5.ORDER_TYPE_BUY
        elif order_type == "sell":
            self.order_type = MetaTrader5.ORDER_TYPE_SELL
        else:
            raise ValueError(
                'The type of order sent is not accepted, it must be "buy" or "sell"'
            )

    def get_buy_price(self):
        return MetaTrader5.symbol_info_tick(  # pylint: disable=maybe-no-member
            self.symbol
        ).ask

    def get_sell_price(self):
        return MetaTrader5.symbol_info_tick(  # pylint: disable=maybe-no-member
            self.symbol
        ).bid

    def __prepare_to_open_positions(
            self,
    ) -> Dict[str, Union[str, int, decimal.Decimal]]:
        """
        Method that forms the dictionary with which to open position.
        """
        if self.order_type == MetaTrader5.ORDER_TYPE_BUY:
            price = self.get_buy_price()
        else:
            price = self.get_sell_price()
        request = {
            "action": self.action,
            "symbol": self.symbol,
            "volume": self.volume,
            "type": self.order_type,
            "price": price,
            "tp": self.tp,
            "sl": self.sl,
            "deviation": self.deviation,
            "magic": self.magic,
            "comment": self.comment,
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
            "action": self.action,
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
            symbol=self.symbol
        )
        if positions:
            results = []
            for position in positions:
                request = self.__prepare_to_close_positions(position)
                results.append(self.__send_to_metatrader(request))
            return results
        raise PositionException(f" Not found positions for symbol {self.symbol}")

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
