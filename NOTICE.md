# Native dependency notice

Nataly compiles a minimal CPython extension named `nataly._swisseph`.
Astronomical calculations are performed by Swiss Ephemeris C sources vendored
under `vendor/swisseph/libswe`.

The vendored source is pinned through the `vendor/swisseph` git submodule to
`sailorfe/pysweph`, an actively maintained packaging fork based on canonical
Swiss Ephemeris 2.10.03. The canonical upstream project is
`aloistr/swisseph`.

Only the following Swiss Ephemeris functions are exposed to Python:

- `swe_julday`
- `swe_calc_ut`
- `swe_houses`
- `swe_set_ephe_path`
- `swe_close`
- `swe_version`

No `pyswisseph` wheel or runtime Python dependency is installed.
