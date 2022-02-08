from abc import ABC, abstractmethod
from core.controller import Controller


class Strategy(ABC):

    def __init__(self):
        self.controller = Controller(self.conf_file)

    @property
    @abstractmethod
    def conf_file(self) -> str:
        ...

    @abstractmethod
    def get_data(self):
        pass

    @abstractmethod
    def strategy_bot(self):
        data = self.get_data()  # pylint: disable=unused-argument

    def start(self):
        while True:
            self.strategy_bot()
