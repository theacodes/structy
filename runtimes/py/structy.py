# TODO: License header
from __future__ import annotations

import dataclasses
import struct
import mmap

from typing import Union, ByteString, List, ClassVar, Type

_StructBuffer = Union[bytearray, memoryview, mmap.mmap]


def _packed_fields(inst: Union[Type[Struct], Struct]) -> List[str]:
    return [field.name for field in dataclasses.fields(inst)]


class Struct:
    _PACK_STRING: ClassVar[str] = ""
    PACKED_SIZE: ClassVar[int] = 0

    def __init__(self, *args, **kwargs):
        pass

    def pack_into(self, *, buffer: _StructBuffer, offset: int) -> None:
        """TODO"""
        values = [getattr(self, field) for field in _packed_fields(self)]

        struct.pack_into(">" + self._PACK_STRING, buffer, offset, *values)

    def pack(self) -> ByteString:
        """TODO"""
        buf = bytearray(self.PACKED_SIZE)
        self.pack_into(buffer=buf, offset=0)
        return buf

    @classmethod
    def unpack_from(cls, *, buffer: _StructBuffer, offset: int) -> Struct:
        values = struct.unpack_from(">" + cls._PACK_STRING, buffer, offset)
        kwargs = dict(zip(_packed_fields(cls), values))

        # While python's `__index__` protocol helps serialize fix16 types,
        # we have to manually convert them when deserializing.
        fix16_fields = [
            field.name for field in dataclasses.fields(cls) if field.type == Fix16
        ]

        for field in fix16_fields:
            value = kwargs[field]
            f16_value = Fix16(0)
            f16_value._value = value
            kwargs[field] = f16_value

        return cls(**kwargs)

    @classmethod
    def unpack(cls, buffer: _StructBuffer) -> Struct:
        return cls.unpack_from(buffer=buffer, offset=0)


_FIX16_ONE: int = 0x00010000


def _fix16_from_float(x: float) -> int:
    return int(x * 65536.0 + 0.5 if x >= 0 else x * 65536.0 - 0.5)


def _fix16_to_float(x: int) -> float:
    return float(x) / _FIX16_ONE


def _fix16_clamp(x: int) -> int:
    if x > 32767:
        return 32767
    elif x < -32768:
        return -32768
    return x


class Fix16:
    def __init__(self, float_value):
        self._value = _fix16_from_float(float_value)

    def __eq__(self, other):
        return self._value == other._value

    def __repr__(self):
        return f"<Fix16 0x{self._value:08x} {_fix16_to_float(self._value)}>"

    def __str__(self):
        return _fix16_to_float(self._value)

    def __add__(self, other):
        return _fix16_clamp(self._value + other._value)

    def __sub__(self, other):
        return _fix16_clamp(self._value - other._value)

    def __mul__(self, other):
        return _fix16_clamp(self._value * other._value)

    def __truediv__(self, other):
        return _fix16_clamp(self._value / other._value)

    def __mod__(self, other):
        return _fix16_clamp(self._value % other._value)

    def __index__(self) -> int:
        return self._value
