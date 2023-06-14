import requests
import mysql.connector as dbConnector
import time
import tkinter as tk
from  tkinter import ttk

host = "http://10.100.38.87"

mydb = dbConnector.connect(
  host="sql7.freemysqlhosting.net",
  user="sql7626247",
  password="6jCzkFRkCS",
  database="sql7626247"
)

cursor = mydb.cursor()

sql= "SELECT * FROM masuratori_sonometru"
cursor.execute(sql)

results = cursor.fetchall()

for row in results:
    for element in row:
        print(element)


def start_measurement():
    response = requests.post(host + "/webxi/applications/SLM/start?password=xxxxxxx")
    if response.status_code == 200:
        result_label["text"] = "Measurement started successfully."
    else:
        result_label["text"] = "Failed to start the measurement."

def insert_value(timestamp_value, value_value):
    try:   
        sql = "INSERT INTO masuratori_sonometru (TIMESTAMP, VALUE) VALUES ('" + str(timestamp_value) + "', " + str(value_value) + ")"
        print("Query: " + sql)
        cursor.execute(sql)
        mydb.commit()
        print(cursor.rowcount, "row(s) were inserted.")
    except dbConnector.Error as error:
        print("Failed to insert values into the database:", error)
    

def read_values():
    response = requests.get(host + "/webxi/applications/SLM/outputs/laf?password=xxxxxxx")
    if response.status_code == 200:
        sound_level = response.json() / 100 
        print("Sound Level:", sound_level)
        timestamp_value = time.time()
        insert_value(timestamp_value, sound_level)
        result_label["text"] = "Sound Level: " + str(sound_level)
    else:
        result_label["text"] = "Failed to read the sound level values.", response.status_code

def delete_values():
    sql = "DELETE FROM masuratori_sonometru"
    cursor.execute(sql)
    mydb.commit()
    result_label["text"] = "Record(s) deleted."

def stop_measurement():
    response = requests.post(host + "/webxi/applications/SLM/stop?password=xxxxxxx")
    if response.status_code == 200:
        result_label["text"] = "Measurement stopped successfully."
    else:
        result_label["text"] = "Failed to stop the measurement.", response.status_code
    time.sleep(2)

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


delete_button = tk.Button(root, text="Delete Values", command=delete_values, font=("Arial", 14))
delete_button.pack(pady=5)

stop_button = tk.Button(root, text="Stop Measurement", command=stop_measurement, font=("Arial", 14))
stop_button.pack(pady=5)

result_label = tk.Label(root, text="", font=("Arial", 14))
result_label.pack(pady=10)

quit_button = tk.Button(root, text="Quit", command=on_quit, font=("Arial", 14))
quit_button.pack(pady=5)

root.configure(bg="#66ccff")
root.geometry("500x500")
root.resizable(False, False)

root.mainloop()
