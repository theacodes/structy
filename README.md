# Structy

Structy is an irresponsibly dumb and simple struct serialization/deserialization library for C, Python, and vanilla JavaScript. You can think of it like protobuf, thrift, flatbuffers, etc. but imagine that instead of a team of engineers maintaining it, it's instead written by a single moron.

Structy was created to exchange data between C-based firmware on embedded devices and Python- and JavaScript-based programming, test, and calibration scripts running on a big-girl computer. As such, it's C implementation is designed specifically for embedded devices: it doesn't do any dynamic allocation and it doesn't have any fancy code for optimizations.

Structy's design goals:

> Be small, be simple, be useful

Explicit non-goals:

> Be fast, be clever

## Using structy

Like protobuf and other complicated data exchange libraries, structy uses a *schema*. Structy's schemas use Python's syntax (so it can be lazy and re-use Python's parser):

```python
class UserSettings:
    brightness : uint8 = 127
    dark_mode: bool = False
    user_id : uint32
```

With this nonsense you can run structy's "compiler" to generate C, JavaScript, and Python code for this "struct".

```bash
structy user_settings.schema --c generated
```

For C, you can import and use this struct just like a normal struct:

```c
#import "generated/user_settings.h"

struct UserSettings settings = {
    .brightness = 127,
    .dark_mode = true,
    .user_id = 6,
};
```

But it also creates the initialization (`UserSettings_initialize`), serialization (`UserSettings_pack`), and deserialization (`UserSettings_initialize`) functions needed for the struct.

## C implementation

Structy's C implementation is written specifically with microcontrollers in mind. Notably:

- The runtime is *tiny*, coming in at right at ~250 lines of code and compiles to less than 1kB of thumb code.
- **Never** uses the heap
- Uses very very little stack space
- Compiles cleanly with `-Werror -Wall -Wextra -Wpedantic -std=c17`
- It includes optional support for `libfixmath`'s `fix16_t`.


### Including Structy's runtime
You must include the files in `runtimes/c` in your project to use structy-generated c code.


### Using generated code

The Structy generates the struct definition and four functions for use with the struct:

### Initialization
```c
void StructName_init(struct StructName* inst);
```

Initializes an instance of the struct with the default values specified in the struct's schema.

### Pack
```c
struct StructyResult StructName_pack(const struct StructName* inst, uint8_t* buf);
```

Packs an instance of the struct into the given buffer. The buffer must have at least `STRUCTNAME_PACKED_SIZE` bytes. Example:

```c
uint8_t output_buffer[STRUCTNAME_PACKED_SIZE];
StructName_pack(&instance, output_buffer);
```

### Unpack

```c
struct StructyResult StructName_unpack(struct StructName* inst, const uint8_t* buf);
```

Unpacks the buffer into the given instance. The buffer must have at least `STRUCTNAME_PACKED_SIZE` bytes.

### Print

```c
void StructName_print(const struct StructName* inst);
```

Prints out the struct in a nicely formatted way, for example:

```
struct UserSettings @ 0x0B00B135
- brightness: 127
- dark_mode: 1
- user_id: 6
```

Since the runtime is designed for embedded systems, Structy doesn't hardcode `printf` here. You can override the print function used by creating a `structy_config.h` file and setting the `STRUCTY_PRINTF` macro:

```c
#include "super_cool_printf.h"

#define STRUCTY_PRINTF(...) super_cool_printf(__VA_ARGS__)
```

By default, Structy will try to use `<stdio.h>`'s `printf` if you're on a big girl computer. If you're on a 32-bit ARM system, Structy will check and see if you have [mpland's embedded-friendly printf](https://github.com/mpaland/printf) and use that if you have it. Otherwise, it'll disable printing.

## Python implementation

Structy's Python implementation is written to be simple, not fast. Some notes:

- The runtime depends on Python 3.7+
- The runtime uses type annotations heavily.
- The runtime includes a very basic implementation of `Q16.16` fixed-point math called `fix16`. It's included because I often work with `libfixmath` on microcontrollers.

### Including Structy's runtime

The runtime is included with the `structy_generator` package. It's import name is `structy`.


### Using generated code

The Structy generates the struct as a [dataclass](https://docs.python.org/3/library/dataclasses.html) in its own module.

### Initialization

```py
# Default values.
inst = StructName()
# Override default value
inst = StructName(field_name=something)
```

Since it's a dataclass, an empty constructor gives the default specified in the `.structy` definition file, but you can pass keyword arguments to override them.

### Pack

```python
result: bytes = inst.pack()
```

Packs an instance and returns a `bytes` object with the data. `len(result)` will be `StructName.PACKED_SIZE`.

### Unpack

```python
inst = StructName.unpack(data)
```

Unpacks the `bytes`-like buffer into a new instance. The buffer must be at least `StructName.PACKED_SIZE` long.

### Print

Since a Structy Struct is just a dataclass, it uses the [dataclass __str__ and __repr__](https://docs.python.org/3/reference/datamodel.html#object.__repr__).

## License

The Structy generator and runtime components are all published under the MIT license. See [LICENSE](LICENSE) for the full text.
