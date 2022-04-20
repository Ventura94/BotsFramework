"""
Clean data Module
"""
from inspect import signature
from typing import TypeVar, Dict, Union

T = TypeVar("T")


def clean_data_to_dict(self: object) -> Dict[str, Union[str, float, int]]:
    """
    Delete None types and return dictionary
    """
    data = {}
    for field in signature(self.__class__).parameters:
        if getattr(self, field) is not None:
            data[field] = getattr(self, field)
    return data
