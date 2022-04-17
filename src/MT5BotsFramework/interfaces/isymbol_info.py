from abc import ABC, abstractmethod


class ISymbolInfo(ABC):
        
    def __init__(self, symbol:str) -> None:
        self.symbol = symbol   
    
    @property
    @abstractmethod
    def ask(self) -> float:
        """
        Get buy price.
        """

    @property
    @abstractmethod
    def bid(self) -> float:
        """
        Get sell price.
        :return: Sell price.
        """

    @property
    @abstractmethod
    def points(self) -> float:
        ...

    @property
    @abstractmethod
    def symbol_contract_size(self)->float:
        ...
    
    @property
    @abstractmethod
    def tick_value(self)->float:
        ...
        
    @property
    @abstractmethod
    def tick_size(self)->float:
        ...
    