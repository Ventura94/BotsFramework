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
from MT5BotsFramework.exceptions.mt5_errors import (
    PositionException,
    InitializeException,
    BalanceException,
    UnknownException,
)
from MT5BotsFramework.models.data_models import DataRequest


class Controller:
    """
    Controller MetaTrader5 bot class.
    """

    def __init__(self, initial_data: DataRequest) -> None:
        if not MetaTrader5.initialize(  # pylint: disable=maybe-no-member
                login=Status().account,
                password=Status().password,
                server=Status().server,
        ):
            MetaTrader5.shutdown()  # pylint: disable=maybe-no-member
            raise InitializeException(MetaTrader5.last_error())
        self.initial_data = initial_data

    def get_buy_price(self) -> float:
        """
        Get buy price.
        :return: Buy price.
        """
        return MetaTrader5.symbol_info_tick(  # pylint: disable=maybe-no-member
            self.initial_data.symbol
        ).ask

    def get_sell_price(self) -> float:
        """
        Get sell price.
        :return: Sell price.
        """

        return MetaTrader5.symbol_info_tick(  # pylint: disable=maybe-no-member
            self.initial_data.symbol
        ).bid

    def __prepare_to_open_market_positions(
            self, data_request: DataRequest
    ) -> Dict[str, Union[str, int, float]]:
        """
        Method that forms the dictionary with which to open position.
        """
        if data_request.type == MetaTrader5.ORDER_TYPE_BUY:
            data_request.price = self.get_buy_price()
        else:
            data_request.price = self.get_sell_price()
        data_request.action = MetaTrader5.TRADE_ACTION_DEAL
        return data_request.clean_dict()

    def open_market_positions(self, data_request: DataRequest) -> OrderSendResult:
        """
        Open a position at market price.
        """
        request = self.__prepare_to_open_market_positions(data_request)
        return self.__send_to_metatrader(request)

    @staticmethod
    def get_balance() -> float:
        """
        Get balance of the account.

        :return: Balance of the account.
        """
        return (
            MetaTrader5.MetaTrader5.account_info().balance  # pylint: disable=maybe-no-member
        )

    @staticmethod
    def __prepare_to_close_positions(
            position: TradePosition,
    ) -> Dict[str, Union[str, float, int]]:
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

        return DataRequest(
            action=MetaTrader5.TRADE_ACTION_DEAL,
            symbol=symbol,
            position=ticket,
            price=price,
            volume=volume,
            type=order_type,
        ).clean_dict()

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
            symbol=self.initial_data.symbol
        )
        if positions:
            results = []
            for position in positions:
                request = self.__prepare_to_close_positions(position)
                results.append(self.__send_to_metatrader(request))
            return results
        raise PositionException(
            f" Not found positions for symbol {self.initial_data.symbol}"
        )

    def get_profit_by_ticket(self, ticket: int) -> float:
        """
        Get profit by ticket.

        :param ticket: Ticket of the position.
        :return: Profit of the position.
        """
        position = self.get_position_by_ticket(ticket)
        return position.profit

    @staticmethod
    def __send_to_metatrader(
            request: Dict[str, Union[str, int, float]]
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
            elif result.retcode == MetaTrader5.TRADE_RETCODE_NO_MONEY:
                raise BalanceException("Not enough money to open position")
            last_result = result
        raise UnknownException(f"Error: {last_result.comment}")

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
