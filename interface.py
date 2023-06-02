import requests
import mysql.connector as dbConnector
import time
import tkinter as tk
from  tkinter import ttk

host = "http://localhost:5050"
#host = "http://10.100.38.87"

mydb = dbConnector.connect(
  host="sql8.freemysqlhosting.net",
  user="sql8622787",
  password="YkGsqm5q7T",
  database="sql8622787"
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
        global timestamp_value
        global value_value
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
valuesTable = tk.Toplevel(root)
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

def openValuesTable():
    valuesTable_label = tk.Label(valuesTable, text="Values table", font=("Arial", 16, "bold"))
    valuesTable_label.pack(pady=10)
    valuesTable.title("Sonometer measurements") 
    valuesTable.geometry("500x500")
    valuesTable.configure(bg="#66ccff")
    valuesTable.resizable(False, False)
    result_label["text"] = "Values Table is opened."        

openValuesTable_button = tk.Button(root, text ="Show stored values", command = openValuesTable, font=("Arial", 14))
openValuesTable_button.pack(pady = 10)

set = ttk.Treeview(valuesTable)
set.pack()

set['columns']= ('id', 'TIMESTAMP','VALUE')
set.column("#0", width=0,  stretch='NO')
set.column("id",anchor='center', width=80)
set.column("TIMESTAMP",anchor='center', width=80)
set.column("VALUE",anchor='center', width=80)

set.heading("#0",text="",anchor='center')
set.heading("id",text="ID",anchor='center')
set.heading("TIMESTAMP",text="TIMEStamp",anchor='center')
set.heading("VALUE",text="Sound Level",anchor='center')

global count
count=0


data=[id, timestamp_value, value_value]
    
for record in data:
    set.insert(parent='',index='end',iid = count,text='',values=(record[0],record[1],record[2]))
    count += 1

    Input_frame = tk.Frame(valuesTable)
    Input_frame.pack()

    id = tk.Label(Input_frame,text="ID")
    id.grid(row=0,column=0)

    id_entry = tk.Entry(Input_frame)
    id_entry.grid(row=1,column=0)

    timestamp_value= tk.Label(Input_frame,text="TIMEStamp")
    timestamp_value.grid(row=0,column=1)

    timestamp_value_entry = tk.Entry(Input_frame)
    timestamp_value_entry.grid(row=1,column=1)

    value_value = tk.Label(Input_frame,text="Sound Level")
    value_value.grid(row=0,column=2)

    value_value_entry = tk.Entry(Input_frame)
    value_value_entry.grid(row=1,column=2)

    def input_record():
        global count
        id_value = id_entry.get()
        timestamp_value = timestamp_value_entry.get()
        value_value = value_value_entry.get()
        
        set.insert(parent='', index='end', iid=id_value, text='', values=(id_value, timestamp_value, value_value))
        
        id_entry.delete(0, 'end')
        timestamp_value_entry.delete(0, 'end')
        value_value_entry.delete(0, 'end')
        
    input_button = tk.Button(valuesTable, text="Input Record", command=input_record)
    input_button.pack()
    
    set.insert(parent='',index='end',iid = count,text='',values=(id_entry.get(),timestamp_value_entry.get(),value_value_entry.get()))
    count += 1

root.mainloop()
