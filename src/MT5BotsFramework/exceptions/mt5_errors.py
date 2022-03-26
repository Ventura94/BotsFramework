class InitializeException(Exception):
    """Exception for MetaTrader5 initialize error"""
    pass


class AccountConnectException(Exception):
    """Exception for MetaTrader5 account connect error"""
    pass


class PositionException(Exception):
    """Exception for MetaTrader5 position not found error"""
    pass
