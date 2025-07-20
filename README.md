# Nataly

A comprehensive Python library for astrological chart calculations and analysis.

## Features

- **Natal Chart Calculations**: Complete birth chart calculations with Swiss Ephemeris
- **Transit Analysis**: Transit chart calculations and aspect analysis
- **Comprehensive Data**: Planets, asteroids, lunar nodes, angles, and more
- **Distribution Analysis**: Elements, modalities, polarities, quadrants, hemispheres
- **Aspect Calculations**: Major and minor aspects with configurable orbs
- **House Systems**: Support for Placidus and other house systems
- **Dignities**: Planetary dignities (domicile, exaltation, detriment, fall)
- **Filtering**: Advanced filtering for celestial bodies by type, sign, house, etc.

## Installation

You can install Nataly using pip:

```bash
pip install nataly
```

For development installation:

```bash
git clone https://github.com/gokerDEV/nataly.git
cd nataly
pip install -e .
```

## Quick Start

```python
import datetime
import pytz
from nataly import NatalChart, create_orb_config

# Create a natal chart
birth_dt = datetime.datetime(1990, 2, 27, 7, 15, tzinfo=pytz.UTC)
chart = NatalChart(
    person_name="Joe Doe",
    dt_utc=birth_dt,
    lat=38.25,  # Izmir, Turkey
    lon=27.09,
    orb_config=create_orb_config('Placidus')
)

# Get planetary positions
sun = chart.get_body_by_name("Sun")
print(f"Sun: {sun.signed_dms} in House {sun.house}")

# Get aspects
for aspect in chart.aspects:
    print(f"{aspect.body1.name} {aspect.symbol} {aspect.body2.name} (orb: {aspect.orb_str})")

# Get distributions
print("Element distribution:", chart.element_distribution)
print("Modality distribution:", chart.modality_distribution)
```

## Advanced Usage

### Filtering Celestial Bodies

```python
from nataly import BodyFilter

# Get only planets (excluding luminaries)
planets_filter = BodyFilter(
    include_planets=True,
    include_luminaries=False,
    include_asteroids=False
)
planets = chart.get_bodies(planets_filter)

# Get bodies in specific signs
fire_signs = chart.get_bodies_by_signs(["Aries", "Leo", "Sagittarius"])

# Get retrograde bodies
retrograde = chart.get_retrograde_bodies()
```

### Transit Analysis

```python
from nataly import AstroEngine

# Create transit chart
transit_dt = datetime.datetime.now(pytz.UTC)
transit_chart = NatalChart(
    person_name="Current Transit",
    dt_utc=transit_dt,
    lat=38.25,
    lon=27.09
)

# Calculate aspects between transit and natal
engine = AstroEngine()
transit_aspects = engine.get_aspects(
    transit_chart.bodies_dict, 
    chart.bodies_dict
)
```

### Custom Orb Configuration

```python
from nataly import OrbConfig

# Create custom orb configuration
custom_orbs = {
    'luminaries': {
        'Conjunction': 10.0,
        'Opposition': 10.0,
        'Trine': 8.0,
        'Square': 8.0
    },
    'planets': {
        'Conjunction': 8.0,
        'Opposition': 8.0,
        'Trine': 6.0,
        'Square': 6.0
    },
    'angles': {
        'Conjunction': 1.0,
        'Opposition': 1.0,
        'Trine': 1.0,
        'Square': 1.0
    }
}

orb_config = OrbConfig.from_dict(custom_orbs)
chart = NatalChart(
    person_name="Custom Orbs",
    dt_utc=birth_dt,
    lat=38.25,
    lon=27.09,
    orb_config=orb_config
)
```

## Examples

Check the `examples/` directory for complete examples:

- `astrological_analysis.py`: Comprehensive chart analysis with report generation
- `basic_usage.py`: Basic library usage examples

## Development

To set up the development environment:

```bash
pip install -e ".[dev]"
```

Run tests:
```bash
pytest
```

Format code:
```bash
black nataly/
```

Lint code:
```bash
flake8 nataly/
```

## Dependencies

### Required
- `swisseph>=2.10.0`: Swiss Ephemeris for planetary calculations
- `pytz>=2021.1`: Timezone handling

### Optional
- `numpy>=1.20.0`: Advanced calculations
- `pandas>=1.3.0`: Data analysis
- `matplotlib>=3.3.0`: Chart visualization
- `seaborn>=0.11.0`: Enhanced plotting

## Ephemeris Files

For accurate calculations, download Swiss Ephemeris files:

1. Go to https://www.astro.com/swisseph/swedownload_j.htm
2. Download ephemeris files (e.g., `seas_18.se1`)
3. Place files in `./nataly/ephe/` directory

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for your changes
5. Run the test suite
6. Submit a pull request

## Version History

- 0.1.0: Initial release with complete astrological functionality 