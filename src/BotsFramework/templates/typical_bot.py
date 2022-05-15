"""
Abstract class Strategy, to implement strategy bots.
"""
from BotsFramework.interfaces.iservice import IService
from BotsFramework.interfaces.providers.iposition import IPosition
from BotsFramework.interfaces.providers.isymbol_info import ISymbolInfo
from BotsFramework.interfaces.providers.iaccount_info import IAccountInfo


class Bot:
    account_info: IAccountInfo = None
    position: IPosition = None
    symbol_info: ISymbolInfo = None

    def __init__(self, service_provider: IService) -> None:
        self.position = service_provider.position
        self.account_info = service_provider.account_info
        self.symbol_info = service_provider.symbol_info
