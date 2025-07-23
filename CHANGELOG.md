# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.5] - 2024-01-XX

### Added
- **Enhanced Declination Calculations**: Accurate declination data for both celestial bodies and house cusps
  - Body declinations now use Swiss Ephemeris equatorial coordinates for precise values
  - House cusp declinations calculated using proper astrological formulas with dynamic obliquity
  - IAU 2006 formula for mean obliquity based on Julian centuries since J2000
  - Compatible with astro.com and other professional astrological software
- **Absolute Longitude Support**: Full 360° longitude calculations for precise positioning
- **Comprehensive Chart Reports**: Enhanced reporting with all astrological data including declinations
- **New Example Scripts**: 
  - `reference_2_enhanced_report.py`: Complete natal chart report with all bodies, aspects, and declinations
  - `reference_1_test.py`: Test script for reference data validation
- **Improved Swiss Ephemeris Integration**: Better flag usage for equatorial coordinate calculations

### Fixed
- **Body Declination Accuracy**: Fixed incorrect declination values by using proper Swiss Ephemeris equatorial coordinates
- **House Cusp Declination Calculation**: Implemented correct mathematical formulas for house cusp declinations
- **Ephemeris File Requirements**: Clarified ephemeris file requirements for accurate calculations

### Changed
- **Development Status**: Upgraded from Alpha to Beta status
- **Documentation**: Enhanced README with declination calculation examples and usage
- **Project Classification**: Added scientific/astronomical classifications

### Technical Details
- Body declinations now use `SEFLG_EQUATORIAL` flag for accurate Swiss Ephemeris calculations
- House cusp declinations use proper astrological formula: `declination = arcsin(sin(lat) * sin(obliquity) + cos(lat) * cos(obliquity) * cos(longitude))`
- Dynamic obliquity calculation ensures accuracy for all historical and future dates

## [0.1.3] - 2024-01-XX

### Added
- **ChartLayout Class**: Geometric chart layout extraction for visualization
- **Public API**: Enhanced public API for chart layout data
- **New Example**: Added chart layout example in basic_usage.py

## [0.1.0] - 2024-01-XX

### Added
- **Initial Release**: Complete astrological functionality
- **Natal Chart Calculations**: Swiss Ephemeris integration
- **Transit Analysis**: Transit chart calculations and aspect analysis
- **Comprehensive Data**: Planets, asteroids, lunar nodes, angles
- **Distribution Analysis**: Elements, modalities, polarities, quadrants, hemispheres
- **Aspect Calculations**: Major and minor aspects with configurable orbs
- **House Systems**: Support for Placidus and other house systems
- **Dignities**: Planetary dignities (domicile, exaltation, detriment, fall)
- **Filtering**: Advanced filtering for celestial bodies 