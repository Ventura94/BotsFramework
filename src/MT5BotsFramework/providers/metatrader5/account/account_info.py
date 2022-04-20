"""
Module account info class for MetaTrader5
"""
import MetaTrader5
from MT5BotsFramework.interfaces.iaccount_info import IAccountInfo


class AccountInfo(IAccountInfo):
    """
    Account Info class for MetaTrader5.
    """

    @property
    def leverage(self) -> float:
        return MetaTrader5.account_info().leverage  # pylint: disable=maybe-no-member

    @property
    def profit(self) -> float:
        return (MetaTrader5.MetaTrader5.account_info().profit  # pylint: disable=maybe-no-member
                )

    @property
    def balance(self) -> float:
        return (MetaTrader5.MetaTrader5.account_info().balance  # pylint: disable=maybe-no-member
                )
