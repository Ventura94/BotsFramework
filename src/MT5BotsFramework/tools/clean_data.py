from inspect import signature
from typing import Type, TypeVar, Dict, Union, Any

T = TypeVar("T")


def clean_data_to_dict(self: object) -> Dict[str, Union[str, float, int]]:
    data = {}
    for field in signature(self.__class__).parameters:
        if getattr(self, field) is not None:
            data[field] = getattr(self, field)
    return data


def parse_data_model(cls: Type[T], **kwargs: Any) -> T:
    cls_fields = {field for field in signature(cls).parameters}
    native_args, new_args = {}, {}
    for name, val in kwargs.items():
        if name in cls_fields:
            native_args[name] = val
        else:
            raise ValueError(f"{name} is not a valid field for {cls.__name__}")
    return cls(**native_args)
