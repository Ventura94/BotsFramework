"""
Symbol Info Interface
"""

from abc import ABC, abstractmethod


class ISymbolInfo(ABC):
    def __init__(self, symbol: str) -> None:
        self.symbol = symbol

    @property
    @abstractmethod
    def ask(self) -> float:
        """
        Returns the current ask price of the symbol
        """

    @property
    @abstractmethod
    def bid(self) -> float:
        """
        This function returns the bid price of the symbol
        """

    @property
    @abstractmethod
    def points(self) -> float:
        """
        Returns the number of points for the symbol
        """
        ...

    @property
    @abstractmethod
    def symbol_contract_size(self) -> float:
        """
        Returns the contract size for the symbol
        """

    @property
    @abstractmethod
    def tick_value(self) -> float:
        """
        Returns the tick value of the symbol
        """

    @property
    @abstractmethod
    def tick_size(self) -> float:
        """
        Returns the tick size for the symbol
        """
