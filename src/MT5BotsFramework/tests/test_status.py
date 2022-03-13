"""
Status test module.
"""
import pytest
import MetaTrader5
from MT5BotsFramework.status import Status


@pytest.fixture
def status() -> Status:
    """
    Status class fixture
    :return: Status class
    """
    return Status()


def test_status_singleton(
        status: Status,  # pylint: disable=redefined-outer-name
) -> None:
    """
    # TODO: Definir descripción de este test aclarando que debe cumplir con el patron de diseño Singleton
    :param status: Status class.
    :param status_other_instance: Status class
    :return: None
    """
    other_status = Status()
    status.symbol = "BTCUSD"
    assert other_status.symbol == "BTCUSD"


def test_order_type_redefine_buy(
        status: Status,  # pylint: disable=redefined-outer-name
) -> None:
    """
    Order type redefine buy test
    :param status: Status class.
    :return: None
    """
    status.order_type_redefine(order_type="Buy")
    assert status.order_type == MetaTrader5.ORDER_TYPE_BUY


def test_order_type_redefine_sell(
        status: Status,  # pylint: disable=redefined-outer-name
) -> None:
    """
    Order type redefine sell test
    :param status: Status class.
    :return: None
    """
    status.order_type_redefine(order_type="sEll")
    assert status.order_type == MetaTrader5.ORDER_TYPE_SELL


def test_order_type_redefine_error(
        status: Status,  # pylint: disable=redefined-outer-name
) -> None:
    """
    Order type redefine with error test
    :param status: Status class
    :return: None
    """
    status.symbol = None
    with pytest.raises(
            ValueError,
            match='The type of order sent is not accepted, it must be "buy" or "sell"',
    ):
        status.order_type_redefine(order_type="other")


def test_update_to_open_order_type_none(
        status: Status,  # pylint: disable=redefined-outer-name
) -> None:
    """
    Update to open with order type None value test
    :param status: Status class.
    :return: None
    """
    status.order_type = None
    with pytest.raises(ValueError, match="Order Type or Symbol not define"):
        status.update_to_open_order()


def test_update_to_open_order_symbol_none(
        status: Status,  # pylint: disable=redefined-outer-name
) -> None:
    """
    Update to open with symbol None value test
    :param status: Status class.
    :return: None
    """
    status.symbol = None
    with pytest.raises(ValueError, match="Order Type or Symbol not define"):
        status.update_to_open_order()


def test_update_to_close_order_type_none(
        status: Status,  # pylint: disable=redefined-outer-name
) -> None:
    """
    Update to close with order type None value test
    :param status: Status class.
    :return: None
    """
    status.order_type = None
    with pytest.raises(ValueError, match="Order Type or Symbol not define"):
        status.update_to_close_order()


def test_update_to_close_order_symbol_none(
        status: Status,  # pylint: disable=redefined-outer-name
) -> None:
    """
    Update to close with symbol None value test
    :param status: Status class.
    :return: None
    """
    status.symbol = None
    with pytest.raises(ValueError, match="Order Type or Symbol not define"):
        status.update_to_close_order()
