# ui.py
import config

class WhaleSurrogateUI:
    def __init__(self):
        self.delay_fan_to_pump = config.DEFAULT_DELAY_FAN_TO_PUMP
        self.pump_period = config.DEFAULT_PUMP_PERIOD
        self.delay_pump_to_fan = config.DEFAULT_DELAY_PUMP_TO_FAN
        self.delay_between_blows = config.DEFAULT_DELAY_BETWEEN_BLOWS
        self.temp_setting = config.DEFAULT_TEMP_SETTING
        self.temp_measured = 70  # Simulated measured temperature
        self.battery_level = 100  # Percentage
        self.comms_status = "OK"
        self.gps_status = "Active"
        self.firing_status = False
        self.nozzles = [True, True, True]  # All nozzles active
        self.pumps = [True, False, True]   # Some pumps active/inactive

    def update_settings(self, **kwargs):
        """Update settings based on user input."""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def generate_ascii_string(self):
        """Generate a comma-delimited ASCII string for serial communication."""
        values = [
            str(self.delay_fan_to_pump),           # DELAY: FAN ON to PUMP ON
            str(self.pump_period),                 # PERIOD: PUMP ON
            str(self.delay_pump_to_fan),           # DELAY: PUMP OFF to FAN OFF
            str(self.delay_between_blows),         # DELAY: TIME BETWEEN BLOWS
            str(self.temp_setting),                # TEMPERATURE SETTING F
            str(self.temp_measured),               # TEMPERATURE MEASURED F
            str(int(self.firing_status)),          # FIRING STATUS (0 or 1)
            str(int(self.battery_level)),          # BATTERY LEVEL %
            self.comms_status,                     # COMMS STATUS
            self.gps_status,                       # GPS STATUS
            ",".join(str(int(n)) for n in self.nozzles),  # NOZZLES (0 or 1)
            ",".join(str(int(p)) for p in self.pumps)     # PUMPS (0 or 1)
        ]
        return ",".join(values)

    def start(self):
        """Simulate starting the system (set firing_status to True)."""
        self.firing_status = True

    def stop(self):
        """Simulate stopping the system (set firing_status to False)."""
        self.firing_status = False

    def manual_fire(self):
        """Simulate a manual fire (toggle firing_status)."""
        self.firing_status = not self.firing_status

    def get_status(self):
        """Return current status for display."""
        return {
            "Battery Level": f"{self.battery_level}%",
            "Comms Status": self.comms_status,
            "GPS Status": self.gps_status,
            "Nozzles": self.nozzles,
            "Pumps": self.pumps,
            "Firing Status": "Active" if self.firing_status else "Inactive",
            "Temperature Setting": f"{self.temp_setting}°F",
            "Temperature Measured": f"{self.temp_measured}°F",
            "Delays": {
                "Fan to Pump": self.delay_fan_to_pump,
                "Pump Period": self.pump_period,
                "Pump to Fan": self.delay_pump_to_fan,
                "Between Blows": self.delay_between_blows
            }
        }