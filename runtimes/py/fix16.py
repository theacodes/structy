# Copyright (c) 2021 Alethea Katherine Flowers.
# Published under the standard MIT License.
# Full text available at: https://opensource.org/licenses/MIT

"""Very limited implmentation of Q16.16 fixed point arithmetic.

This is largely based on libfixmath's fix16:
* https://github.com/PetteriAimonen/libfixmath/blob/master/libfixmath/fix16.c

It's possible to use Python's Decimal class for this, but I wanted
to match fix16's behavior as much as possible.
"""


_FIX16_ONE: int = 0x00010000


def _fix16_from_float(x: float) -> int:
    return int(x * 65536.0 + 0.5 if x >= 0 else x * 65536.0 - 0.5)


def _fix16_to_float(x: int) -> float:
    return float(x) / _FIX16_ONE


def _fix16_clamp(x: int) -> int:
    if x > 2 ** 31 - 1:
        return 2 ** 31 - 1
    elif x < -(2 ** 31):
        return -(2 ** 31)
    return x


class Fix16:
    """A Q16.16 fixed-point value.

    Args:
        float_value: Creates a Fix16 that approximates the given float.
        raw_value: Creates a Fix16 from the binary representation. This
            is useful when deserializing Fix16 values from bytes.
    """

    def __init__(self, float_value=None, raw_value=None):
        if raw_value is not None:
            self._value = _fix16_clamp(raw_value)
        else:
            self._value = _fix16_clamp(_fix16_from_float(float_value))

    def __eq__(self, other):
        return self._value == other._value

    def __repr__(self):
        return f"<Fix16 0x{self._value:08x} {_fix16_to_float(self._value)}>"

    def __str__(self):
        return str(_fix16_to_float(self._value)) + "Q16.16"

    def __add__(self, other):
        return Fix16(raw_value=self._value + other._value)

    def __sub__(self, other):
        return Fix16(raw_value=self._value - other._value)

    def __mul__(self, other):
        product = self._value * other._value

        if product < 0:
            product -= 1

        result = product >> 16
        result += (product & 0x8000) >> 15

        return Fix16(raw_value=result)

    def __truediv__(self, other):
        a = self._value
        b = other._value

        remainder = a if a >= 0 else (-a)
        divider = b if b >= 0 else (-b)
        quotient = 0
        bit_pos = 17

        if divider & 0xFFF00000:
            shifted_div = (divider >> 17) + 1
            quotient = remainder // shifted_div
            remainder -= (quotient * divider) >> 17

        while not (divider & 0xF) and bit_pos >= 4:
            divider >>= 4
            bit_pos -= 4

        while remainder and bit_pos >= 0:
            shift = 67 - len(bin(-remainder)) & ~remainder >> 64
            if shift > bit_pos:  # pragma: no cover
                shift = bit_pos
            remainder <<= shift
            bit_pos -= shift

            div = remainder // divider
            remainder = remainder % divider
            quotient += div << bit_pos

            remainder <<= 1
            bit_pos -= 1

        quotient += 1
        result = quotient >> 1

        if (a ^ b) & 0x80000000:
            result = -result

        return Fix16(raw_value=result)

    def __mod__(self, other):
        result = self._value % other._value
        return Fix16(raw_value=result)

    def __neg__(self):
        return Fix16(raw_value=-self._value)

    def __index__(self) -> int:
        return self._value
