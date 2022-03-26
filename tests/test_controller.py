"""
Bot test module.
"""
import pytest
import MetaTrader5
from pytest_mock.plugin import MockerFixture
from MT5BotsFramework.status import Status
from MT5BotsFramework.core.controller import Controller
from MT5BotsFramework.tests.test_status import (
    mocker_symbol_info_tick_method,
    status_symbol_btcusd_order_type_buy,
)


@pytest.fixture
def mocker_controller(mocker: MockerFixture) -> Controller:
    mocker.patch.object(MetaTrader5, "initialize", return_value=True)
    return Controller()


def test_prepare_to_open_positions(
    mocker_controller: Controller,
    mocker_symbol_info_tick_method: MockerFixture,
    mocker: MockerFixture,
) -> None:
    mocker.patch.object(
        MetaTrader5, "symbol_info_tick", return_value=mocker_symbol_info_tick_method
    )
    status_symbol_btcusd_order_type_buy()
    expected_result = {
        "action": 1,
        "symbol": "BTCUSD",
        "volume": 0.01,
        "type": 0,
        "price": 3.0,
        "deviation": 20,
        "magic": 0,
        "comment": "V3N2R4",
        "type_time": 0,
        "type_filling": 2,
    }
    assert mocker_controller.prepare_to_open_positions() == expected_result
