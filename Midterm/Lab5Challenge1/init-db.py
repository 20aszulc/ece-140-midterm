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



cursor.execute("CREATE DATABASE IF NOT EXISTS Triton_Gallery;")
cursor.execute("USE Triton_Gallery;")
db_name = 'Triton_Gallery'
cursor.execute("DROP TABLE IF EXISTS Gallery_Details;")
 
try:
  cursor.execute("""
    CREATE TABLE IF NOT EXISTS Gallery_Details (
      id          integer  AUTO_INCREMENT PRIMARY KEY,
      name        VARCHAR(50) NOT NULL,
      owner       VARCHAR(50) NOT NULL,
      
      height        integer NOT NULL,    
      age           integer NOT NULL,
      created_at  TIMESTAMP
    );
  """)

   #INSERT VALUES
  query = 'INSERT INTO Gallery_Details (name, owner, height, age, created_at) VALUES (%s, %s, %s, %s, %s)'
  values = [('geisel-1.jpg', 'Terrell Gilmore', '163', '45',  '2022-02-7 12:36:09'),
         ('geisel-2.jpg', 'Sila Mann', '189', '51',  '2022-02-7 12:36:09'),
         ('geisel-3.jpg', 'Nyle Hendrix', '152', '27',  '2022-02-7 12:36:09'),
         ('geisel-4.jpg', 'Axel Horton', '176', '21',  '2022-02-7 12:36:09'),
         ('geisel-5.jpg', 'Courtney Mcneil', '172', '64',  '2022-02-7 12:36:09'),
         ]
  cursor.executemany(query,values)
  db.commit()
except RuntimeError as err:
  print("runtime error: {0}".format(err))

# BASIC SELECT WITH VALUE
sql = "SELECT * FROM Gallery_Details WHERE age > 10;"
cursor.execute(sql)
result = cursor.fetchall()
print('---SELECT---')
[print(x) for x in result]