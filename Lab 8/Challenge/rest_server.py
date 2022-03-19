from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
import json
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import FileResponse
import mysql.connector as mysql
from dotenv import load_dotenv
import PID
#import PID1
from geopy.geocoders import Nominatim
from datetime import datetime
import os
import cv2
import numpy as np

#make sure to install geopy

# This is used to render response through a JSON to the front-end
from pyramid.renderers import render_to_response

import mysql.connector as mysql
import os
from dotenv import load_dotenv

load_dotenv() # Loads all details from the "credentials.env"


''' Environment Variables '''
db_host = os.environ['MYSQL_HOST']
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = "Lab8"#os.environ['MYSQL_DATABASE']


def get_coordinates(name1, color_range, contour, size, longitude, latitude):
  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()
  #figure out address by importing and rundding pid controller
  address1 = PID.run_pid(name1, color_range, contour, size)
  print(address1)
  #if object is not in camera's view, then coordinates cannot be found
  if address1 == "object not in view":
    print(address1)
    return address1
  print("object was in view"+address1)
  #else we print out the coordinates and geolocation put it in the table
  #Geolocation
  #geoLoc = Nominatim(user_agent="GetLoc")
  address_actual = longitude + "," + latitude
  #locname = geoLoc.reverse(address_actual)
  # printing the address/location name
  #print("Location "+locname.address)
  #address_actual = address_actual + " at " + locname.address

  #this puts the object and its address into found objects sql table
  print(name1)
  record = 1
  value = 0
  saved_name = name1
      #if name already exists make it nameN where N is a number
  while record is not None:
    value = value + 1
    if value != 1:
      cursor.execute("Select * from found_objects where object_name= %s", (name1+str(value),))
      record = cursor.fetchone()
      saved_name =name1+str(value)
    else:
      cursor.execute("Select * from found_objects where object_name = %s", (name1,))
      record = cursor.fetchone()
    
    print("value"+str(value))
    db.commit()
    print(record)
  print("out of loop")
  query = 'INSERT INTO found_objects(object_name, object_name_value, address) VALUES (%s, %s, %s)'
  values = (saved_name, value, address_actual)
  cursor.execute(query, values)
  db.commit()



  #this returns the coordinates of object to be shown on index
  return address_actual

''' Instance Route to GET object rank '''
def object_rank(req):
  # Retrieve the route argument (this is not GET/POST data!)
  the_id = req.matchdict['object_rank_id']
  #get longitude and latitude
  longitude = str(req.matchdict.get('longitude_id', None))
  latitude = str(req.matchdict.get('latitude_id', None))
  print("This is longitude: ")
  print(longitude+","+latitude)

  # Connect to the database and retrieve the object
  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()
  cursor.execute("select * from objects where id='%s';" % the_id)
  record = cursor.fetchone()
  db.close()
  if record is None:
    return ""
  else:
    coordinates = get_coordinates(str(record[1]), str(record[2]), str(record[3]), str(record[4]), longitude, latitude)
  print("The coordinates")
  print(coordinates)
  # Format the result as key-value pairs
  response = {
	'id':     	record[0],
	'name':   	record[1],
	'color_range':  	record[2],
	'contour':   record[3],
	'size':    	record[4],
    'coordinates': coordinates
  }
  return response

''' Collection Route to show the location of object list '''
def store_location(req):
  db = mysql.connect(host=db_host, database=db_name, user=db_user, passwd=db_pass)
  cursor = db.cursor()

  #retrieve info to post on website and in console
  cursor.execute('SELECT * from found_objects ORDER BY id;')
  my_result = cursor.fetchall()
  records = "---This is the found_objects table\'s contents---<br>"
  print('---This is the found_objects table\'s contents---<br>') #post found_objects info in console
  [print(x) for x in my_result]
  for x in my_result:
    records = records + str(x) + "<br>"

  return records

def get_home(req):
  return FileResponse('./Challenge/index.html')


''' Route Configurations '''
if __name__ == '__main__':
  with Configurator() as config:

 	# to use Jinja2 to render the template! 
    #config.include('pyramid_jinja2')
    #config.add_jinja2_renderer('.html')


    # Home route
    config.add_route('get_home', '/')
    config.add_view(get_home, route_name='get_home')


    config.add_route('store_location', '/store_location')
    config.add_view(store_location, route_name='store_location', renderer='json')

    config.add_route('object_rank', '/object_rank/{object_rank_id}/{longitude_id}/{latitude_id}')
    config.add_view(object_rank, route_name='object_rank', renderer='json')

 	# For our static assets!
    config.add_static_view(name='/', path='./public', cache_max_age=3600)

    app = config.make_wsgi_app()

  server = make_server('0.0.0.0', 6543, app)
  print('Web server started on: http://0.0.0.0:6543')
  server.serve_forever()

