# main.py
import tkinter as tk
from ui import WhaleSurrogateUI
import time
import json
import os
import tkinter.messagebox  # for messagebox if needed

class WhaleSurrogateGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Whale Surrogate System")
        self.ui = WhaleSurrogateUI()

        # Tkinter variables to track firing status, nozzles, and pumps
        self.firing_status_var = tk.BooleanVar(value=self.ui.firing_status)
        self.nozzle_vars = [tk.BooleanVar(value=n) for n in self.ui.nozzles]
        self.pump_vars = [tk.BooleanVar(value=p) for p in self.ui.pumps]

        self.nozzle_circles = []
        self.pump_circles = []
        self.selections_canvas = None
        self.firing_circle_widget = None

        self.create_widgets()
        self.check_test_values()  # Continually check for new test_values.json

    def create_widgets(self):
        # Main frame with two columns (left for settings, right for status)
        main_frame = tk.Frame(self.root)
        main_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Left column (Settings and Indicators)
        left_frame = tk.Frame(main_frame)
        left_frame.pack(side=tk.LEFT, padx=5, pady=5, fill="y")

        # Title
        tk.Label(left_frame, text="Whale Surrogate System", font=("Arial", 14, "bold")).pack(pady=5)

        # Time Settings Frame
        time_frame = tk.LabelFrame(left_frame, text="Time Settings (seconds)")
        time_frame.pack(pady=5, padx=5, fill="x")
        tk.Label(time_frame, text="DELAY: FAN ON to PUMP ON").grid(row=0, column=0, padx=5, pady=2)
        self.delay_fan_to_pump = tk.Entry(time_frame, width=10)
        self.delay_fan_to_pump.insert(0, str(self.ui.delay_fan_to_pump))
        self.delay_fan_to_pump.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(time_frame, text="PERIOD: PUMP ON").grid(row=1, column=0, padx=5, pady=2)
        self.pump_period = tk.Entry(time_frame, width=10)
        self.pump_period.insert(0, str(self.ui.pump_period))
        self.pump_period.grid(row=1, column=1, padx=5, pady=2)

        tk.Label(time_frame, text="DELAY: PUMP OFF to FAN OFF").grid(row=2, column=0, padx=5, pady=2)
        self.delay_pump_to_fan = tk.Entry(time_frame, width=10)
        self.delay_pump_to_fan.insert(0, str(self.ui.delay_pump_to_fan))
        self.delay_pump_to_fan.grid(row=2, column=1, padx=5, pady=2)

        tk.Label(time_frame, text="DELAY: TIME BETWEEN BLOWS").grid(row=3, column=0, padx=5, pady=2)
        self.delay_between_blows = tk.Entry(time_frame, width=10)
        self.delay_between_blows.insert(0, str(self.ui.delay_between_blows))
        self.delay_between_blows.grid(row=3, column=1, padx=5, pady=2)

        # Status Indicators Frame
        status_frame = tk.LabelFrame(left_frame, text="Status Indicators")
        status_frame.pack(pady=5, padx=5, fill="x")

        tk.Label(status_frame, text="BATTERY LEVEL %").grid(row=0, column=0, padx=5, pady=2)
        # Show battery level as a Label
        self.battery_level_label = tk.Label(status_frame, width=10, anchor="w")
        self.battery_level_label.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(status_frame, text="COMMS STATUS").grid(row=1, column=0, padx=5, pady=2)
        # Show comms status as a Label
        self.comms_status_label = tk.Label(status_frame, width=10, anchor="w")
        self.comms_status_label.grid(row=1, column=1, padx=5, pady=2)

        tk.Label(status_frame, text="GPS STATUS").grid(row=2, column=0, padx=5, pady=2)
        # Show GPS status as a Label
        self.gps_status_label = tk.Label(status_frame, width=10, anchor="w")
        self.gps_status_label.grid(row=2, column=1, padx=5, pady=2)

        # Temperature Settings Frame
        temp_frame = tk.LabelFrame(left_frame, text="Temperature Settings (°F)")
        temp_frame.pack(pady=5, padx=5, fill="x")
        tk.Label(temp_frame, text="TEMPERATURE SETTING").grid(row=0, column=0, padx=5, pady=2)
        self.temp_setting = tk.Entry(temp_frame, width=10)
        self.temp_setting.insert(0, str(self.ui.temp_setting))
        self.temp_setting.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(temp_frame, text="TEMPERATURE MEASURED").grid(row=1, column=0, padx=5, pady=2)
        # Show measured temp as a Label
        self.temp_measured_label = tk.Label(temp_frame, width=10, anchor="w")
        self.temp_measured_label.grid(row=1, column=1, padx=5, pady=2)

        # Firing Status Frame
        firing_frame = tk.LabelFrame(left_frame, text="Firing Status")
        firing_frame.pack(pady=5, padx=5, fill="x")
        self.firing_circle_widget = tk.Canvas(firing_frame, width=30, height=30, bg="white")
        self.firing_circle_widget.pack()
        self.firing_circle_widget.create_oval(5, 5, 25, 25,
                                              fill="green" if self.ui.firing_status else "red")
        self.firing_circle_widget.bind("<Button-1>", lambda e: self.toggle_firing())

        # Right column (Status Window and Selections)
        right_frame = tk.Frame(main_frame)
        right_frame.pack(side=tk.RIGHT, padx=5, pady=5, fill="both", expand=True)

        # Status Window Frame
        status_window_frame = tk.LabelFrame(right_frame, text="Status Window")
        status_window_frame.pack(pady=5, padx=5, fill="both", expand=True)
        self.status_text = tk.Text(status_window_frame, height=10, width=30)
        self.status_text.pack(pady=5, padx=5)
        self.update_status()

        # Selections Frame (Nozzles and Pumps)
        selections_frame = tk.LabelFrame(right_frame, text="Selections")
        selections_frame.pack(pady=5, padx=5, fill="x")

        # Create labels for Nozzles and Pumps
        for i in range(3):
            tk.Label(selections_frame, text=f"Nozzle {i+1}").grid(row=0, column=i, padx=30, pady=2)
            tk.Label(selections_frame, text=f"Pump {i+1}").grid(row=1, column=i, padx=30, pady=2)

        # Canvas for Nozzles and Pumps
        self.selections_canvas = tk.Canvas(selections_frame, width=420, height=120, bg="white")
        self.selections_canvas.grid(row=2, column=0, columnspan=3, pady=5, padx=5)

        # Draw Nozzles in first row
        for i in range(3):
            x = 90 + i * 130
            circle = self.selections_canvas.create_oval(x - 10, 10, x + 10, 30,
                                                        fill="green" if self.ui.nozzles[i] else "red")
            self.nozzle_circles.append(circle)

        # Draw Pumps in second row
        for i in range(3):
            x = 90 + i * 130
            circle = self.selections_canvas.create_oval(x - 10, 50, x + 10, 70,
                                                        fill="green" if self.ui.pumps[i] else "red")
            self.pump_circles.append(circle)

        # Bind clicks to toggle circles
        for i, circle in enumerate(self.nozzle_circles):
            self.selections_canvas.tag_bind(circle, "<Button-1>",
                                            lambda e, idx=i: self.toggle_circle("nozzle", idx))
        for i, circle in enumerate(self.pump_circles):
            self.selections_canvas.tag_bind(circle, "<Button-1>",
                                            lambda e, idx=i: self.toggle_circle("pump", idx))

        # Bottom Buttons (START, STOP, MANUAL FIRE)
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=10, fill="x")
        tk.Button(button_frame, text="START", command=self.start).grid(row=0, column=0, padx=30, pady=5)
        tk.Button(button_frame, text="STOP", command=self.stop).grid(row=0, column=1, padx=30, pady=5)
        tk.Button(button_frame, text="MANUAL FIRE", command=self.manual_fire).grid(row=0, column=2, padx=30, pady=5)

        # Update Settings button
        tk.Button(left_frame, text="Update Settings", command=self.update_settings).pack(pady=5)

        # ASCII String at the bottom
        self.ascii_label = tk.Label(self.root, text=f"ASCII String: {self.ui.generate_ascii_string()}")
        self.ascii_label.pack(pady=5)

    def update_status(self):
        """Update the status window and circles with current values."""
        status = self.ui.get_status()
        self.status_text.delete(1.0, tk.END)
        for key, value in status.items():
            if isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    self.status_text.insert(tk.END, f"{sub_key}: {sub_value}\n")
            else:
                self.status_text.insert(tk.END, f"{key}: {value}\n")

        # Update dynamic indicators (Labels)
        self.battery_level_label.config(text=f"{self.ui.battery_level}%")
        self.comms_status_label.config(text=self.ui.comms_status)
        self.gps_status_label.config(text=self.ui.gps_status)
        self.temp_measured_label.config(text=f"{self.ui.temp_measured}°F")

        self.firing_status_var.set(self.ui.firing_status)

        # Update nozzle circles
        for i, circle in enumerate(self.nozzle_circles):
            self.selections_canvas.itemconfig(
                circle, fill="green" if self.ui.nozzles[i] else "red"
            )
            self.nozzle_vars[i].set(self.ui.nozzles[i])

        # Update pump circles
        for i, circle in enumerate(self.pump_circles):
            self.selections_canvas.itemconfig(
                circle, fill="green" if self.ui.pumps[i] else "red"
            )
            self.pump_vars[i].set(self.ui.pumps[i])

        # Update firing status circle
        if self.firing_circle_widget:
            self.firing_circle_widget.delete("all")
            self.firing_circle_widget.create_oval(
                5, 5, 25, 25,
                fill="green" if self.ui.firing_status else "red"
            )

        self.root.after(1000, self.update_status)  # Refresh every second

    def update_settings(self):
        """Update UI settings (time/temperature) from the text fields."""
        try:
            settings = {
                "delay_fan_to_pump": float(self.delay_fan_to_pump.get()),
                "pump_period": float(self.pump_period.get()),
                "delay_pump_to_fan": float(self.delay_pump_to_fan.get()),
                "delay_between_blows": float(self.delay_between_blows.get()),
                "temp_setting": float(self.temp_setting.get()),
            }
            self.ui.update_settings(**settings)
            self.ascii_label.config(text=f"ASCII String: {self.ui.generate_ascii_string()}")
        except ValueError:
            tk.messagebox.showerror("Invalid Input", "Please enter valid numerical values for settings.")

    def start(self):
        self.ui.start()
        self.firing_status_var.set(self.ui.firing_status)

    def stop(self):
        self.ui.stop()
        self.firing_status_var.set(self.ui.firing_status)

    def manual_fire(self):
        self.ui.manual_fire()
        self.firing_status_var.set(self.ui.firing_status)

    def toggle_circle(self, circle_type, index):
        """Toggle a nozzle or pump circle."""
        if circle_type == "nozzle":
            self.ui.toggle_nozzle(index)
            self.nozzle_vars[index].set(self.ui.nozzles[index])
        else:
            self.ui.toggle_pump(index)
            self.pump_vars[index].set(self.ui.pumps[index])
        self.ascii_label.config(text=f"ASCII String: {self.ui.generate_ascii_string()}")

    def toggle_firing(self):
        """Toggle the firing status circle."""
        self.ui.manual_fire()
        self.firing_status_var.set(self.ui.firing_status)
        self.ascii_label.config(text=f"ASCII String: {self.ui.generate_ascii_string()}")
        if self.firing_circle_widget:
            self.firing_circle_widget.delete("all")
            self.firing_circle_widget.create_oval(
                5, 5, 25, 25,
                fill="green" if self.ui.firing_status else "red"
            )

    def check_test_values(self):
        """Check if there's a test_values.json and load it if present."""
        if os.path.exists("test_values.json"):
            with open("test_values.json", "r") as f:
                test_values = json.load(f)
            # Update all relevant fields in the UI object
            self.ui.update_settings(**test_values)
            # We do NOT call self.update_settings() here (that would overwrite JSON data)
            os.remove("test_values.json")

        # Schedule the next check
        self.root.after(1000, self.check_test_values)

if __name__ == "__main__":
    root = tk.Tk()
    app = WhaleSurrogateGUI(root)
    root.mainloop()
