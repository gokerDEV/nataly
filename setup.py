"""Build the minimal Swiss Ephemeris extension bundled with Nataly."""

from pathlib import Path
import sys

from setuptools import Extension, setup

ROOT = Path(__file__).parent.resolve()
SWISSEPH_ROOT = ROOT / "vendor" / "swisseph" / "libswe"

SWISSEPH_SOURCES = [
    "swecl.c",
    "swedate.c",
    "swehel.c",
    "swehouse.c",
    "swejpl.c",
    "swemmoon.c",
    "swemplan.c",
    "sweph.c",
    "swephlib.c",
]

missing_sources = [
    source for source in SWISSEPH_SOURCES
    if not (SWISSEPH_ROOT / source).is_file()
]
if missing_sources:
    missing = ", ".join(missing_sources)
    raise RuntimeError(
        "Swiss Ephemeris sources are missing: "
        f"{missing}. Run `git submodule update --init --recursive` before "
        "building Nataly."
    )

extra_compile_args = []
define_macros = []
if sys.platform == "win32":
    define_macros.append(("_CRT_SECURE_NO_WARNINGS", "1"))
elif sys.platform == "darwin":
    extra_compile_args.append(
        "-Wno-error=unused-command-line-argument-hard-error-in-future"
    )

native_extension = Extension(
    "nataly._swisseph",
    sources=[
        str(ROOT / "native" / "_swisseph.c"),
        *[str(SWISSEPH_ROOT / source) for source in SWISSEPH_SOURCES],
    ],
    include_dirs=[str(SWISSEPH_ROOT)],
    define_macros=define_macros,
    extra_compile_args=extra_compile_args,
)

setup(
    ext_modules=[native_extension],
    include_package_data=True,
    package_data={"nataly": ["ephe/*.se1"]},
)
