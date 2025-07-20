#!/usr/bin/env python3
"""
Example showing how to configure ephemeris file paths in nataly library.
"""

import datetime
import pytz
from nataly import NatalChart, set_ephe_path, get_ephe_path, create_config

def example_global_config():
    """Example using global configuration."""
    print("=== Global Configuration Example ===")
    
    # Set global ephemeris path
    set_ephe_path("/path/to/your/ephemeris/files")
    
    # Get current path
    current_path = get_ephe_path()
    print(f"Current ephemeris path: {current_path}")
    
    # Create chart (will use global config)
    birth_dt = datetime.datetime(1990, 2, 27, 9, 15, tzinfo=pytz.UTC)
    chart = NatalChart(
        person_name="Joe Doe",
        dt_utc=birth_dt,
        lat=38.4192,  # Izmir, Turkey
        lon=27.1287
    )
    
    print(f"Chart created successfully using ephemeris path: {current_path}")
    print()

def example_per_chart_config():
    """Example using per-chart configuration."""
    print("=== Per-Chart Configuration Example ===")
    
    birth_dt = datetime.datetime(1990, 2, 27, 9, 15, tzinfo=pytz.UTC)
    
    # Create chart with specific ephemeris path
    chart = NatalChart(
        person_name="Joe Doe",
        dt_utc=birth_dt,
        lat=38.4192,  # Izmir, Turkey
        lon=27.1287,
        ephe_path="/custom/path/to/ephemeris"
    )
    
    print("Chart created with custom ephemeris path")
    print()

def example_config_object():
    """Example using NatalyConfig object."""
    print("=== Config Object Example ===")
    
    # Create a configuration object
    config = create_config(ephe_path="/another/path/to/ephemeris")
    
    # Validate the path
    is_valid = config.validate_ephe_path()
    print(f"Ephemeris path valid: {is_valid}")
    
    # Get the path
    path = config.get_ephe_path()
    print(f"Ephemeris path: {path}")
    print()

if __name__ == "__main__":
    print("🔮 NATALY CONFIGURATION EXAMPLES")
    print("=" * 50)
    
    # Note: These examples show the API but won't work without actual ephemeris files
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