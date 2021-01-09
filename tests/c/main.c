/*
    Copyright (c) 2021 Alethea Katherine Flowers.
    Published under the standard MIT License.
    Full text available at: https://opensource.org/licenses/MIT
*/

#pragma GCC diagnostic ignored "-Wdouble-promotion"

#include "gemsettings.h"
#include "munit.h"
#include "printf.h"
#include <assert.h>
#include <stdlib.h>

// clang-format off
const uint8_t runtime_ref_data[] = {
    0x7F,
    (uint8_t)-32,
    /* 43690 */0xAA, 0xAA,
    /* -23211 */0xA5, 0x55,
    /* 3132799674 */0xBA, 0xBA, 0xBA, 0xBA,
    /* -1094795586 */0xBE, 0xBE, 0xBE, 0xBE,
    /* 3.145 */0x40, 0x49, 0x47, 0xAE,
    0x01,
};
// clang-format on

const size_t runtime_ref_data_length = sizeof(runtime_ref_data) / sizeof(uint8_t);
const size_t runtime_ref_data_items = 8;
const char runtime_ref_pack_string[] = "BbHhIif?";

MunitResult test_runtime_pack(const MunitParameter params[], void* data) {
    (void)params;
    (void)data;

    uint8_t buf[19];
    int8_t uint8 = 0x7F;
    int8_t sint8 = -32;
    uint16_t uint16 = 43690;
    int16_t sint16 = -23211;
    uint32_t uint32 = 3132799674;
    int32_t sint32 = -1094795586;
    float floatv = 3.145f;
    bool boolv = 1;

    struct StructyResult result = structy_pack(
        runtime_ref_pack_string,
        buf,
        runtime_ref_data_length,
        uint8,
        sint8,
        uint16,
        sint16,
        uint32,
        sint32,
        floatv,
        boolv);

    munit_assert_int(result.status, ==, STRUCTY_RESULT_OKAY);
    munit_assert_size(result.count, ==, runtime_ref_data_items);
    munit_assert_memory_equal(runtime_ref_data_length, buf, runtime_ref_data);

    return MUNIT_OK;
}

MunitResult test_runtime_unpack(const MunitParameter params[], void* data) {
    (void)params;
    (void)data;

    uint8_t uint8;
    int8_t sint8;
    uint16_t uint16;
    int16_t sint16;
    uint32_t uint32;
    int32_t sint32;
    float floatv;
    bool boolv;

    struct StructyResult result = structy_unpack(
        runtime_ref_pack_string,
        runtime_ref_data,
        runtime_ref_data_length,
        &uint8,
        &sint8,
        &uint16,
        &sint16,
        &uint32,
        &sint32,
        &floatv,
        &boolv);

    munit_assert_int(result.status, ==, STRUCTY_RESULT_OKAY);
    munit_assert_size(result.count, ==, runtime_ref_data_items);
    munit_assert_uint8(uint8, ==, 127);
    munit_assert_int8(sint8, ==, -32);
    munit_assert_uint16(uint16, ==, 43690);
    munit_assert_int16(sint16, ==, -23211);
    munit_assert_uint32(uint32, ==, 3132799674);
    munit_assert_int32(sint32, ==, -1094795586);
    munit_assert_float(floatv, ==, 3.145f);
    munit_assert_true(boolv);

    return MUNIT_OK;
}

MunitResult test_generated_init(const MunitParameter params[], void* data) {
    (void)params;
    (void)data;

    struct GemSettings inst;

    GemSettings_init(&inst);

    munit_assert_uint16(inst.adc_gain_corr, ==, 2048);
    munit_assert_int16(inst.adc_offset_corr, ==, 0);
    munit_assert_uint16(inst.led_brightness, ==, 127);
    munit_assert_float(inst.castor_knob_min, ==, F16(-1.01));
    munit_assert_float(inst.castor_knob_max, ==, F16(1.01));
    munit_assert_float(inst.pollux_knob_min, ==, F16(-1.01));
    munit_assert_float(inst.pollux_knob_max, ==, F16(1.01));
    munit_assert_float(inst.chorus_max_intensity, ==, F16(0.05));
    munit_assert_float(inst.chorus_max_frequency, ==, F16(0.2));
    munit_assert_float(inst.knob_offset_corr, ==, F16(0.0));
    munit_assert_float(inst.knob_gain_corr, ==, F16(1.0));
    munit_assert_float(inst.smooth_initial_gain, ==, F16(0.1));
    munit_assert_float(inst.smooth_sensitivity, ==, F16(30.0));
    munit_assert_uint16(inst.pollux_follower_threshold, ==, 56);
    munit_assert_false(inst.castor_lfo_pwm);
    munit_assert_false(inst.pollux_lfo_pwm);
    munit_assert_int32(inst.test_field, ==, 0);

    return MUNIT_OK;
}

// clang-format off
const uint8_t generated_ref_data[] = {
    /* 2048 */0x08, 0x00,
    /* 0 */0x00, 0x00,
    /* 127 */0x00, 0x7F,
    /* -1.01 */0xff, 0xfe, 0xfd, 0x71,
    /* 1.01 */0x00, 0x01, 0x02, 0x8f,
    /* -1.01 */0xff, 0xfe, 0xfd, 0x71,
    /* 1.01 */0x00, 0x01, 0x02, 0x8f,
    /* 0.05 */0x00, 0x00, 0x0c, 0xcd,
    /* 0.2 */0x00, 0x00, 0x33, 0x33,
    /* 0.0 */0x00, 0x00, 0x00, 0x00,
    /* 1.0 */0x00, 0x01, 0x00, 0x00,
    /* 0.1 */0x00, 0x00, 0x19, 0x9a,
    /* 30.0 */0x00, 0x1e, 0x00, 0x00,
    /* 56 */0x00, 0x38,
    /* false */0x00,
    /* false */0x00,
    /* 0 */0x00, 0x00, 0x00, 0x00
};
// clang-format on

static_assert(
    sizeof(generated_ref_data) / sizeof(uint8_t) == GEMSETTINGS_PACKED_SIZE,
    "Reference data must match struct packed size.");

MunitResult test_generated_pack(const MunitParameter params[], void* data) {
    (void)params;
    (void)data;

    uint8_t buf[GEMSETTINGS_PACKED_SIZE];
    struct GemSettings inst;

    GemSettings_init(&inst);

    GemSettings_pack(&inst, buf);

    munit_assert_memory_equal(GEMSETTINGS_PACKED_SIZE, buf, generated_ref_data);

    return MUNIT_OK;
}

MunitResult test_generated_unpack(const MunitParameter params[], void* data) {
    (void)params;
    (void)data;

    struct GemSettings inst;

    GemSettings_unpack(&inst, generated_ref_data);

    munit_assert_uint16(inst.adc_gain_corr, ==, 2048);
    munit_assert_int16(inst.adc_offset_corr, ==, 0);
    munit_assert_uint16(inst.led_brightness, ==, 127);
    munit_assert_float(inst.castor_knob_min, ==, F16(-1.01));
    munit_assert_float(inst.castor_knob_max, ==, F16(1.01));
    munit_assert_float(inst.pollux_knob_min, ==, F16(-1.01));
    munit_assert_float(inst.pollux_knob_max, ==, F16(1.01));
    munit_assert_float(inst.chorus_max_intensity, ==, F16(0.05));
    munit_assert_float(inst.chorus_max_frequency, ==, F16(0.2));
    munit_assert_float(inst.knob_offset_corr, ==, F16(0.0));
    munit_assert_float(inst.knob_gain_corr, ==, F16(1.0));
    munit_assert_float(inst.smooth_initial_gain, ==, F16(0.1));
    munit_assert_float(inst.smooth_sensitivity, ==, F16(30.0));
    munit_assert_uint16(inst.pollux_follower_threshold, ==, 56);
    munit_assert_false(inst.castor_lfo_pwm);
    munit_assert_false(inst.pollux_lfo_pwm);
    munit_assert_int32(inst.test_field, ==, 0);

    return MUNIT_OK;
}

const char reference_print_output[] =
    "\
Struct GemSettings:\n\
- adc_gain_corr: 2048\n\
- adc_offset_corr: 0\n\
- led_brightness: 127\n\
- castor_knob_min: -1.01\n\
- castor_knob_max: 1.01\n\
- pollux_knob_min: -1.01\n\
- pollux_knob_max: 1.01\n\
- chorus_max_intensity: 0.05\n\
- chorus_max_frequency: 0.20\n\
- knob_offset_corr: 0.00\n\
- knob_gain_corr: 1.00\n\
- smooth_initial_gain: 0.10\n\
- smooth_sensitivity: 30.00\n\
- pollux_follower_threshold: 56\n\
- castor_lfo_pwm: 0\n\
- pollux_lfo_pwm: 0\n\
- test_field: 0\n";

MunitResult test_generated_print(const MunitParameter params[], void* data) {
    (void)params;
    (void)data;

    struct GemSettings inst;

    GemSettings_init(&inst);

    char output_buffer[2048];
    test_printf_set_buf(output_buffer);

    GemSettings_print(&inst);

    munit_assert_string_equal(output_buffer, reference_print_output);

    return MUNIT_OK;
}

static MunitTest test_suite_tests[] = {
    {
        .name = "runtime.pack",
        .test = test_runtime_pack,
    },
    {
        .name = "runtime.unpack",
        .test = test_runtime_unpack,
    },
    {
        .name = "generated.init",
        .test = test_generated_init,
    },
    {
        .name = "generated.pack",
        .test = test_generated_pack,
    },
    {
        .name = "generated.unpack",
        .test = test_generated_unpack,
    },
    {
        .name = "generated.print",
        .test = test_generated_print,
    },
    {.test = NULL},
};

static const MunitSuite test_suite = {
    .prefix = "structy.",
    .tests = test_suite_tests,
    .iterations = 1,
};

int main(int argc, char* argv[MUNIT_ARRAY_PARAM(argc + 1)]) {
    return munit_suite_main(&test_suite, (void*)"structy", argc, argv);
}
