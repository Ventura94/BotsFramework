"""
Status module.
"""
from threading import Lock
from typing import Dict

import MetaTrader5


class StatusMeta(type):
    """
    Status metaclass, necessary for the Singleton Pattern Design.
    """

    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            with cls._lock:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]


class RequestConfig:
    action = MetaTrader5.TRADE_ACTION_DEAL
    order_type = None
    symbol = None
    volume = 0.01
    sl = None
    tp = None
    deviation = 20
    magic = 0
    comment = "V3N2R4"

    @property
    def price(self) -> None:
        """
        Last price.
        :return: None
        """
        if all([self.order_type is None, self.symbol is None]):
            raise ValueError("Order Type or Symbol not define")
        for _ in range(3):
            try:
                if self.order_type == MetaTrader5.ORDER_TYPE_BUY:
                    return (
                        MetaTrader5.symbol_info_tick(  # pylint: disable=maybe-no-member
                            self.symbol
                        ).ask
                    )
                return MetaTrader5.symbol_info_tick(  # pylint: disable=maybe-no-member
                    self.symbol
                ).bid
            except AttributeError:
                pass
        raise TypeError("Meta Trader not return order or price")

    @classmethod
    def order_type_define(cls, order_type: str) -> None:
        """
        Define type order.
        :param order_type: Buy or Sell
        :return: None
        """
        order_type = order_type.lower()
        if order_type == "buy":
            cls.order_type = MetaTrader5.ORDER_TYPE_BUY
        elif order_type == "sell":
            cls.order_type = MetaTrader5.ORDER_TYPE_SELL
        else:
            raise ValueError(
                'The type of order sent is not accepted, it must be "buy" or "sell"'
            )


class Status(metaclass=StatusMeta):
    """
    Status class.
    """
    account: int = None
    password: str = None
    server: str = None
    type_time: int = MetaTrader5.ORDER_TIME_GTC
    type_filling: int = MetaTrader5.ORDER_FILLING_RETURN
    request_config: Dict[int, RequestConfig] = {}

    @classmethod
    def register_request_config(cls, bot_id: int) -> RequestConfig:
        """
        Register the request configuration.
        :param bot_id: Bot ID.
        :return: None.
        """
        if cls.request_config.get(bot_id, None) is None:
            cls.request_config[bot_id] = RequestConfig()
        return cls.request_config.get(bot_id)
