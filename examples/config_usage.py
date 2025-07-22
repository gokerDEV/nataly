#!/usr/bin/env python3
"""
Example showing how to configure ephemeris file paths in nataly library.
"""

import datetime
import os
from nataly import NatalChart, set_ephe_path, get_ephe_path, create_config, to_utc
from nataly.constants import ASTROLOGICAL_BODY_GROUPS, ANGLES_SYMBOLS, SIGNS

# === USER MUST SET THIS ===
# Path to directory containing Swiss Ephemeris .se1 files (e.g. seas_18.se1, sepl_18.se1, ...)
ephe_path = "/Users/goker/codes/nataly/ephe"  # <-- SET THIS TO YOUR EPHEMERIS DIRECTORY

# Check ephemeris directory and files
required_files = [
    "seas_18.se1", "sepl_18.se1", "semo_18.se1", "seplm18.se1", "semom18.se1"
]
if not os.path.isdir(ephe_path):
    raise RuntimeError(f"Ephemeris directory not found: {ephe_path}")
missing = [f for f in required_files if not os.path.isfile(os.path.join(ephe_path, f))]
if missing:
    raise RuntimeError(f"Missing ephemeris files in {ephe_path}: {missing}\nPlease download from https://www.astro.com/ftp/swisseph/ephe/")

def example_global_config():
    print("=== Global Configuration Example ===")
    set_ephe_path(ephe_path)
    current_path = get_ephe_path()
    print(f"Current ephemeris path: {current_path}")
    dob = '1990-02-27 09:15'
    tz_offset = '+02:00'
    birth_dt = to_utc(dob, tz_offset)
    chart = NatalChart(
        person_name="Joe Doe",
        dt_utc=birth_dt,
        lat=38.4192,  # Izmir, Turkey
        lon=27.1287,
        ephe_path=ephe_path
    )
    print(f"Chart created successfully using ephemeris path: {current_path}")
    print()

def example_per_chart_config():
    print("=== Per-Chart Configuration Example ===")
    dob = '1990-02-27 09:15'
    tz_offset = '+02:00'
    birth_dt = to_utc(dob, tz_offset)
    chart = NatalChart(
        person_name="Joe Doe",
        dt_utc=birth_dt,
        lat=38.4192,  # Izmir, Turkey
        lon=27.1287,
        ephe_path=ephe_path
    )
    print("Chart created with custom ephemeris path")
    print()

def example_config_object():
    print("=== Config Object Example ===")
    config = create_config(ephe_path=ephe_path)
    is_valid = config.validate_ephe_path()
    print(f"Ephemeris path valid: {is_valid}")
    path = config.get_ephe_path()
    print(f"Ephemeris path: {path}")
    print()

if __name__ == "__main__":
    print("🔮 NATALY CONFIGURATION EXAMPLES")
    print("=" * 50)
    print("Note: These examples demonstrate the API but require actual ephemeris files to work.")
    print()
    example_global_config()
    example_per_chart_config()
    example_config_object()
    print("Configuration system allows you to:")
    print("1. Set global ephemeris path for all charts")
    print("2. Set ephemeris path per individual chart")
    print("3. Validate ephemeris file availability")
    print("4. Use default path if none specified") 