# test_script.py
import json
import time
import os

# Define two sets of test values
test_values_1 = {
    "delay_fan_to_pump": 5.0,
    "pump_period": 10.0,
    "delay_pump_to_fan": 3.0,
    "delay_between_blows": 15.0,
    "temp_setting": 72.0,
    "temp_measured": 70.0,
    "battery_level": 100,
    "comms_status": "OK",
    "gps_status": "Active",
    "firing_status": True,
    "nozzles": [True, True, True],
    "pumps": [True, False, True]
}

test_values_2 = {
    "delay_fan_to_pump": 7.5,
    "pump_period": 12.0,
    "delay_pump_to_fan": 4.0,
    "delay_between_blows": 20.0,
    "temp_setting": 75.0,
    "temp_measured": 72.0,
    "battery_level": 90,
    "comms_status": "OK",
    "gps_status": "Active",
    "firing_status": False,
    "nozzles": [False, True, False],
    "pumps": [False, True, False]
}

def send_test_values(values):
    """Write test values to a JSON file for main.py to read."""
    with open("test_values.json", "w") as f:
        json.dump(values, f)
    print(f"Test values sent to test_values.json: {values}")

if __name__ == "__main__":
    current_values = test_values_1  # Start with the first set
    while True:
        send_test_values(current_values)
        # Toggle between the two sets of values
        current_values = test_values_2 if current_values == test_values_1 else test_values_1
        time.sleep(5)  # Wait 5 seconds before sending the next set