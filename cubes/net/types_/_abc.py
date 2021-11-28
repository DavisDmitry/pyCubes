import abc
import io
from typing import Generic, TypeVar

# pylint: disable=C0103

T = TypeVar("T")


class AbstractType(abc.ABC, Generic[T]):
    __slots__ = ("_value",)

    def __init__(self, value: T):
        self.validate(value)
        self._value = value

    @classmethod
    @abc.abstractmethod
    def validate(cls, value: T) -> None:
        """"""

    @abc.abstractmethod
    def pack(self) -> bytes:
        """"""

    @classmethod
    @abc.abstractmethod
    def unpack(cls, data: bytes) -> T:
        """"""

    @abc.abstractmethod
    def to_buffer(self, buffer: io.BytesIO) -> None:
        """"""

    @classmethod
    @abc.abstractmethod
    def from_buffer(cls, buffer: io.BytesIO) -> T:
        """"""
