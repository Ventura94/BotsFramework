"""
Metatrader Service Module
"""
import MetaTrader5
from MT5BotsFramework.interfaces.iservice import IService
from MT5BotsFramework.interfaces.iaccount_info import IAccountInfo
from MT5BotsFramework.interfaces.iposition import IPosition
from MT5BotsFramework.interfaces.isymbol_info import ISymbolInfo
from MT5BotsFramework.providers.metatrader5.account.account_info import AccountInfo
from MT5BotsFramework.providers.metatrader5.symbol.symbol_info import SymbolInfo
from MT5BotsFramework.providers.metatrader5.position.position import Position
from MT5BotsFramework.providers.metatrader5.exceptions import InitializeException


class MetaTraderService(IService):
    """
    Metatrader Service Class
    """
    account_info: IAccountInfo = None
    position: IPosition = None
    symbol_info: ISymbolInfo = None

    def __init__(self) -> None:
        if not MetaTrader5.initialize():  # pylint: disable=maybe-no-member
            MetaTrader5.shutdown()  # pylint: disable=maybe-no-member
            raise InitializeException(MetaTrader5.last_error()  # pylint: disable=maybe-no-member
                                      )
        self.account_info: IAccountInfo = AccountInfo
        self.position: IPosition = Position
        self.symbol_info: ISymbolInfo = SymbolInfo
