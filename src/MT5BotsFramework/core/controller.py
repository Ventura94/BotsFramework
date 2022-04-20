"""
 MetaTrader5 controller module.
"""

import time
import threading
from typing import List, Dict, Union
import MetaTrader5
from MetaTrader5 import (  # pylint: disable=no-name-in-module
    TradePosition, OrderSendResult,
)
from MT5BotsFramework.status import Status


class Controller:
    """
    Controller MetaTrader5 bot class.
    """

    @staticmethod
    def __prepare_upgrade_sl(ticket: int,
                             sl: float) -> Dict[str, Union[int, float]]:
        return DataRequest(action=MetaTrader5.TRADE_ACTION_SLTP,
                           position=ticket,
                           sl=sl).clean_dict()

    def upgrade_stop_lost(self, ticket: int, sl: float) -> OrderSendResult:
        request = self.__prepare_upgrade_sl(ticket=ticket, sl=sl)
        return self.__send_to_metatrader(request)

    def trailing_stop(self, ticket: int, points: float) -> None:
        threading.Thread(target=self.__trailing_stop,
                         args=(ticket, points)).start()

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
                        sl = self.get_buy_price(
                        ) - points * self.get_symbol_point()
                        if sl > last_sl_used or last_sl_used == 0:
                            last_sl_used = sl
                            self.upgrade_stop_lost(ticket=ticket, sl=sl)
                    else:
                        sl = self.get_buy_price(
                        ) + points * self.get_symbol_point()
                        if sl < last_sl_used or last_sl_used == 0:
                            last_sl_used = sl
                            self.upgrade_stop_lost(ticket=ticket, sl=sl)
                    time.sleep(5)
                except UnknownException:
                    pass
        except PositionException:
            pass

    @staticmethod
    def get_position_by_ticket(ticket: int) -> TradePosition:
        """
        Get position by ticket.
        :param ticket: Ticket of the position.
        :return: TradePosition object.
        """
        position = MetaTrader5.positions_get(  # pylint: disable=maybe-no-member
            ticket=ticket)
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
