"""
Position interface
"""
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
    def get_position_by_id(self, position_id: int) -> Any:
        """
        Return position by ticket.
        """

    @abstractmethod
    def close_positions_by_id(self, position_id: int) -> Any:
        """
        Close a position for ticket.
        """

    @abstractmethod
    def close_positions_by_symbol(self, symbol: str) -> Any:
        """
        Close all positions of a symbol.
        """
