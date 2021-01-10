# Copyright (c) 2021 Alethea Katherine Flowers.
# Published under the standard MIT License.
# Full text available at: https://opensource.org/licenses/MIT

import math

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


TOLERANCE = 1e-03


def test_generated_unpack():
    inst = gemsettings.GemSettings.unpack(REF_DATA)

    assert inst.adc_gain_corr == 2048
    assert inst.adc_offset_corr == 0
    assert inst.led_brightness == 127
    assert math.isclose(inst.castor_knob_min, -1.01, rel_tol=TOLERANCE)
    assert math.isclose(inst.castor_knob_max, 1.01, rel_tol=TOLERANCE)
    assert math.isclose(inst.pollux_knob_min, -1.01, rel_tol=TOLERANCE)
    assert math.isclose(inst.pollux_knob_max, 1.01, rel_tol=TOLERANCE)
    assert math.isclose(inst.chorus_max_intensity, 0.05, rel_tol=TOLERANCE)
    assert math.isclose(inst.chorus_max_frequency, 0.2, rel_tol=TOLERANCE)
    assert math.isclose(inst.knob_offset_corr, 0.0, rel_tol=TOLERANCE)
    assert math.isclose(inst.knob_gain_corr, 1.0, rel_tol=TOLERANCE)
    assert math.isclose(inst.smooth_initial_gain, 0.1, rel_tol=TOLERANCE)
    assert math.isclose(inst.smooth_sensitivity, 30.0, rel_tol=TOLERANCE)
    assert inst.pollux_follower_threshold == 56
    assert inst.castor_lfo_pwm is False
    assert inst.pollux_lfo_pwm is False
    assert inst.test_field == 0
