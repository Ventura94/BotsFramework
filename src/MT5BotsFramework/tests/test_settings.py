import pytest
import MetaTrader5
from pytest_mock.plugin import MockerFixture
from MT5BotsFramework.settings import Settings


@pytest.fixture
def settings():
    return Settings()


@pytest.fixture
def settings_other_instance():
    return Settings()


def test_settings_singleton(settings, settings_other_instance):
    settings.symbol = "BTC"
    assert settings_other_instance.symbol is "BTC"


def test_order_type_redefine_buy(settings):
    settings.order_type_redefine(order_type="Buy")
    assert settings.order_type == MetaTrader5.ORDER_TYPE_BUY


def test_order_type_redefine_sell(settings):
    settings.order_type_redefine(order_type="sEll")
    assert settings.order_type == MetaTrader5.ORDER_TYPE_SELL


def test_order_type_redefine_error(settings):
    settings.symbol = None
    with pytest.raises(ValueError, match='The type of order sent is not accepted, it must be "buy" or "sell"'):
        settings.order_type_redefine(order_type="other")


def test_update_to_open_order_type_none(settings):
    settings.order_type = None
    with pytest.raises(ValueError, match="Order Type or Symbol not define"):
        settings.update_to_open_order()


def test_update_to_open_order_symbol_none(settings):
    settings.symbol = None
    with pytest.raises(ValueError, match="Order Type or Symbol not define"):
        settings.update_to_open_order()
