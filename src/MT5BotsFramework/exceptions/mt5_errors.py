"""
Exceptions for MT5BotFramework
"""


class InitializeException(Exception):
    """Exception for MetaTrader5 initialize error"""


class AccountConnectException(Exception):
    """Exception for MetaTrader5 account connect error"""


class PositionException(Exception):
    """Exception for MetaTrader5 position not found error"""


class BalanceException(Exception):
    """Exception for MetaTrader5 balance not found error"""


class UnknownException(Exception):
    """Exception for unknown error"""
