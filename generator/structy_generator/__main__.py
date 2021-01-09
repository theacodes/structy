#!/usr/env/bin python3

# Copyright (c) 2021 Alethea Katherine Flowers.
# Published under the standard MIT License.
# Full text available at: https://opensource.org/licenses/MIT

import argparse
import datetime
import pathlib
import os
import os.path
import sys

import structy_generator.kinds
import structy_generator.parser
import structy_generator.templates


class StructyError(Exception):
    pass


def relativize_from_common_path(*paths):
    paths = [os.path.realpath(path) for path in paths]
    try:
        common_path = os.path.commonpath(paths)
        return [
            pathlib.Path(common_path),
            *(pathlib.Path(path).relative_to(common_path) for path in paths),
        ]
    except ValueError:
        return paths


def run(language: str, struct_file, destination_path: pathlib.Path):
    template = structy_generator.templates.template_for(language)

    if not destination_path.exists():
        if os.isatty():
            create = input(
                f"Hey, {destination_path} doesn't exist, do want me to create it? (y/n)"
            )
            if create == "y":
                destination_path.mkdir(parents=True)
            else:
                raise StructyError(
                    f"Well, fine, {destination_path} doesn't exist and you don't want me to make it so I give up."
                )

        else:
            raise StructyError(f"C'mon, {destination_path} doesn't exist!")

    if not destination_path.is_dir():
        raise StructyError(
            f"Hey, {destination_path} isn't a path. I can't put files into another file."
        )

    source_file_name = pathlib.Path(struct_file.name).name
    source_file_stem = pathlib.Path(struct_file.name).stem

    struct = structy_generator.parser.parse(struct_file.read())

    outputs = template.render(
        source_file_stem,
        date=datetime.datetime.utcnow(),
        source=source_file_name,
        source_stem=source_file_stem,
        struct=struct,
        kinds=structy_generator.kinds.get_kinds(),
    )

    for output_name, output_contents in outputs.items():
        path = destination_path / output_name
        path.write_text(output_contents)
        print(f"Generated {path}.")


def _parse_args():
    parser = argparse.ArgumentParser("structy")
    parser.add_argument("-l", "--language", default="c", choices=["c", "py", "js"])
    parser.add_argument("struct_file", type=argparse.FileType("r"))
    parser.add_argument("destination_path", type=pathlib.Path)
    return parser.parse_args()


def main():
    args = _parse_args()
    run(args.language, args.struct_file, args.destination_path)
    return 0


if __name__ == "__main__":
    sys.exit(main())
