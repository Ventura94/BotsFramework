from typing import Literal, Any
from MT5BotsFramework.interfaces.iposition import IPosition
from MT5BotsFramework.providers.metatrader5.data_models.data_request import DataRequest
from MT5BotsFramework.providers.metatrader5.symbol.symbol_info import SymbolInfo
from MT5BotsFramework.providers.metatrader5.exceptions import PositionException
import MetaTrader5
from MetaTrader5 import OrderSendResult


class Position(IPosition):
    def open_buy_positions(
        self, symbol: str, leverage: float = 0.01
    ) -> OrderSendResult:
        data_request = DataRequest
        data_request.type = MetaTrader5.ORDER_TYPE_BUY
        data_request.symbol = symbol
        data_request.price = SymbolInfo(symbol).ask
        data_request.volume = leverage
        data_request.action = MetaTrader5.TRADE_ACTION_DEAL
        return data_request.send_to_metatrader()

    def open_sell_positions(
        self, symbol: str, leverage: float = 0.01
    ) -> OrderSendResult:
        data_request = DataRequest
        data_request.type = MetaTrader5.ORDER_TYPE_SELL
        data_request.symbol = symbol
        data_request.price = SymbolInfo(symbol).bid
        data_request.volume = leverage
        data_request.action = MetaTrader5.TRADE_ACTION_DEAL
        return data_request.send_to_metatrader()

    def get_position(self) -> Any:
        pass

    def close_positions(self) -> Any:
        pass

    def close_positions_by_symbol(self, symbol: str) -> None:
        positions = MetaTrader5.positions_get(  # pylint: disable=maybe-no-member
            symbol=symbol
        )
        if positions:
            for position in positions:
                data_request = DataRequest()
                if position.type == MetaTrader5.ORDER_TYPE_BUY:
                    data_request.type = MetaTrader5.ORDER_TYPE_SELL
                    data_request.price = SymbolInfo(symbol).bid
                else:
                    data_request.type = MetaTrader5.ORDER_TYPE_BUY
                    data_request.price = SymbolInfo(symbol).ask
                data_request.action = MetaTrader5.TRADE_ACTION_DEAL
                data_request.symbol = position.symbol
                data_request.position = position.ticket
                data_request.volume = position.volume
                data_request.send_to_metatrader()
        raise PositionException(
            f" Not found positions for symbol {self.initial_data.symbol}"
        )
