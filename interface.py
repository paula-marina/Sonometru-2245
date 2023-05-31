import requests
import tkinter as tk

host = "http://10.100.38.87"

def start_measurement():
    response = requests.post(host + "/webxi/applications/slm/start")
    if response.status_code == 200:
        result_label["text"] = "Measurement started successfully."
    else:
        result_label["text"] = "Failed to start the measurement."

def read_values():
    response = requests.get(host + "/webxi/applications/slm/outputs/laf")
    if response.status_code == 200:
        sound_level = response.json() / 100 
        result_label["text"] = "Sound Level: " + str(sound_level)
    else:
        result_label["text"] = "Failed to read the sound level values."

def stop_measurement():
    response = requests.post(host + "/webxi/applications/slm/stop")
    if response.status_code == 200:
        result_label["text"] = "Measurement stopped successfully."
    else:
        result_label["text"] = "Failed to stop the measurement."

def on_quit():
    root.destroy()

root = tk.Tk()
root.title("Sound Level Meter Interface")

menu_label = tk.Label(root, text="Menu:", font=("Arial", 16, "bold"))
menu_label.pack(pady=10)

start_button = tk.Button(root, text="Start Measurement", command=start_measurement, font=("Arial", 14))
start_button.pack(pady=5)

read_button = tk.Button(root, text="Read Values", command=read_values, font=("Arial", 14))
read_button.pack(pady=5)

stop_button = tk.Button(root, text="Stop Measurement", command=stop_measurement, font=("Arial", 14))
stop_button.pack(pady=5)

result_label = tk.Label(root, text="", font=("Arial", 14))
result_label.pack(pady=10)

quit_button = tk.Button(root, text="Quit", command=on_quit, font=("Arial", 14))
quit_button.pack(pady=5)


root.configure(bg="#f0f0f0")
root.geometry("300x300")
root.resizable(False, False)

root.mainloop()