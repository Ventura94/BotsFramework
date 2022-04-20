from abc import ABC, abstractmethod


class IAccountInfo(ABC):
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
