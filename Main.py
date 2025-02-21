# main.py
from ui import WhaleSurrogateUI
import time

def main():
    ui = WhaleSurrogateUI()
    
    print("Whale Surrogate System - Control Interface")
    print("----------------------------------------")
    
    while True:
        print("\nCurrent Status:")
        status = ui.get_status()
        for key, value in status.items():
            print(f"{key}: {value}")
        
        print("\nCommands:")
        print("1. Update Settings (e.g., delay_fan_to_pump=10, temp_setting=75)")
        print("2. Start System")
        print("3. Stop System")
        print("4. Manual Fire")
        print("5. Generate ASCII String")
        print("6. Exit")
        
        choice = input("Enter your choice (1-6): ")
        
        if choice == "1":
            settings = {}
            setting_input = input("Enter settings (e.g., delay_fan_to_pump=10, temp_setting=75): ")
            for pair in setting_input.split(","):
                if "=" in pair:
                    key, value = pair.split("=", 1)
                    try:
                        settings[key.strip()] = float(value.strip())
                    except ValueError:
                        settings[key.strip()] = value.strip()
            ui.update_settings(**settings)
        
        elif choice == "2":
            ui.start()
            print("System started!")
        
        elif choice == "3":
            ui.stop()
            print("System stopped!")
        
        elif choice == "4":
            ui.manual_fire()
            print("Manual fire toggled!")
        
        elif choice == "5":
            ascii_string = ui.generate_ascii_string()
            print(f"ASCII String: {ascii_string}")
        
        elif choice == "6":
            print("Exiting...")
            break
        
        time.sleep(1)  # Small delay to prevent overwhelming output

if __name__ == "__main__":
    main()