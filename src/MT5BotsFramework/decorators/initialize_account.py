import MetaTrader5
from MT5BotsFramework.exceptions.mt5_errors import InitializeException
from MT5BotsFramework.status import Status


class InitializeAccount(object):
    """
    InitializeAccount class decorator.
    """

    def __init__(self, function) -> None:
        self.status = Status()
        self.function = function

    def __call__(self, *args, **kwargs):
        if not MetaTrader5.initialize(  # pylint: disable=maybe-no-member
                login=self.status.account,
                password=self.status.password,
                server=self.status.server,
        ):
            MetaTrader5.shutdown()  # pylint: disable=maybe-no-member
            raise InitializeException("Error launching MetaTrader")
        result = self.function(*args, **kwargs)
        MetaTrader5.shutdown()  # pylint: disable=maybe-no-member
        return result
