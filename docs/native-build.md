# Native Swiss Ephemeris build

The `native` branch does not depend on the `pyswisseph` Python distribution.
It compiles `nataly._swisseph` from the Swiss Ephemeris C source included as a
git submodule.

## Clone and build

```bash
git clone --recurse-submodules https://github.com/gokerDEV/nataly.git
cd nataly
git switch native
python -m pip install -e ".[dev]"
python -m pytest
```

For an existing clone:

```bash
git submodule update --init --recursive
```

The extension preserves the subset of the legacy `pyswisseph` return shapes
that Nataly uses. In particular, `houses()` converts Swiss Ephemeris' 1-based
13-element cusp buffer to the historical 12-element Python tuple.

## Distribution

Source distributions must be created from a checkout with initialized
submodules so `vendor/swisseph/libswe` is included by `MANIFEST.in`.
Platform wheels are built with `cibuildwheel`; they contain the compiled native
extension and require no C compiler at installation time.
