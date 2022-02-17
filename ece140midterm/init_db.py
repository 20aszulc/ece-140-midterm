# create my sql database

import mysql.connector as mysql
import os
import datetime
from dotenv import load_dotenv #only required if using dotenv for creds
 
load_dotenv('credentials.env')
db_host = os.environ['MYSQL_HOST']
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
 
db = mysql.connect(user=db_user, password=db_pass, host=db_host)
cursor = db.cursor()



cursor.execute("CREATE DATABASE IF NOT EXISTS Midterm;")
cursor.execute("USE Midterm;")
db_name = 'Midterm'
cursor.execute("DROP TABLE IF EXISTS Sensor_Data;")
 
try:
  cursor.execute("""
    CREATE TABLE IF NOT EXISTS Sensor_Data (
      id          integer  AUTO_INCREMENT PRIMARY KEY,
      motion_sensor        INT NOT NULL,
      second_sensor              INT NOT NULL,
      atTime               INT
    );
  """)

except RuntimeError as err:
  print("runtime error: {0}".format(err))

query = 'INSERT INTO Sensor_Data (motion_sensor, second_sensor, atTime) VALUES (%s, %s, %s)'
values = [('3', '2', '2'),('2', '2', '4') ]

cursor.executemany(query,values)
db.commit()
# BASIC SELECT WITH VALUE
sql = "SELECT * FROM Sensor_Data;"
cursor.execute(sql)
result = cursor.fetchall()
print('---SELECT---')
[print(x) for x in result]

import random

from datetime import datetime

now = datetime.now() # current date and time

time = now.strftime("%H%M%S")

r1 = random.randint(0, 10)
print("Random number between 0 and 10 is % s" % (r1))

def sendDataToServer(distance, buttonPress, time):
    now = datetime.now()  # current date and time
    time = now.strftime("%H%M%S")
    cursor.execute("""INSERT INTO Sensor_Data (motion_sensor, second_sensor, atTime) VALUES
                   ('%d', '%d', '%d');""" %(int(distance), buttonPress, int(time)))
    db.commit()
    #print out most recent data:
    cursor.execute("""SELECT * FROM Sensor_Data WHERE id=(SELECT max(id) FROM Sensor_Data);""")
    result = cursor.fetchone()
    print('---SELECT---')
    [print(x) for x in result]

for x in range(30):
    r1 = random.randint(0, 10)
    time = now.strftime("%H%M%S")
    sendDataToServer(r1, r1, time)

