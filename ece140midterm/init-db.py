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
cursor.execute("DROP TABLE IF EXISTS Raspberry_Pi;")
 
try:
  cursor.execute("""
    CREATE TABLE IF NOT EXISTS Raspberry_Pi (
      id          integer  AUTO_INCREMENT PRIMARY KEY,
      motion_sensor        VARCHAR(50) NOT NULL,
      second_sensor       VARCHAR(50) NOT NULL,
      created_at  TIMESTAMP
    );
  """)

   #INSERT VALUES
  cursor.executemany(query,values)
  db.commit()
except RuntimeError as err:
  print("runtime error: {0}".format(err))

# BASIC SELECT WITH VALUE
sql = "SELECT * FROM Midterm;"
cursor.execute(sql)
result = cursor.fetchall()
print('---SELECT---')
[print(x) for x in result]