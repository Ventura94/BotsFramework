"""
 MetaTrader5 controller module.
"""

import time
import threading
from typing import List, Dict, Union
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

    def get_symbol_point(self) -> float:
        return MetaTrader5.symbol_info(self.initial_data.symbol).point

    def get_symbol_contract_size(self):
        return MetaTrader5.symbol_info(self.initial_data.symbol).trade_contract_size

    def get_tick_value(self):
        return MetaTrader5.symbol_info(self.initial_data.symbol).trade_tick_value

    def get_tick_size(self):
        return MetaTrader5.symbol_info(self.initial_data.symbol).trade_tick_size

    def get_leverage(self):
        return MetaTrader5.account_info().leverage

    def get_account_profit(self):
        return MetaTrader5.MetaTrader5.account_info().profit

    @staticmethod
    def __prepare_upgrade_sl(ticket: int, sl: float) -> Dict[str, Union[int, float]]:
        return DataRequest(
            action=MetaTrader5.TRADE_ACTION_SLTP, position=ticket, sl=sl
        ).clean_dict()

    def upgrade_stop_lost(self, ticket: int, sl: float) -> OrderSendResult:
        request = self.__prepare_upgrade_sl(ticket=ticket, sl=sl)
        return self.__send_to_metatrader(request)

    def trailing_stop(self, ticket: int, points: float) -> None:
        threading.Thread(target=self.__trailing_stop, args=(ticket, points)).start()

    def __trailing_stop(self, ticket: int, points: float) -> None:
        """
        Trailing stop.
        """
        try:
            position = self.get_position_by_ticket(ticket)
            last_sl_used = 0
            while True:
                try:
                    if position.type == MetaTrader5.ORDER_TYPE_BUY:
                        sl = self.get_buy_price() - points * self.get_symbol_point()
                        if sl > last_sl_used or last_sl_used == 0:
                            last_sl_used = sl
                            self.upgrade_stop_lost(ticket=ticket, sl=sl)
                    else:
                        sl = self.get_buy_price() + points * self.get_symbol_point()
                        if sl < last_sl_used or last_sl_used == 0:
                            last_sl_used = sl
                            self.upgrade_stop_lost(ticket=ticket, sl=sl)
                    time.sleep(5)
                except UnknownException:
                    pass
        except PositionException:
            pass

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

    def __prepare_to_close_positions(
            self,
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
            price = self.get_sell_price()
        else:
            order_type = MetaTrader5.ORDER_TYPE_BUY
            price = self.get_buy_price()
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

    def close_positions_by_ticket(self, ticket: int) -> OrderSendResult:
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
