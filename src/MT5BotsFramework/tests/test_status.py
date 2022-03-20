"""
Status test module.
"""
import pytest
import MetaTrader5
from pytest_mock.plugin import MockerFixture
from MT5BotsFramework.status import Status


def status_symbol_btcusd_order_type_buy():
    Status.symbol = "BTCUSD"
    Status.order_type = MetaTrader5.ORDER_TYPE_BUY


def status_symbol_btcusd_order_type_sell():
    Status.symbol = "BTCUSD"
    Status.order_type = MetaTrader5.ORDER_TYPE_SELL


@pytest.fixture
def mocker_symbol_info_tick_method():
    class MockerSymbolInfoTickMethod:
        """
        Symbol info tick method mocker
        """

        ask = 3.0
        bid = 8.0

        def __init__(self, symbol: str = None) -> None:
            self.symbol = symbol

    return MockerSymbolInfoTickMethod


def test_order_type_redefine_buy() -> None:
    """
    Order type redefine buy test
    :return: None
    """
    Status.order_type_redefine(order_type="Buy")
    assert Status.order_type == MetaTrader5.ORDER_TYPE_BUY


def test_order_type_redefine_sell() -> None:
    """
    Order type redefine sell test
    :return: None
    """
    Status.order_type_redefine(order_type="sEll")
    assert Status.order_type == MetaTrader5.ORDER_TYPE_SELL


def test_order_type_redefine_error() -> None:
    """
    Order type redefine with error test
    :return: None
    """
    Status.symbol = None
    with pytest.raises(
            ValueError,
            match='The type of order sent is not accepted, it must be "buy" or "sell"',
    ):
        Status.order_type_redefine(order_type="other")


def test_update_to_open_order_type_none() -> None:
    """
    Update to open with order type None value test
    :return: None
    """
    Status.order_type = None
    with pytest.raises(ValueError, match="Order Type or Symbol not define"):
        Status.update_to_open_order()


def test_update_to_open_order_symbol_none() -> None:
    """
    Update to open with symbol None value test
    :return: None
    """
    Status.symbol = None
    with pytest.raises(ValueError, match="Order Type or Symbol not define"):
        Status.update_to_open_order()


def test_update_to_close_order_type_none() -> None:
    """
    Update to close with order type None value test
    :return: None.
    """
    Status.order_type = None
    with pytest.raises(ValueError, match="Order Type or Symbol not define"):
        Status.update_to_close_order()


def test_update_to_close_order_symbol_none() -> None:
    """
    Update to close with symbol None value test.
    :return: None.
    """
    Status.symbol = None
    with pytest.raises(ValueError, match="Order Type or Symbol not define"):
        Status.update_to_close_order()


def test_update_to_open_order_buy(
        mocker: MockerFixture,
        mocker_symbol_info_tick_method: MockerFixture,  # pylint: disable=redefined-outer-name
) -> None:
    """
    Update to open order buy test with MetaTrade5 object mocker.
    :param mocker: Mocker fixture.
    :param mocker_symbol_info_tick_method: Mocker method.
    :return: None.
    """
    mocker.patch.object(
        MetaTrader5, "symbol_info_tick", return_value=mocker_symbol_info_tick_method
    )
    status_symbol_btcusd_order_type_buy()
    Status.update_to_open_order()
    assert Status.price == mocker_symbol_info_tick_method.ask


def test_update_to_open_order_sell(
        mocker: MockerFixture,
        mocker_symbol_info_tick_method: MockerFixture,  # pylint: disable=redefined-outer-name
) -> None:
    """
    Update to open order sell test with MetaTrade5 object mocker.
    :param mocker: Mocker fixture.
    :param mocker_symbol_info_tick_method: Mocker method.
    :return: None.
    """
    mocker.patch.object(
        MetaTrader5, "symbol_info_tick", return_value=mocker_symbol_info_tick_method
    )
    status_symbol_btcusd_order_type_sell()
    Status.update_to_open_order()
    assert Status.price == mocker_symbol_info_tick_method.bid


def test_update_to_close_order_buy(
        mocker: MockerFixture,
        mocker_symbol_info_tick_method: MockerFixture,  # pylint: disable=redefined-outer-name
) -> None:
    """
    Update to close order buy test with MetaTrade5 object mocker.
    :param mocker: Mocker fixture
    :param mocker_symbol_info_tick_method: Mocker method.
    :return: None
    """
    mocker.patch.object(
        MetaTrader5, "symbol_info_tick", return_value=mocker_symbol_info_tick_method
    )
    status_symbol_btcusd_order_type_buy()
    Status.update_to_close_order()
    assert Status.price == mocker_symbol_info_tick_method.bid


def test_update_to_close_order_sell(
        mocker: MockerFixture,
        mocker_symbol_info_tick_method: MockerFixture,  # pylint: disable=redefined-outer-name
) -> None:
    """
    Update to close order sell test with MetaTrade5 object mocker.
    :param mocker: Mocker fixture
    :param mocker_symbol_info_tick_method: Mocker method.
    :return: None
    """
    mocker.patch.object(
        MetaTrader5, "symbol_info_tick", return_value=mocker_symbol_info_tick_method
    )
    status_symbol_btcusd_order_type_sell()
    Status.update_to_close_order()
    assert Status.price == mocker_symbol_info_tick_method.ask
