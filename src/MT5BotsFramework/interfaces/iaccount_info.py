"""
Account info interface.
"""

from abc import ABC, abstractmethod


class IAccountInfo(ABC):
    """
    This class is the interface for account info.
    """

    @property
    @abstractmethod
    def leverage(self):
        ...

    @property
    @abstractmethod
    def profit(self) -> float:
        """
        Get profit of the account.

        :return: Profit of the account.
        """

    @property
    @abstractmethod
    def balance(self) -> float:
        """
        Get balance of the account.

        :return: Balance of the account.
        """
