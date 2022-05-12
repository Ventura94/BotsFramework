from dataclasses import dataclass
from typing import Dict, Union
from BotsFramework.utils.clean_data import clean_data_to_dict
from BotsFramework.providers.metatrader5.exceptions import (
    BalanceException,
    UnknownException,
)
from MetaTrader5 import OrderSendResult
import MetaTrader5


@dataclass
class DataRequest:
    type: int = None
    symbol: str = None
    price: float = None
    action: int = None
    volume: float = None
    sl: float = None
    tp: float = None
    deviation: int = None
    magic: int = None
    comment: str = None
    type_time: int = None
    type_filling: int = None
    position: int = None

    def clean_dict(self) -> Dict[str, Union[str, float, int]]:
        return clean_data_to_dict(self)

    def send_to_metatrader(self) -> OrderSendResult:
        """
        Send order to metatrader.
        """
        last_result = None
        for _ in range(3):
            result = MetaTrader5.order_send(  # pylint: disable=maybe-no-member
                self.clean_dict()
            )
            if result.retcode == MetaTrader5.TRADE_RETCODE_DONE:
                return result
            elif result.retcode == MetaTrader5.TRADE_RETCODE_NO_MONEY:
                raise BalanceException("Not enough money to open position")
            # TODO: Faltan las demás excepciones, crearla aquí y en las del modulo de excepciones            last_result = result
        raise UnknownException(f"Error: {last_result.comment}")
