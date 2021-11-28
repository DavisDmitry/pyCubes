import io

from cubes.net.types_ import _abc


class StupidValidationMixin(_abc.AbstractType[_abc.T]):
    TYPE: _abc.T

    @classmethod
    def validate(cls, value: _abc.T) -> None:
        cls._TYPE(value)


class RangeValidationMixin(_abc.AbstractType[_abc.T]):
    TYPE: _abc.T
    _RANGE: tuple[_abc.T, _abc.T]

    @classmethod
    def validate(cls, value: _abc.T) -> None:
        value = cls._TYPE(value)
        min_, max_ = cls._RANGE
        if value < min_ or value > max_:
            raise ValueError


class BufferPackMixin(_abc.AbstractType[_abc.T]):
    def pack(self) -> bytes:
        buffer = io.BytesIO()
        self.to_buffer(buffer)
        return buffer.getvalue()
