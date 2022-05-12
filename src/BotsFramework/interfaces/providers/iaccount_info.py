"""
Account info interface.
"""

from abc import ABC, abstractmethod


class IAccountInfo(ABC):

    @property
    @abstractmethod
    def leverage(self):
        """
        Return leverage of the account
        """

    @property
    @abstractmethod
    def profit(self) -> float:
        """
        Return profit of the account
        """

    @property
    @abstractmethod
    def balance(self) -> float:
        """
        Return balance of the account.
        """
