"""
Symbol Info module for MetaTrader5
"""
import MetaTrader5
from BotsFramework.interfaces.providers.isymbol_info import ISymbolInfo


class SymbolInfo(ISymbolInfo):
    """
    Symbol info class for MetaTrader5
    """

    symbol: str = None

    @property
    def ask(self) -> float:
        return MetaTrader5.symbol_info_tick(  # pylint: disable=maybe-no-member
            self.symbol).ask

    @property
    def bid(self) -> float:
        return MetaTrader5.symbol_info_tick(  # pylint: disable=maybe-no-member
            self.symbol).bid

    @property
    def points(self) -> float:
        return MetaTrader5.symbol_info(  # pylint: disable=maybe-no-member
            self.symbol).point

    @property
    def symbol_contract_size(self) -> float:
        return MetaTrader5.symbol_info(  # pylint: disable=maybe-no-member
            self.symbol).trade_contract_size

    @property
    def tick_value(self) -> float:
        return MetaTrader5.symbol_info(  # pylint: disable=maybe-no-member
            self.symbol).trade_tick_value

    @property
    def tick_size(self) -> float:
        return MetaTrader5.symbol_info(  # pylint: disable=maybe-no-member
            self.symbol).trade_tick_size
