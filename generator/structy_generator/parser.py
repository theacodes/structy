# Copyright (c) 2021 Alethea Katherine Flowers.
# Published under the standard MIT License.
# Full text available at: https://opensource.org/licenses/MIT

import ast
import struct

import structy_generator.kinds


class StructyStruct:
    def __init__(self, name):
        self.name = name
        self.fields = []

    @property
    def pack_string(self):
        return "".join(field.kind.pack for field in self.fields)

    @property
    def packed_size(self):
        return struct.Struct(">" + self.pack_string).size

    @property
    def unique_kinds(self):
        out = {}
        for field in self.fields:
            out[field.kind] = None

        return out.keys()

    def __repr__(self):
        return f"<StructyStruct name={self.name} fields={self.fields}>"


class StructField:
    def __init__(self, name, kind, value, docstring):
        self.name = name
        self.kind = structy_generator.kinds.get_kinds()[kind]
        self.value = value
        self.docstring = docstring

    def __repr__(self):
        return f"<Field name={self.name} kind={self.kind.name} value={self.value}>"


class StructyVisitor(ast.NodeVisitor):
    def __init__(self):
        super().__init__()
        self.struct = None
        self.docstring = None

    def generic_visit(self, node):
        super().generic_visit(node)

    def visit_ClassDef(self, node):
        self.struct = StructyStruct(name=node.name)
        super().generic_visit(node)

    def visit_AnnAssign(self, node):
        self.struct.fields.append(
            StructField(
                name=node.target.id,
                kind=node.annotation.id,
                value=ast.literal_eval(node.value) if node.value is not None else None,
                docstring=self.docstring,
            )
        )
        self.docstring = None

    def visit_Expr(self, node):
        if not isinstance(node.value, ast.Str):
            return

        self.docstring = node.value.s


def parse(source):
    tree = ast.parse(source)

    visitor = StructyVisitor()
    visitor.visit(tree)
    struct_ = visitor.struct

    return struct_
