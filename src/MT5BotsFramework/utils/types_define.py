from typing import Literal
import MetaTrader5
from MT5BotsFramework.models.data_models import DataRequest


def order_type_define(
    order_type: Literal["buy", "sell"], data_request: DataRequest
) -> DataRequest:
    """
    Define type order.
    :param order_type: Buy or Sell
    :param data_request: DataRequest object.
    :return: None
    """
    order_type = order_type.lower()
    if order_type == "buy":
        data_request.type = MetaTrader5.ORDER_TYPE_BUY
    elif order_type == "sell":
        data_request.type = MetaTrader5.ORDER_TYPE_SELL
    else:
        raise ValueError(
            'The type of order sent is not accepted, it must be "buy" or "sell"'
        )
    return data_request
