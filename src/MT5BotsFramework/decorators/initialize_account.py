import MetaTrader5
from MT5BotsFramework.exceptions.mt5_errors import InitializeException


class InitializeAccount(object):
    """
    InitializeAccount class decorator.
    """

    def __init__(self, function) -> None:
        self.function = function

    def __call__(self, *args, **kwargs):
        if not MetaTrader5.initialize(  # pylint: disable=maybe-no-member
                login=account,
                password=BROKER_PASSWORD,
                server=BROKER_SERVER,
        ):
            MetaTrader5.shutdown()  # pylint: disable=maybe-no-member
            raise InitializeException("Error launching MetaTrader")
        result = self.function(*args, **kwargs)
        MetaTrader5.shutdown()  # pylint: disable=maybe-no-member
        return result
