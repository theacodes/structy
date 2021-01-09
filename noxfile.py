from glob import glob

import nox


@nox.session
def format(session):
    session.install("black==20.8b1")
    session.run("black", "noxfile.py", "runtimes/py", "tests/py", "generator")


@nox.session
def pytests(session):
    session.install("./generator", "pytest", "flake8==3.8.4", "mypy==0.790")
    session.run(
        "structy", "-l", "py", "tests/resources/gemsettings.structy", "tests/py"
    )
    session.run("mypy", "runtimes/py", "tests/py")
    session.run("flake8", "runtimes/py", "tests/py")
    session.run("pytest", "tests/py")


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
    session.run(
        "gcc",
        "-Werror",
        "-Wall",
        "-Wpedantic",
        "-Wextra",
        "-Wundef",
        "-Wsign-conversion",
        "-Wswitch-default",
        "-Wcast-align",
        "-Winit-self",
        "-Wdouble-promotion",
        "-std=c17",
        # "-g",
        "-O2",
        "-isystem pthird_party/munit",
        "-Ithird_party/munit",
        "-Iruntimes/c",
        "-Itests/c",
        "third_party/munit/munit.c",
        *runtime_sources,
        *test_sources,
        "-o",
        f"{session.bin}/ctests",
        external=True,
    )
    session.run("ctests")
