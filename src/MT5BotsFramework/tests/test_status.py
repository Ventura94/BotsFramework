"""
Status test module.
"""
import pytest
import MetaTrader5
from pytest_mock.plugin import MockerFixture
from MT5BotsFramework.status import Status


class Mocker_Symbol_Info_Tick_Method:
    ask = 3.0
    bid = 8.0

    def __init__(self, symbol=None):
        self.symbol = symbol


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
    Check that it complies with the operation of the Singleton design pattern.
    :param status: Status class.
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


def test_update_to_open_order_buy(mocker, status) -> None:
    mocker.patch.object(
        MetaTrader5, "symbol_info_tick", return_value=Mocker_Symbol_Info_Tick_Method
    )
    status.symbol = "BTCUSD"
    status.order_type = MetaTrader5.ORDER_TYPE_BUY
    status.update_to_open_order()
    assert status.price == Mocker_Symbol_Info_Tick_Method.ask


def test_update_to_open_order_sell(mocker, status) -> None:
    mocker.patch.object(
        MetaTrader5, "symbol_info_tick", return_value=Mocker_Symbol_Info_Tick_Method
    )
    status.symbol = "BTCUSD"
    status.order_type = MetaTrader5.ORDER_TYPE_SELL
    status.update_to_open_order()
    assert status.price == Mocker_Symbol_Info_Tick_Method.bid


def test_update_to_close_order_buy(mocker, status) -> None:
    mocker.patch.object(
        MetaTrader5, "symbol_info_tick", return_value=Mocker_Symbol_Info_Tick_Method
    )
    status.symbol = "BTCUSD"
    status.order_type = MetaTrader5.ORDER_TYPE_BUY
    status.update_to_close_order()
    assert status.price == Mocker_Symbol_Info_Tick_Method.bid


def test_update_to_close_order_sell(mocker, status) -> None:
    mocker.patch.object(
        MetaTrader5, "symbol_info_tick", return_value=Mocker_Symbol_Info_Tick_Method
    )
    status.symbol = "BTCUSD"
    status.order_type = MetaTrader5.ORDER_TYPE_SELL
    status.update_to_close_order()
    assert status.price == Mocker_Symbol_Info_Tick_Method.ask


@pytest.mark.skipif(
    not MetaTrader5.initialize(), reason="Required MetaTrader5 platform"
)
def test_update_to_open_order_buy_not_mocker(status) -> None:
    status.symbol = "BTCUSD"
    status.order_type = MetaTrader5.ORDER_TYPE_BUY
    status.update_to_open_order()
    assert isinstance(status.price, float)


@pytest.mark.skipif(
    not MetaTrader5.initialize(), reason="Required MetaTrader5 platform"
)
def test_update_to_open_order_sell_not_mocker(status) -> None:
    status.symbol = "BTCUSD"
    status.order_type = MetaTrader5.ORDER_TYPE_SELL
    status.update_to_open_order()
    assert isinstance(status.price, float)


@pytest.mark.skipif(
    not MetaTrader5.initialize(), reason="Required MetaTrader5 platform"
)
def test_update_to_close_order_buy_not_mocker(status) -> None:
    status.symbol = "BTCUSD"
    status.order_type = MetaTrader5.ORDER_TYPE_BUY
    status.update_to_close_order()
    assert isinstance(status.price, float)


@pytest.mark.skipif(
    not MetaTrader5.initialize(), reason="Required MetaTrader5 platform"
)
def test_update_to_close_order_sell_not_mocker(status) -> None:
    status.symbol = "BTCUSD"
    status.order_type = MetaTrader5.ORDER_TYPE_SELL
    status.update_to_close_order()
    assert isinstance(status.price, float)
