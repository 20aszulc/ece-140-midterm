import mysql.connector as mysql # Allows us to run SQL commands in Python
import os                       # Used to import environment data
from dotenv import load_dotenv  # Used to load data from .env file


load_dotenv('credentials.env') # Loads all details from the "credentials.env"

''' Environment Variables '''
db_host = os.environ['MYSQL_HOST']
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
#db_base = os.environ['MYSQL_DATABASE']

db = mysql.connect(
  host= db_host,
  user=db_user,
  password=db_pass,
  #base = db_base
)

cursor = db.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS Lab8;")
cursor.execute("USE Lab8")

cursor.execute("DROP table if exists objects")
cursor.execute("DROP table if exists found_objects")

cursor.execute(
    """CREATE TABLE if NOT EXISTS objects(
    id integer NOT NULL AUTO_INCREMENT primary key,
    name varchar(32),
    color_range_values varchar(32),
    size varchar(32),
    contour varchar(32),
    created_at  TIMESTAMP
    );
""")

cursor.execute(
    """CREATE TABLE if NOT EXISTS found_objects(
    id integer NOT NULL AUTO_INCREMENT primary key,
    object_name varchar(32),
    object_name_value varchar(32),
    address varchar(32)
    );
""")

cursor.execute("SHOW TABLES")
my_result = cursor.fetchall()
for x in my_result:
  print(x)

#INSERT VALUES
query = 'INSERT INTO objects(name, color_range_values, size, contour) VALUES (%s, %s, %s, %s)'
values = [('Mouse', 'BLUE', 'bartman', '10'),
         ('Toothbrush Holder', 'RED', 'vegan', '8'),
         ('Tennis Ball', 'GREEN', 'Startup', '78')
         ]
cursor.executemany(query,values)
db.commit()



print('---INSERT---')
print(cursor.rowcount, "record(s) inserted")

# BASIC SELECT
cursor.execute('SELECT * from objects ORDER BY name;')
my_result = cursor.fetchall()
print('---SELECT---')
[print(x) for x in my_result]

'''' 
# BASIC UPDATE
sql = "UPDATE students SET age = 39 WHERE name = 'Bart';"
cursor.execute(sql)
print(cursor.rowcount, "record(s) affected")
db.commit()
 
# BASIC SELECT WITH VALUE
sql = "SELECT * FROM students WHERE age > 10;"
cursor.execute(sql)
result = cursor.fetchall()
print('---SELECT---')
[print(x) for x in result]

'''