import MetaTrader5


class StatusMeta(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            instance = super().__call__(*args, **kwargs)
            cls._instances[cls] = instance
        return cls._instances[cls]


class Status(metaclass=StatusMeta):
    action = MetaTrader5.TRADE_ACTION_DEAL
    order_type = None
    symbol = None
    volume = 0.01
    price = None
    deviation = 20
    magic = 0
    comment = "V3N2R4"
    type_time = MetaTrader5.ORDER_TIME_GTC
    type_filling = MetaTrader5.ORDER_FILLING_RETURN

    def order_type_redefine(self, order_type: str):
        order_type = order_type.lower()
        if order_type == "buy":
            self.order_type = MetaTrader5.ORDER_TYPE_BUY
        elif order_type == "sell":
            self.order_type = MetaTrader5.ORDER_TYPE_SELL
        else:
            raise ValueError(
                'The type of order sent is not accepted, it must be "buy" or "sell"'
            )

    def update_to_open_order(self):
        if all([self.order_type is None, self.symbol is None]):
            raise ValueError("Order Type or Symbol not define")
        count = 0
        while count < 3:
            try:
                if self.order_type == MetaTrader5.ORDER_TYPE_BUY:
                    self.price = (
                        MetaTrader5.symbol_info_tick(  # pylint: disable=maybe-no-member
                            self.symbol
                        ).ask
                    )
                else:
                    self.price = (
                        MetaTrader5.symbol_info_tick(  # pylint: disable=maybe-no-member
                            self.symbol
                        ).bid
                    )
                return
            except AttributeError:
                count += 1
        raise TypeError("Meta Trader not return order or price")

    def update_to_close_order(self):
        if all([self.order_type is None, self.symbol is None]):
            raise ValueError("Order Type or Symbol not define")
        count = 0
        while count < 3:
            try:
                if self.order_type == MetaTrader5.ORDER_TYPE_BUY:
                    self.order_type = MetaTrader5.ORDER_TYPE_SELL
                    self.price = (
                        MetaTrader5.symbol_info_tick(  # pylint: disable=maybe-no-member
                            self.symbol
                        ).bid
                    )
                else:
                    self.order_type = MetaTrader5.ORDER_TYPE_BUY
                    self.price = (
                        MetaTrader5.symbol_info_tick(  # pylint: disable=maybe-no-member
                            self.symbol
                        ).ask
                    )
                return
            except TypeError:
                count += 1
        raise TypeError("Meta Trader not return order or price")
