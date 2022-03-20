"""
Status module.
"""
import MetaTrader5


class StatusMeta(type):
    """
    Status metaclass, necessary for the Singleton Pattern Design.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Status(metaclass=StatusMeta):
    """
    Status class.
    """
    action = MetaTrader5.TRADE_ACTION_DEAL
    order_type = None
    symbol = None
    volume = 0.01
    sl = None
    tp = None
    deviation = 20
    magic = 0
    comment = "V3N2R4"
    type_time = MetaTrader5.ORDER_TIME_GTC
    type_filling = MetaTrader5.ORDER_FILLING_RETURN

    @property
    def price(self):
        if all([self.order_type is None, self.symbol is None]):
            raise ValueError("Order Type or Symbol not define")
        for i in range(3):
            try:
                if self.order_type == MetaTrader5.ORDER_TYPE_BUY:
                    return MetaTrader5.symbol_info_tick(  # pylint: disable=maybe-no-member
                        self.symbol
                    ).ask
                else:
                    return MetaTrader5.symbol_info_tick(  # pylint: disable=maybe-no-member
                        self.symbol
                    ).bid
            except AttributeError:
                pass
        raise TypeError("Meta Trader not return order or price")

    @classmethod
    def order_type_define(cls, order_type: str):
        order_type = order_type.lower()
        if order_type == "buy":
            cls.order_type = MetaTrader5.ORDER_TYPE_BUY
        elif order_type == "sell":
            cls.order_type = MetaTrader5.ORDER_TYPE_SELL
        else:
            raise ValueError(
                'The type of order sent is not accepted, it must be "buy" or "sell"'
            )

    @classmethod
    def update_to_close_order(cls):
        if all([cls.order_type is None, cls.symbol is None]):
            raise ValueError("Order Type or Symbol not define")
        count = 0
        while count < 3:
            try:
                if cls.order_type == MetaTrader5.ORDER_TYPE_BUY:
                    cls.order_type = MetaTrader5.ORDER_TYPE_SELL
                else:
                    cls.order_type = MetaTrader5.ORDER_TYPE_BUY
                return
            except TypeError:
                count += 1
        raise TypeError("Meta Trader not return order or price")
