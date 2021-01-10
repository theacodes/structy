import { assertEquals } from "https://deno.land/std@0.83.0/testing/asserts.ts";
import GemSettings from "./gemsettings.js";

Deno.test("Default construction", () => {
  const inst = new GemSettings();
  assertEquals(inst.adc_gain_corr, 2048);
  assertEquals(inst.adc_offset_corr, 0);
  assertEquals(inst.led_brightness, 127);
  assertEquals(inst.castor_knob_min, -1.01);
  assertEquals(inst.castor_knob_max, 1.01);
  assertEquals(inst.pollux_knob_min, -1.01);
  assertEquals(inst.pollux_knob_max, 1.01);
  assertEquals(inst.chorus_max_intensity, 0.05);
  assertEquals(inst.chorus_max_frequency, 0.2);
  assertEquals(inst.knob_offset_corr, 0.0);
  assertEquals(inst.knob_gain_corr, 1.0);
  assertEquals(inst.smooth_initial_gain, 0.1);
  assertEquals(inst.smooth_sensitivity, 30.0);
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
  assertEquals(inst.castor_knob_min, -1.01);
  assertEquals(inst.castor_knob_max, 1.01);
  assertEquals(inst.pollux_knob_min, -1.01);
  assertEquals(inst.pollux_knob_max, 1.01);
  assertEquals(inst.chorus_max_intensity, 0.05);
  assertEquals(inst.chorus_max_frequency, 0.2);
  assertEquals(inst.knob_offset_corr, 0.0);
  assertEquals(inst.knob_gain_corr, 1.0);
  assertEquals(inst.smooth_initial_gain, 0.1);
  assertEquals(inst.smooth_sensitivity, 30.0);
  assertEquals(inst.pollux_follower_threshold, 56);
  assertEquals(inst.castor_lfo_pwm, false);
  assertEquals(inst.pollux_lfo_pwm, false);
  assertEquals(inst.test_field, 42);
});
