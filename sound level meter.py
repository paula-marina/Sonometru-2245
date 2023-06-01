import requests
import mysql.connector
import time

host = "http://localhost:5050"

mydb = mysql.connector.connect(
  host="sql8.freemysqlhosting.net",
  user="sql8622787",
  password="YkGsqm5q7T",
  database="sql8622787"
)

cursor = mydb.cursor() 

sql = "SELECT * FROM masuratori_sonometru"
cursor.execute(sql)

results = cursor.fetchall()

for row in results:
    for element in row:
        print(element)

def start_measurement():
    response = requests.post(host + "/webxi/applications/SLM/start?password=xxxxxxx")
    if response.status_code == 200:
        print("Measurement started successfully.")
    else:
        print("Failed to start the measurement.")
        print(response.status_code)
    time.sleep(2)

def insert_value(timestamp_value, value_value):
    try:
        cursor = mydb.cursor()
        
        sql = "INSERT INTO masuratori_sonometru (TIMESTAMP, VALUE) VALUES (%s, %s)"
        cursor.execute(sql, (timestamp_value, value_value))
        mydb.commit()
        print(cursor.rowcount, "row(s) were inserted.")
    except mysql.connector.Error as error:
        print("Failed to insert values into the database:", error)
    

def read_values(): 
    response = requests.get(host + "/webxi/applications/SLM/outputs/laf?password=xxxxxxx")
    if response.status_code == 200:
        sound_level = response.json() / 100  
        print("Sound Level:", sound_level)
        timestamp_value = time.strftime('%Y-%m-%d %H:%M:%S')
        insert_value(timestamp_value, sound_level)
    else:
        print("Failed to read the sound level values.")
    time.sleep(2)


def stop_measurement():
    response = requests.post(host + "/webxi/applications/SLM/stop?password=xxxxxxx")
    if response.status_code == 200:
        print("Measurement stopped successfully.")
    elif response.status_code == 400:
        print("Bad Request. Status code:", response.status_code)
    elif response.status_code == 500:
        print("Internal Server Error. Status code:", response.status_code)
    else:
        print("Failed to stop the measurement. Status code:", response.status_code)
    time.sleep(2)

while True:
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