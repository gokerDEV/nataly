"""Parity and packaging tests for the bundled Swiss Ephemeris extension."""

from importlib import metadata

import pytest

from nataly import _swisseph as swe

JULIAN_DAY = 2447949.8020833335
LATITUDE = 38.4237
LONGITUDE = 27.1428


def test_pyswisseph_is_not_a_runtime_dependency() -> None:
    requirements = metadata.requires("nataly") or []
    assert not any("pyswisseph" in requirement.lower() for requirement in requirements)


def test_native_version_is_exposed() -> None:
    assert swe.version.startswith("2.10.03")
    assert swe.__version__ == swe.version


def test_julday_matches_reference_value() -> None:
    actual = swe.julday(1990, 2, 27, 7.25)
    assert actual == pytest.approx(JULIAN_DAY, abs=1e-12)


@pytest.mark.parametrize(
    ("body", "expected_longitude", "expected_speed"),
    [
        (swe.SUN, 338.4340823024853, 1.0050412975966168),
        (swe.MOON, 4.220157127074975, 14.529460956449936),
        (swe.MERCURY, 322.6927683726705, 1.617059758309322),
        (swe.PLUTO, 227.76815017184703, -0.004819174970981032),
        (swe.TRUE_NODE, 316.38730113138917, -0.053233658414602085),
    ],
)
def test_calc_ut_matches_reference_values(
    body: int,
    expected_longitude: float,
    expected_speed: float,
) -> None:
    values, return_flags = swe.calc_ut(
        JULIAN_DAY,
        body,
        swe.FLG_MOSEPH | swe.FLG_SPEED,
    )

    assert len(values) == 6
    assert values[0] == pytest.approx(expected_longitude, abs=1e-10)
    assert values[3] == pytest.approx(expected_speed, abs=1e-10)
    assert return_flags & swe.FLG_SPEED


def test_equatorial_calculation_returns_declination() -> None:
    values, return_flags = swe.calc_ut(
        JULIAN_DAY,
        swe.SUN,
        swe.FLG_MOSEPH | swe.FLG_SPEED | swe.FLG_EQUATORIAL,
    )

    assert values[1] == pytest.approx(-8.40842364215144, abs=1e-10)
    assert return_flags & swe.FLG_EQUATORIAL


def test_houses_matches_pyswisseph_compatible_shape_and_values() -> None:
    cusps, ascmc = swe.houses(
        JULIAN_DAY,
        LATITUDE,
        LONGITUDE,
        b"P",
    )

    assert len(cusps) == 12
    assert len(ascmc) == 8
    assert cusps[0] == pytest.approx(36.10403346817058, abs=1e-10)
    assert cusps[9] == pytest.approx(291.0516462479352, abs=1e-10)
    assert ascmc[swe.ASC] == pytest.approx(36.10403346817058, abs=1e-10)
    assert ascmc[swe.MC] == pytest.approx(291.0516462479352, abs=1e-10)


def test_houses_rejects_invalid_house_system() -> None:
    with pytest.raises(ValueError, match="exactly one byte"):
        swe.houses(JULIAN_DAY, LATITUDE, LONGITUDE, b"PP")
