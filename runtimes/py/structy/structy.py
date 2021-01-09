# Copyright (c) 2021 Alethea Katherine Flowers.
# Published under the standard MIT License.
# Full text available at: https://opensource.org/licenses/MIT

"""Structy runtime components for Python

Structy helps deserialize and serialize structs to bytes. This module
provides runtime support for Structy-generated classes.
"""

from __future__ import annotations

import dataclasses
import struct
import mmap
from typing import Any, Union, ByteString, List, ClassVar, Type

try:
    from structy import fix16
except ImportError:  # pragma: no cover
    fix16 = None  # type: ignore

_StructBuffer = Union[bytearray, memoryview, mmap.mmap]


def _packed_fields(inst: Union[Type[Struct], Struct]) -> List[str]:
    return [field.name for field in dataclasses.fields(inst)]


def _unpack_fix16_fields(cls: Type, kwargs: Any):
    if fix16 is None:  # pragma: no cover
        return

    # While python's `__index__` protocol helps serialize fix16 types,
    # we have to manually convert them when deserializing.
    fix16_fields = [
        field.name for field in dataclasses.fields(cls) if field.type == fix16.Fix16
    ]

    for field in fix16_fields:
        value = kwargs[field]
        f16_value = fix16.Fix16(0)
        f16_value._value = value
        kwargs[field] = f16_value


class Struct:
    """A Structy Struct provides methods for packing and unpacking the
    struct's data to and from bytes."""

    _PACK_STRING: ClassVar[str] = ""
    PACKED_SIZE: ClassVar[int] = 0

    def __init__(self, *args, **kwargs):  # pragma: no cover
        pass

    def pack_into(self, *, buffer: _StructBuffer, offset: int) -> None:
        """Packs this struct's data into the given buffer at the given offset."""
        values = [getattr(self, field) for field in _packed_fields(self)]

        struct.pack_into(">" + self._PACK_STRING, buffer, offset, *values)

    def pack(self) -> ByteString:
        """Packs this struct's data into a new ByteString."""
        buf = bytearray(self.PACKED_SIZE)
        self.pack_into(buffer=buf, offset=0)
        return buf

    @classmethod
    def unpack_from(cls: Type[Struct], *, buffer: _StructBuffer, offset: int) -> Struct:
        """Creates a new struct with the data unpacked from the given buffer at the given offset."""
        values = struct.unpack_from(">" + cls._PACK_STRING, buffer, offset)
        kwargs = dict(zip(_packed_fields(cls), values))

        _unpack_fix16_fields(cls, kwargs)

        return cls(**kwargs)

    @classmethod
    def unpack(cls: Type[Struct], buffer: _StructBuffer) -> Struct:
        """Creates a new struct with the data unpacked from the given buffer."""
        return cls.unpack_from(buffer=buffer, offset=0)
