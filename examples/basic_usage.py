#!/usr/bin/env python3
"""
Basic usage example for the Nataly library.

This script demonstrates the core functionality of the Nataly library.
"""

from nataly import NatalyCore, example_function, process_data
from nataly.utils import save_to_json, load_from_json, format_timestamp
from nataly.constants import ASTROLOGICAL_BODY_GROUPS, ANGLES_SYMBOLS, SIGNS


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
        import datetime
        import pytz
        from nataly import NatalChart, ChartLayout
        # Example birth data
        birth_dt = datetime.datetime(1990, 2, 27, 9, 15, tzinfo=pytz.UTC)
        chart = NatalChart(
            person_name="Joe Doe",
            dt_utc=birth_dt,
            lat=38.4192,  # Izmir, Turkey
            lon=27.1287
        )
        layout = ChartLayout(chart)
        layout_data = layout.get_data()
        print("   Chart layout data (truncated):")
        print(f"   Center: {layout_data['center']}, Radius: {layout_data['radius']}")
        print(f"   Houses: {layout_data['natal']['houses'][:2]} ...")
        print(f"   Bodies: {layout_data['natal']['bodies'][:2]} ...")
        print(f"   Aspects: {layout_data['natal']['aspects'][:2]} ...")
    except Exception as e:
        print(f"   [Error] Could not generate chart layout: {e}")


if __name__ == "__main__":
    main() 