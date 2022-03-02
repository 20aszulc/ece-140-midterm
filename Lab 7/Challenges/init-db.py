import mysql.connector as mysql # Allows us to run SQL commands in Python
import os                       # Used to import environment data
from dotenv import load_dotenv  # Used to load data from .env file

load_dotenv('credentials.env') # Loads all details from the "credentials.env"

''' Environment Variables '''
db_host = os.environ['MYSQL_HOST']
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']

db = mysql.connect(
  host= db_host,
  user=db_user,
  password=db_pass,
)

cursor = db.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS Lab7;")
cursor.execute("USE Lab7")

cursor.execute("DROP TABLE IF EXISTS car")

cursor.execute(
    """CREATE TABLE IF NOT EXISTS car(
    id integer NOT NULL AUTO_INCREMENT primary key,
    namePlate varchar(32),
    name varchar(32),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    );
""")

query = 'INSERT INTO car (namePlate, name) VALUES (%s, %s)'
values = [('Test1', 'Arizona_47.jpg'),('Test2', 'Contrast.jpg'),('Test3', 'Delaware_Plate.png') ]

cursor.executemany(query,values)
db.commit()

cursor.execute("SHOW TABLES")
my_result = cursor.fetchall()
for x in my_result:
  print(x)



print('---INSERT---')
print(cursor.rowcount, "record(s) inserted")

cursor.execute("""SELECT * FROM car""")
result = cursor.fetchall()
print('---SELECT---')
[print(x) for x in result]

# BASIC SELECT
#cursor.execute('SELECT * from students ORDER BY age;')