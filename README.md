# Structy

Structy is an irresponsibly dumb and simple struct serialization/deserialization library for C, Python, and vanilla JavaScript. You can think of it like protobuf, thrift, flatbuffers, etc. but imagine that instead of a team of engineers maintaining it, it's instead written by a single moron.

Structy was created to exchange data between C-based firmware on embedded devices and Python- and JavaScript-based programming, test, and calibration scripts running on a big-girl computer. As such, it's C implementation is designed specifically for embedded devices: it doesn't do any dynamic allocation and it doesn't have any fancy code for optimizations.

Structy's design goals:

> Be small, be simple, be useful

Explicit non-goals:

> Be fast, be clever

If you want something far more thought out and comprehensive I'd suggest checking out things like [Kaitai Struct](https://kaitai.io/).

## Using structy

Like protobuf and other complicated data exchange libraries, structy uses a *schema*. Structy's schemas use Python's syntax (so it can be lazy and re-use Python's parser):

```python
class UserSettings:
    brightness : uint8 = 127
    dark_mode: bool = False
    user_id : uint32
```

With this nonsense you can run structy's generator to generate C, JavaScript, and Python code for this "struct".

```bash
$ python3 -m pip install structy
$ structy user_settings.schema --c generated
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

Structy's Python implementation is written to be simple, not fast or "powerful" or whatever. Some notes:

- The runtime depends on Python 3.7+
- The runtime has complete type annotations.
- The runtime supports converting floats between libfixmath's fix16 during packing & unpacking.
- It's built on top of Python's excellent [struct](https://docs.python.org/3/library/struct.html) module.

### Including Structy's runtime

The runtime can be installed by installing the `structy` package:

```bash
$ python3 -m pip install structy
```


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

Since a Structy Struct is just a dataclass, it uses the [dataclass \_\_str__ and \_\_repr__](https://docs.python.org/3/reference/datamodel.html#object.__repr__).


## JavaScript implementation

Structy's JavaScript implementation, like the others, is intended to be simple. Here's some notes on it:

- It's implemented as a [JavaScript module](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules).
- It's meant to be used in a web browser. It also works with [Deno](https://deno.land/), but I only use Deno for testing.
- It's implemented using [Javascript classes](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Classes) and uses *public static members* which means [Safari will probably be a dick about it](https://bugs.webkit.org/show_bug.cgi?id=194095) until like Safari 14.1 or 15, who the heck knows?


### Including Structy's runtime

The runtime is a single file located at [runtimes/js/structy.js](runtimes/js/structy.js). There's no Node/npm package because the last time I used npm my nose suddenly starting bleeding and I passed out and woke up with several mysterious lesions, and the last time I used Node.js I managed to somehow unleash a 10,000 year-old minor demon who's currently causing minor chaos by removing stop signs in low-traffic rural areas.

So just copy it into your project next to wherever you're going to place the generated code, like we did when the web was young. If you're lazy (and you probably are), just run this:

```bash
$ wget https://raw.githubusercontent.com/theacodes/structy/runtimes/js/structy.js
$ wget https://raw.githubusercontent.com/theacodes/structy/third_party/struct.js/struct.mjs
```

Those commands also copy in the one dependency: the excellent and tiny [struct.js](https://github.com/lyngklip/structjs) module- yes, I know it's confusing to have `structy.js` and `stuct.js`, but get over it. `struct.js` implements Python [struct](https://docs.python.org/3/library/struct.html) module in JavaScript which is great because I can write less code.

### Using generated code

The Structy generates the struct as a nice class in its own module. The module's only export is the class, so you can import it like this:

```html
<script type="module">
import StructName from "./structname.js";
</script>
```


### Initialization

```js
// Default values.
inst = new StructName();
// Override a default value by passing in an object
inst = new StructName({field_name: something});
```

It's a JavaScript class so just use `new` to make an instance. It uses the pattern of passing in an object with field values so you can update fields without needing to specify all of them.

### Pack

```python
result = inst.pack();
```

Packs an instance and returns a [Uint8Array](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/Uint8Array) object with the data. `result.length()` will be `StructName.packed_size`.

### Unpack

```python
inst = StructName.unpack(data);
```

Unpacks the `Uint8Array` or `ArrayBuffer` into a new instance. The buffer must be at least `StructName.packed_size` long.



## FAQ

> Does Structy support arrays/lists?

No, Struct structs must be a deterministic length when encoded.

> How about bitfields?

No yet, but it could. I'm just too lazy.

> Little-endian? Mixed-endianess?

No. Supporting anything other than big-endian would complicate the C runtime and I don't want to do that. Idk, maybe I could be talked into accepting a PR for it.

> Custom types?

No, but it's possible in the future. There's a little bit of this thought out because Struct supports Q16.16 fixed-point values.

> Nested structs?

No, but it could be added. I just haven't needed it yet.

> Why does structy use `snake_case` for properties and methods even in C and JS where it's common to use `lowerCamelCase`? 

Mostly because I want data access to be identical in all languages, but also because I deeply, deeply, hate `lowerCamelCase`. I find it hard to read.

## Support / issues / etc

Unlike some of my other open-source projects, this project was made with one user in mind: me. I made it open source in case someone else finds it useful but I am not in the business of supporting this project. If you run into issues or need help feel free to submit an issue on GitHub, however, please know that I do not feel any obligation to support this project.

## License

The Structy generator and runtime components are all published under the MIT license. See [LICENSE](LICENSE) for the full text.
