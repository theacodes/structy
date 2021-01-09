
class Kind:
    name = "unknown"
    c_type = "unknown"
    c_format = "unknown"
    py_type = "unknown"
    js_type = "unknown"
    pack = "x"

    c_includes = None

    @classmethod
    def c_value(cls, value):
        return 0 if value is None else value

    @classmethod
    def py_value(cls, value):
        return value

    @classmethod
    def c_printer(cls, field):
        return f"STRUCTY_PRINTF(\"- {field}: {cls.c_format}\\n\", inst->{field});"


class Uint8Kind(Kind):
    name = "uint8"
    c_type = "uint8_t"
    c_format = "%u"
    py_type = "int"
    js_type = ""
    pack = "B"

class Uint16Kind(Kind):
    name = "uint16"
    c_type = "uint16_t"
    c_format = "%u"
    py_type = "int"
    js_type = ""
    pack = "H"

class Uint32Kind(Kind):
    name = "uint32"
    c_type = "uint32_t"
    c_format = "%u"
    py_type = "int"
    js_type = ""
    pack = "I"

class Int8Kind(Kind):
    name = "int8"
    c_type = "int8_t"
    c_format = "%d"
    py_type = "int"
    js_type = ""
    pack = "b"

class Int16Kind(Kind):
    name = "int16"
    c_type = "int16_t"
    c_format = "%d"
    py_type = "int"
    js_type = ""
    pack = "h"

class Int32Kind(Kind):
    name = "int32"
    c_type = "int32_t"
    c_format = "%d"
    py_type = "int"
    js_type = ""
    pack = "i"

class BoolKind(Kind):
    name = "bool"
    c_type = "bool"
    c_format = "%u"
    py_type = "bool"
    js_type = ""
    pack = "?"

    @classmethod
    def c_value(cls, value):
        return "true" if value else "false"

class Fixed16Kind(Kind):
    name = "fix16"
    c_type = "fix16_t"
    c_format = "0x%08x"
    py_type = "structy.Fix16"
    js_type = ""
    pack = "i"

    c_includes = "#include \"fix16.h\""

    @classmethod
    def c_value(cls, value):
        return f"F16({value})"

    @classmethod
    def py_value(cls, value):
        return f"structy.Fix16({value})"

    @classmethod
    def c_printer(cls, field):
        return f"""\
{{
    char fix16buf[13];
    fix16_to_str(inst->{field}, fix16buf, 2);
    STRUCTY_PRINTF(\"- {field}: %s\\n\", fix16buf);
}}"""

def get_kinds():
    return {
        cls.name: cls
        for cls
        in Kind.__subclasses__()
    }
