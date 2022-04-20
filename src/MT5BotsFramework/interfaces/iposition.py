from abc import ABC, abstractmethod
from typing import Any


class IPosition(ABC):
    @abstractmethod
    def open_buy_positions(self, symbol: str, leverage: float) -> Any:
        """
        Open buy position at market price.
        """

    @abstractmethod
    def open_sell_positions(self, symbol: str, leverage: float) -> Any:
        """
        Open sell position at market price.
        """

    @abstractmethod
    def get_position(self) -> Any:
        """
        Get position by ticket.
        :param ticket: Ticket of the position.
        :return: TradePosition object.
        """

    @abstractmethod
    def close_positions(self) -> Any:
        """
        Close a position for your ticket.

        :return: Closing result.
        """

    @abstractmethod
    def close_positions_by_symbol(self) -> Any:
        """
        Close all positions of a symbol.
        """
