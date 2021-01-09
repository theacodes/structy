import importlib.resources

import jinja2

_templates = {
    name[:name.rfind(".")]: jinja2.Template(
        importlib.resources.read_text("structy.templates", name),
        lstrip_blocks=True,
        keep_trailing_newline=True,
    )
    for name in importlib.resources.contents("structy.templates")
    if name.endswith(".jinja2")
}

class CTemplates:
    def render(self, struct_name, **kwargs):
        return {
            f"{struct_name}.h": _templates["c.header"].render(**kwargs),
            f"{struct_name}.c": _templates["c.source"].render(**kwargs),
        }

class PyTemplates:
    def render(self, struct_name, **kwargs):
        return {
            f"{struct_name}.py": _templates["py"].render(**kwargs),
        }

templates = {
    "c": CTemplates(),
    "py": PyTemplates(),
}

def template_for(lang):
    return templates[lang]