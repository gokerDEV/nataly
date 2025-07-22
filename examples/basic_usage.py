#!/usr/bin/env python3
"""
Basic usage example for the Nataly library.

This script demonstrates the core functionality of the Nataly library.
"""

from nataly import NatalyCore, example_function, process_data
from nataly.utils import save_to_json, load_from_json, format_timestamp
from nataly.constants import ASTROLOGICAL_BODY_GROUPS, ANGLES_SYMBOLS, SIGNS

import datetime
import os
from nataly import NatalChart, create_orb_config, to_utc

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

def main():
    """Main function demonstrating Nataly library usage."""
    print("=== Nataly Library Basic Usage Example ===\n")
    
    # 1. Basic function call
    print("1. Basic function:")
    greeting = example_function()
    print(f"   {greeting}\n")
    
    # 2. Data processing
    print("2. Data processing:")
    test_string = "Hello world from Nataly"
    test_list = [1, 2, 3, 4, 5]
    test_dict = {"name": "Nataly", "version": "0.1.0"}
    
    print(f"   String: {test_string}")
    string_info = process_data(test_string)
    print(f"   String info: {string_info}")
    
    print(f"   List: {test_list}")
    list_info = process_data(test_list)
    print(f"   List info: {list_info}")
    
    print(f"   Dict: {test_dict}")
    dict_info = process_data(test_dict)
    print(f"   Dict info: {dict_info}\n")
    
    # 3. Core functionality
    print("3. Core functionality:")
    core = NatalyCore("ExampleCore")
    print(f"   Created core instance: {core.name}")
    
    # Add some data
    core.add_data("user", "Alice")
    core.add_data("age", 30)
    core.add_data("interests", ["Python", "Data Science", "AI"])
    
    print(f"   Stored keys: {core.list_data()}")
    print(f"   User: {core.get_data('user')}")
    print(f"   Age: {core.get_data('age')}")
    print(f"   Interests: {core.get_data('interests')}\n")
    
    # 4. Utility functions
    print("4. Utility functions:")
    timestamp = format_timestamp()
    print(f"   Current timestamp: {timestamp}")
    
    # 5. JSON operations
    print("5. JSON operations:")
    data_to_save = {
        "core_name": core.name,
        "user_data": {
            "user": core.get_data("user"),
            "age": core.get_data("age"),
            "interests": core.get_data("interests")
        },
        "timestamp": timestamp
    }
    
    # Save data to JSON
    json_file = "nataly_example_data.json"
    if save_to_json(data_to_save, json_file):
        print(f"   Data saved to {json_file}")
        
        # Load data back
        loaded_data = load_from_json(json_file)
        if loaded_data:
            print(f"   Data loaded successfully")
            print(f"   Core name: {loaded_data['core_name']}")
            print(f"   User: {loaded_data['user_data']['user']}")
    
    print("\n=== Example completed successfully! ===")

    # 6. Natal chart layout example
    print("\n6. Natal Chart Layout Example:")
    try:
        name = "Joe Doe"
        dob = '1990-02-27 09:15'
        tz_offset = '+02:00'
        latitude = 38.4192
        longitude = 27.1287
        birth_dt_utc = to_utc(dob, tz_offset)
        chart = NatalChart(
            person_name=name,
            dt_utc=birth_dt_utc,
            lat=latitude,
            lon=longitude,
            orb_config=create_orb_config('Placidus'),
            ephe_path=ephe_path
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
    except Exception as e:
        print(f"   [Error] Could not generate chart layout: {e}")


if __name__ == "__main__":
    main() 