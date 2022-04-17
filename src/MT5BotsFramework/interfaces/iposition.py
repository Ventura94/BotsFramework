from abc import ABC, abstractmethod
from typing import Any


class IPosition(ABC):

    @abstractmethod
    def open_positions(self) -> Any:
        """
        Open a position at market price.
        """           
        
    
    @abstractmethod
    def get_position(self) -> Any:
        """
        Get position by ticket.
        :param ticket: Ticket of the position.
        :return: TradePosition object.
        """        


    @abstractmethod
    def close_positions(self) -> Any:
        """
        Close a position for your ticket.

        :return: Closing result.
        """
        

    @abstractmethod
    def close_positions_by_symbol(self) -> Any:
        """
        Close all positions of a symbol.
        """
    