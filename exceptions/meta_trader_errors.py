"""
This Module contains MetaTraderBot custom errors.
"""


class Error(Exception):
    """Base class for exceptions in this module."""


class InitializeError(Error):
    """Exception raised by MetaTrader startup errors.

    :param message: String with the message explanation of the error.
    """

    def __init__(self, message: str) -> None:
        super().__init__()
        self.message = message


class TypeOrderError(Error):
    """Exception raised by MetaTrader startup errors.

    :param message: String with the message explanation of the error.
    """

    def __init__(self, message: str) -> None:
        super().__init__()
        self.message = message
