from glob import glob

import nox


@nox.session
def format(session):
    session.install("black==20.8b1")
    session.run("black", "noxfile.py", "runtimes/py", "tests/py", "generator")
    session.run(
        "clang-format",
        "--verbose",
        "-i",
        *glob("runtimes/c/*.c"),
        *glob("runtimes/c/*.h"),
        *glob("tests/c/*.c"),
        *glob("runtimes/c/*.h"),
        external=True,
    )
    session.run("deno", "fmt", "tests/js", "runtimes/js", external=True)


@nox.session
def pytests(session):
    session.install(
        "./generator",
        "./runtimes/py",
        "pytest",
        "pytest-cov",
        "flake8==3.8.4",
        "mypy==0.790",
    )
    session.run(
        "structy", "-l", "py", "tests/resources/gemsettings.structy", "tests/py"
    )
    session.run("mypy", "runtimes/py", "tests/py")
    session.run("flake8", "runtimes/py", "tests/py")
    session.run(
        "pytest",
        "--cov-report",
        "term-missing",
        "--cov",
        "structy",
        "--cov",
        "tests/py",
        "tests/py",
    )


@nox.session
def ctests(session):
    runtime_headers = glob("runtimes/c/*.h")
    runtime_sources = glob("runtimes/c/*.c")
    test_headers = glob("tests/c/*.h")
    test_sources = glob("tests/c/*.c")

    session.install("./generator")
    session.run("structy", "-l", "c", "tests/resources/gemsettings.structy", "tests/c")
    session.run(
        "clang-tidy",
        *runtime_headers,
        *runtime_sources,
        *test_headers,
        *test_sources,
        "--",
        "-Ithird_party/munit",
        "-Iruntimes/c",
        external=True,
    )
    gcc_args = [
        "-Werror",
        "-Wall",
        "-Wpedantic",
        "-Wstrict-aliasing",
        "-Wextra",
        "-Wundef",
        "-Wsign-conversion",
        "-Wswitch-default",
        "-Wcast-align",
        "-Winit-self",
        "-Wdouble-promotion",
        "-std=c17",
        "-isystem pthird_party/munit",
        "-Ithird_party/munit",
        "-Iruntimes/c",
        "-Itests/c",
        "third_party/munit/munit.c",
    ]
    gcc_sources = [
        *runtime_sources,
        *test_sources,
    ]
    session.run(
        "gcc",
        *gcc_args,
        *gcc_sources,
        "-O2",
        "-o",
        f"{session.bin}/ctests",
        external=True,
    )
    session.run("ctests")


@nox.session
def jstests(session):
    session.install("./generator")
    session.run(
        "structy", "-l", "js", "tests/resources/gemsettings.structy", "tests/js"
    )
    session.chdir("tests/js")
    session.run("deno", "fmt", "--check", external=True)
    session.run("deno", "lint", "--unstable", ".", "../../runtimes/js", external=True)
    session.run(
        "deno",
        "test",
        "--unstable",
        "--import-map",
        "import_map.json",
        "tests.js",
        external=True,
    )
