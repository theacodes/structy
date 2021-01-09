# Copyright (c) 2021 Alethea Katherine Flowers.
# Published under the standard MIT License.
# Full text available at: https://opensource.org/licenses/MIT

from structy import fix16

import gemsettings

REF_DATA = bytearray(
    [
        # 2048
        0x08,
        0x00,
        # 0
        0x00,
        0x00,
        # 127
        0x00,
        0x7F,
        # -1.01
        0xFF,
        0xFE,
        0xFD,
        0x71,
        # 1.01
        0x00,
        0x01,
        0x02,
        0x8F,
        # -1.01
        0xFF,
        0xFE,
        0xFD,
        0x71,
        # 1.01
        0x00,
        0x01,
        0x02,
        0x8F,
        # 0.05
        0x00,
        0x00,
        0x0C,
        0xCD,
        # 0.2
        0x00,
        0x00,
        0x33,
        0x33,
        # 0.0
        0x00,
        0x00,
        0x00,
        0x00,
        # 1.0
        0x00,
        0x01,
        0x00,
        0x00,
        # 0.1
        0x00,
        0x00,
        0x19,
        0x9A,
        # 30.0
        0x00,
        0x1E,
        0x00,
        0x00,
        # 56
        0x00,
        0x38,
        # false
        0x00,
        # false
        0x00,
        # 0
        0x00,
        0x00,
        0x00,
        0x00,
    ]
)


def test_generated_pack():
    inst = gemsettings.GemSettings()

    output = inst.pack()

    assert bytearray(output) == REF_DATA


def test_generated_unpack():
    inst = gemsettings.GemSettings.unpack(REF_DATA)

    assert inst.adc_gain_corr == 2048
    assert inst.adc_offset_corr == 0
    assert inst.led_brightness == 127
    assert inst.castor_knob_min == fix16.Fix16(-1.01)
    assert inst.castor_knob_max == fix16.Fix16(1.01)
    assert inst.pollux_knob_min == fix16.Fix16(-1.01)
    assert inst.pollux_knob_max == fix16.Fix16(1.01)
    assert inst.chorus_max_intensity == fix16.Fix16(0.05)
    assert inst.chorus_max_frequency == fix16.Fix16(0.2)
    assert inst.knob_offset_corr == fix16.Fix16(0.0)
    assert inst.knob_gain_corr == fix16.Fix16(1.0)
    assert inst.smooth_initial_gain == fix16.Fix16(0.1)
    assert inst.smooth_sensitivity == fix16.Fix16(30.0)
    assert inst.pollux_follower_threshold == 56
    assert inst.castor_lfo_pwm is False
    assert inst.pollux_lfo_pwm is False
    assert inst.test_field == 0
