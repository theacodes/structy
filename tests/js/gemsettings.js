// Hey this file was generated by Structy on 2021-01-10 03:20:47.992372 from
// gemsettings.structy. Maybe don't edit it!

import Struct from "./structy.js";

class GemSettings extends Struct {
  static _pack_string = "HhHiiiiiiiiiiH??i";
  static _fields = [
    { name: "adc_gain_corr", kind: "uint16", default: 2048 },
    { name: "adc_offset_corr", kind: "int16", default: 0 },
    { name: "led_brightness", kind: "uint16", default: 127 },
    { name: "castor_knob_min", kind: "fix16", default: -1.01 },
    { name: "castor_knob_max", kind: "fix16", default: 1.01 },
    { name: "pollux_knob_min", kind: "fix16", default: -1.01 },
    { name: "pollux_knob_max", kind: "fix16", default: 1.01 },
    { name: "chorus_max_intensity", kind: "fix16", default: 0.05 },
    { name: "chorus_max_frequency", kind: "fix16", default: 0.2 },
    { name: "knob_offset_corr", kind: "fix16", default: 0.0 },
    { name: "knob_gain_corr", kind: "fix16", default: 1.0 },
    { name: "smooth_initial_gain", kind: "fix16", default: 0.1 },
    { name: "smooth_sensitivity", kind: "fix16", default: 30.0 },
    { name: "pollux_follower_threshold", kind: "uint16", default: 56 },
    { name: "castor_lfo_pwm", kind: "bool", default: false },
    { name: "pollux_lfo_pwm", kind: "bool", default: false },
    { name: "test_field", kind: "int32", default: null },
  ];

  static packed_size = 54;

  constructor(values = {}) {
    super(values);
  }
}

export default GemSettings;
