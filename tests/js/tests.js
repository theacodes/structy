/*
    Copyright (c) 2021 Alethea Katherine Flowers.
    Published under the standard MIT License.
    Full text available at: https://opensource.org/licenses/MIT
*/

// deno-lint-ignore-file camelcase

import { assertEquals } from "https://deno.land/std@0.83.0/testing/asserts.ts";
import Struct from "./structy.js";
import GemSettings from "./gemsettings.js";

function assertNumberEquals(a, b, frac = 2) {
  assertEquals(a.toFixed(frac), b.toFixed(frac));
}

Deno.test("Default construction", () => {
  const inst = new GemSettings();
  assertEquals(inst.adc_gain_corr, 2048);
  assertEquals(inst.adc_offset_corr, 0);
  assertEquals(inst.led_brightness, 127);
  assertNumberEquals(inst.castor_knob_min, -1.01);
  assertNumberEquals(inst.castor_knob_max, 1.01);
  assertNumberEquals(inst.pollux_knob_min, -1.01);
  assertNumberEquals(inst.pollux_knob_max, 1.01);
  assertNumberEquals(inst.chorus_max_intensity, 0.05);
  assertNumberEquals(inst.chorus_max_frequency, 0.2);
  assertNumberEquals(inst.knob_offset_corr, 0.0);
  assertNumberEquals(inst.knob_gain_corr, 1.0);
  assertNumberEquals(inst.smooth_initial_gain, 0.1);
  assertNumberEquals(inst.smooth_sensitivity, 30.0);
  assertEquals(inst.pollux_follower_threshold, 56);
  assertEquals(inst.castor_lfo_pwm, false);
  assertEquals(inst.pollux_lfo_pwm, false);
  assertEquals(inst.test_field, null);
});

Deno.test("Default parameters construction", () => {
  const inst = new GemSettings({ test_field: 42 });
  assertEquals(inst.adc_gain_corr, 2048);
  assertEquals(inst.adc_offset_corr, 0);
  assertEquals(inst.led_brightness, 127);
  assertNumberEquals(inst.castor_knob_min, -1.01);
  assertNumberEquals(inst.castor_knob_max, 1.01);
  assertNumberEquals(inst.pollux_knob_min, -1.01);
  assertNumberEquals(inst.pollux_knob_max, 1.01);
  assertNumberEquals(inst.chorus_max_intensity, 0.05);
  assertNumberEquals(inst.chorus_max_frequency, 0.2);
  assertNumberEquals(inst.knob_offset_corr, 0.0);
  assertNumberEquals(inst.knob_gain_corr, 1.0);
  assertNumberEquals(inst.smooth_initial_gain, 0.1);
  assertNumberEquals(inst.smooth_sensitivity, 30.0);
  assertEquals(inst.pollux_follower_threshold, 56);
  assertEquals(inst.castor_lfo_pwm, false);
  assertEquals(inst.pollux_lfo_pwm, false);
  assertEquals(inst.test_field, 42);
});

Deno.test("Fixed16 roundtrip", () => {
  class Fix16Struct extends Struct {
    static _pack_string = "i";
    static _fields = [
      { name: "fvalue", kind: "fix16", default: 4.2 },
    ];

    constructor(values = {}) {
      super(values);
    }
  }

  const inst = new Fix16Struct({ fvalue: 66.2 });
  assertEquals(inst.fvalue, 66.2);

  const packed = inst.pack();
  const inst2 = Fix16Struct.unpack(packed);
  assertEquals(inst2.fvalue.toFixed(1), "66.2");
});

const reference_data = Uint8Array.from([
  /* 2048 */ 0x08,
  0x00,
  /* 0 */ 0x00,
  0x00,
  /* 127 */ 0x00,
  0x7F,
  /* -1.01 */ 0xff,
  0xfe,
  0xfd,
  0x71,
  /* 1.01 */ 0x00,
  0x01,
  0x02,
  0x8f,
  /* -1.01 */ 0xff,
  0xfe,
  0xfd,
  0x71,
  /* 1.01 */ 0x00,
  0x01,
  0x02,
  0x8f,
  /* 0.05 */ 0x00,
  0x00,
  0x0c,
  0xcd,
  /* 0.2 */ 0x00,
  0x00,
  0x33,
  0x33,
  /* 0.0 */ 0x00,
  0x00,
  0x00,
  0x00,
  /* 1.0 */ 0x00,
  0x01,
  0x00,
  0x00,
  /* 0.1 */ 0x00,
  0x00,
  0x19,
  0x9a,
  /* 30.0 */ 0x00,
  0x1e,
  0x00,
  0x00,
  /* 56 */ 0x00,
  0x38,
  /* false */ 0x00,
  /* false */ 0x00,
  /* 0 */ 0x00,
  0x00,
  0x00,
  0x00,
]);

Deno.test("Pack", () => {
  const inst = new GemSettings();
  const packed = inst.pack();
  assertEquals(packed, reference_data);
});

Deno.test("Unpack", () => {
  const inst = GemSettings.unpack(reference_data);
  assertEquals(inst.adc_gain_corr, 2048);
  assertEquals(inst.adc_offset_corr, 0);
  assertEquals(inst.led_brightness, 127);
  assertNumberEquals(inst.castor_knob_min, -1.01);
  assertNumberEquals(inst.castor_knob_max, 1.01);
  assertNumberEquals(inst.pollux_knob_min, -1.01);
  assertNumberEquals(inst.pollux_knob_max, 1.01);
  assertNumberEquals(inst.chorus_max_intensity, 0.05);
  assertNumberEquals(inst.chorus_max_frequency, 0.2);
  assertNumberEquals(inst.knob_offset_corr, 0.0);
  assertNumberEquals(inst.knob_gain_corr, 1.0);
  assertNumberEquals(inst.smooth_initial_gain, 0.1);
  assertNumberEquals(inst.smooth_sensitivity, 30.0);
  assertEquals(inst.pollux_follower_threshold, 56);
  assertEquals(inst.castor_lfo_pwm, false);
  assertEquals(inst.pollux_lfo_pwm, false);
  assertEquals(inst.test_field, 0);
});
