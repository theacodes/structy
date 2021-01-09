/*
    Copyright (c) 2021 Alethea Katherine Flowers.
    Published under the standard MIT License.
    Full text available at: https://opensource.org/licenses/MIT
*/

#include "printf.h"
#include <assert.h>
#include <stdarg.h>
#include <stdio.h>

char* _buf = NULL;
size_t _buf_offset = 0;

void test_printf_set_buf(char* buf) {
    _buf = buf;
    _buf_offset = 0;
}

int test_printf(const char* format, ...) {
    assert(_buf != NULL);
    va_list va;
    va_start(va, format);
    const int ret = vsprintf(_buf + _buf_offset, format, va);
    if (ret > 0) {
        _buf_offset += (size_t)ret;
    }
    va_end(va);
    return ret;
}
