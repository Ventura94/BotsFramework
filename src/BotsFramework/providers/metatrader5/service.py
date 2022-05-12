"""
Metatrader Service Module
"""
import MetaTrader5
from BotsFramework.interfaces.iservice import IService
from BotsFramework.interfaces.providers.iaccount_info import IAccountInfo
from BotsFramework.interfaces.providers.iposition import IPosition
from BotsFramework.interfaces.providers.isymbol_info import ISymbolInfo
from BotsFramework.providers.metatrader5.account.account_info import AccountInfo
from BotsFramework.providers.metatrader5.symbol.symbol_info import SymbolInfo
from BotsFramework.providers.metatrader5.position.position import Position
from BotsFramework.providers.metatrader5.exceptions import InitializeException


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
