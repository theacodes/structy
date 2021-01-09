# Copyright (c) 2021 Alethea Katherine Flowers.
# Published under the standard MIT License.
# Full text available at: https://opensource.org/licenses/MIT

from structy import fix16


class TestFix16:
    def test_basic(self):
        val = fix16.Fix16(1.0)
        assert val._value == 65536
        val = fix16.Fix16(-1.0)
        assert val._value == -65536
        val = fix16.Fix16(10.0)
        assert val._value == 655360
        val = fix16.Fix16(-10.0)
        assert val._value == -655360

    def test_saturate(self):
        a = fix16.Fix16(65530.0)
        b = fix16.Fix16(100.0)
        assert (a + b) == fix16.Fix16(65535.0)

        a = fix16.Fix16(-65530.0)
        assert (a - b) == fix16.Fix16(-65535.0)

    def test_operations(self):
        a = fix16.Fix16(10.5)
        b = fix16.Fix16(5.25)

        assert (a + b) == fix16.Fix16(15.75)
        assert (a - b) == fix16.Fix16(5.25)
        assert (a * b) == fix16.Fix16(55.125)
        assert (a * -b) == fix16.Fix16(-55.125)
        assert (a / b) == fix16.Fix16(2)
        assert (a / -b) == fix16.Fix16(-2)
        assert (a / fix16.Fix16(raw_value=0xFFFFFFFF)) == fix16.Fix16(
            raw_value=0x00000015
        )
        assert (a / fix16.Fix16(raw_value=0x00000015)) == fix16.Fix16(
            raw_value=0xFFFFFFFF
        )
        assert (a % b) == fix16.Fix16(0)

    def test_str_repr(self):
        a = fix16.Fix16(10.5)

        assert str(a) == "10.5Q16.16"
        assert repr(a) == "<Fix16 0x000a8000 10.5>"
