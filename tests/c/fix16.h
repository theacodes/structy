#pragma once

#include <stdint.h>
#include <stdio.h>


typedef int32_t fix16_t;
static const fix16_t fix16_one = 0x00010000;
#define F16(x) ((fix16_t)(((x) >= 0) ? ((x) * 65536.0 + 0.5) : ((x) * 65536.0 - 0.5)))

inline static void fix16_to_str(fix16_t val, char* buf, int precision) {
    sprintf(buf, "%.*f", precision, (float)val / fix16_one);
}
