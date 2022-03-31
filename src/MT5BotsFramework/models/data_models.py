from dataclasses import dataclass
from typing import Dict, Union
from MT5BotsFramework.tools.clean_data import clean_data_to_dict


@dataclass
class DataRequest:
    type: int = None
    price: float = None
    symbol: str = None
    action: int = None
    volume: float = None
    sl: float = None
    tp: float = None
    deviation: int = None
    magic: int = None
    comment: str = None
    type_time: int = None
    type_filling: int = None
    position: int = None

    @classmethod
    def to_dict(cls) -> Dict[str, Union[str, float, int]]:
        return clean_data_to_dict(cls)
