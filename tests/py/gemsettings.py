# Hey this file was generated by Structy on 2021-01-09 20:26:59.794113 from
# gemsettings.structy. Maybe don't edit it!

from dataclasses import dataclass
from typing import ClassVar

import structy
import structy.fix16


@dataclass
class GemSettings(structy.Struct):
    _PACK_STRING: ClassVar[str] = "HhHiiiiiiiiiiH??i"

    PACKED_SIZE: ClassVar[int] = 54
    """The total size of the struct once packed."""

    adc_gain_corr: int = 2048
    """The ADC's internal gain correction register."""

    adc_offset_corr: int = 0
    """The ADC's internal offset correction register."""

    led_brightness: int = 127
    """The front-plate LED brightness."""

    castor_knob_min: structy.fix16.Fix16 = structy.fix16.Fix16(-1.01)
    """Configuration for the CV knob mins and maxs in volts, defaults to -1.01 to +1.01."""

    castor_knob_max: structy.fix16.Fix16 = structy.fix16.Fix16(1.01)

    pollux_knob_min: structy.fix16.Fix16 = structy.fix16.Fix16(-1.01)

    pollux_knob_max: structy.fix16.Fix16 = structy.fix16.Fix16(1.01)

    chorus_max_intensity: structy.fix16.Fix16 = structy.fix16.Fix16(0.05)
    """Maximum amount that the chorus can impact Pollux's frequency."""

    chorus_max_frequency: structy.fix16.Fix16 = structy.fix16.Fix16(0.2)
    """Maximum frequency that the chorus can run at in hertz."""

    knob_offset_corr: structy.fix16.Fix16 = structy.fix16.Fix16(0.0)
    """Error correction for the ADC readings for the CV and PWM knobs."""

    knob_gain_corr: structy.fix16.Fix16 = structy.fix16.Fix16(1.0)

    smooth_initial_gain: structy.fix16.Fix16 = structy.fix16.Fix16(0.1)
    """Pitch input CV smoothing parameters."""

    smooth_sensitivity: structy.fix16.Fix16 = structy.fix16.Fix16(30.0)

    pollux_follower_threshold: int = 56
    """This is the "deadzone" for Pollux's pitch CV input, basically, it
           should be around 0v and it's the point where Pollux starts following
           Castor's pitch CV. By default this is 6 code points to allow some
           variance in time and temperature."""

    castor_lfo_pwm: bool = False
    """Route LFO to PWM for oscillators"""

    pollux_lfo_pwm: bool = False

    test_field: int = 0
