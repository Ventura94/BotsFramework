"""
Status module.
"""
from threading import Lock
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


class Status(metaclass=StatusMeta):
    """
    Status class.
    """

    account: int = None
    password: str = None
    server: str = None
    type_time: int = MetaTrader5.ORDER_TIME_GTC
    type_filling: int = MetaTrader5.ORDER_FILLING_RETURN
