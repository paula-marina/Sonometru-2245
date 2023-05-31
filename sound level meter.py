import requests

# Define the host address of the sound level meter
host = "http://10.100.38.87"

def start_measurement():
    # Send a POST request to start the measurement
    response = requests.post(host + "/webxi/applications/slm/start")
    if response.status_code == 200:
        print("Measurement started successfully.")
    else:
        print("Failed to start the measurement.")

def read_values():
    # Send a GET request to retrieve the sound level values
    response = requests.get(host + "/webxi/applications/slm/outputs/laf")
    if response.status_code == 200:
        sound_level = response.json() / 100  # Convert the value to dB
        print("Sound Level:", sound_level)
    else:
        print("Failed to read the sound level values.")

def stop_measurement():
    # Send a POST request to stop the measurement
    response = requests.post(host + "/webxi/applications/slm/stop")
    if response.status_code == 200:
        print("Measurement stopped successfully.")
    else:
        print("Failed to stop the measurement.")

# Main application loop
while True:
    # Display menu options
    print("Menu:")
    print("1. Start Measurement")
    print("2. Read Values")
    print("3. Stop Measurement")
    print("4. Quit")

    choice = input("Enter your choice (1-4): ")
    print()

    if choice == "1":
        start_measurement()
    elif choice == "2":
        read_values()
    elif choice == "3":
        stop_measurement()
    elif choice == "4":
        break
    else:
        print("Invalid choice. Please try again.")