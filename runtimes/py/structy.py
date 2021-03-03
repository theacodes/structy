# Copyright (c) 2021 Alethea Katherine Flowers.
# Published under the standard MIT License.
# Full text available at: https://opensource.org/licenses/MIT

"""Structy runtime components for Python

Structy helps deserialize and serialize structs to bytes. This module
provides runtime support for Structy-generated classes.
"""

from __future__ import annotations

__version__ = "2021.3.3"


import dataclasses
import struct
import mmap
from typing import Any, Union, ByteString, List, ClassVar, Type

_StructBuffer = Union[bytearray, memoryview, mmap.mmap]


def _packed_fields(inst: Union[Type[Struct], Struct]) -> List[dataclasses.Field]:
    return [field for field in dataclasses.fields(inst)]


def _pack_fix16_fields(self: Struct, values: Any) -> None:
    fix16_fields = [field.name for field in _packed_fields(self) if field.type == Fix16]

    for field in fix16_fields:
        value = values[field] * 0x00010000
        value += 0.5 if value >= 0 else -0.5
        values[field] = int(value)


def _unpack_fix16_fields(cls: Type, kwargs: Any) -> None:
    fix16_fields = [field.name for field in _packed_fields(cls) if field.type == Fix16]

    for field in fix16_fields:
        value = kwargs[field]
        kwargs[field] = float(value) / 0x00010000


# This bullshit is just to appease mypy. Fuckin' mypy, curse you for being useful.


class _Fix16:
    pass


Fix16 = Union[float, _Fix16]


class Struct:
    """A Structy Struct provides methods for packing and unpacking the
    struct's data to and from bytes."""

    _PACK_STRING: ClassVar[str] = ""
    PACKED_SIZE: ClassVar[int] = 0

    def __init__(self, *args, **kwargs):  # pragma: no cover
        pass

    def pack_into(self, *, buffer: _StructBuffer, offset: int) -> None:
        """Packs this struct's data into the given buffer at the given offset."""
        values = {
            field.name: getattr(self, field.name) for field in _packed_fields(self)
        }

        _pack_fix16_fields(self, values)

        struct.pack_into(">" + self._PACK_STRING, buffer, offset, *values.values())

    def pack(self) -> ByteString:
        """Packs this struct's data into a new ByteString."""
        buf = bytearray(self.PACKED_SIZE)
        self.pack_into(buffer=buf, offset=0)
        return buf

    @classmethod
    def unpack_from(cls: Type[Struct], *, buffer: _StructBuffer, offset: int) -> Struct:
        """Creates a new struct with the data unpacked from the given buffer at the given offset."""
        values = struct.unpack_from(">" + cls._PACK_STRING, buffer, offset)
        kwargs = dict(zip([field.name for field in _packed_fields(cls)], values))

        _unpack_fix16_fields(cls, kwargs)

        return cls(**kwargs)

    @classmethod
    def unpack(cls: Type[Struct], buffer: _StructBuffer) -> Struct:
        """Creates a new struct with the data unpacked from the given buffer."""
        return cls.unpack_from(buffer=buffer, offset=0)

    def __str__(self):
        pad_len = max(len(field.name) for field in _packed_fields(self)) + 3
        fields = "\n".join(f"· {field.name + ':':{pad_len}} {getattr(self, field.name)!r}" for field in _packed_fields(self))
        return f"{self.__class__.__name__}:\n{fields}"
