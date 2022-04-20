from inspect import signature
from typing import Type, TypeVar, Dict, Union, Any

T = TypeVar("T")


def clean_data_to_dict(self: object) -> Dict[str, Union[str, float, int]]:
    data = {}
    for field in signature(self.__class__).parameters:
        if getattr(self, field) is not None:
            data[field] = getattr(self, field)
    return data
