from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response, FileResponse
import mysql.connector as mysql
from getSonar import *
from datetime import datetime
from dotenv import load_dotenv
import os
import numpy as np


ledOn = 0
buzzerOn = 0
time_id = ""
distance_id = ""





load_dotenv()

 #Environment Variables
db_host = os.environ['MYSQL_HOST']
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']


def index_page(request):
   return FileResponse('/home/pi/Documents/ece-140-midterm/ece140midterm/index.html')


def buzzIt(req):
    global buzzerOn
    print("recieved")
    if(0 == buzzerOn):
         startBuzz()
         buzzerOn = 1
    else:
        stopBuzz()
        buzzerOn = 0

def ledIt(req):
    global ledOn
    print("receved led")
    if (ledOn == 0):
        lightUpLed()
        ledOn=1
    else:
        turnOffLed()
        ledOn = 0


def check_range(distance_id2, time_id2):
    db = mysql.connect(host=db_host, user=db_user, passwd=db_pass, database=db_name)
    cursor = db.cursor()
    cursor.execute(
        """"SELECT id, motion_sensor, second_sensor, atTime 
        FROM Sensor_Data e
           WHERE '%d'=(SELECT COUNT(DISTINCT atTime) 
                        FROM Sensor_Data p
                        WHERE e.atTime<=p.atTime)
            AND '%d'=(SELECT COUNT(DISTINCT motion_sensor) 
                        FROM Sensor_Data p
                        WHERE e.motion_sensor<=p.motion_sensor);""" % (time_id2, distance_id2))
    record = cursor.fetchone()
    if record is None:
        cursor.execute(
            """"SELECT id, motion_sensor, second_sensor, atTime 
            FROM Sensor_Data e
               WHERE '%d'>(SELECT COUNT(DISTINCT atTime) 
                            FROM Sensor_Data p
                            WHERE e.atTime<=p.atTime)
                AND '%d' =(SELECT COUNT(DISTINCT motion_sensor) 
                            FROM Sensor_Data p
                            WHERE e.motion_sensor<=p.motion_sensor);""" % (time_id2, distance_id2))
        record = cursor.fetchone()
    db.close()
    return record

def get_time_rank(req):
  global time_id
  global distance_id
  print("time")
  db = mysql.connect(host=db_host, user=db_user, passwd=db_pass, database=db_name)
  cursor = db.cursor()
  #get the id from the request
  time_id = req.matchdict['time_rank_id']
  #query the database with the id
  id2 = int(time_id)
  if distance_id is not "":
      record = check_range(distance_id, id2)
  else:
      cursor.execute(
          """SELECT id, motion_sensor, second_sensor, atTime 
          FROM Sensor_Data e
           WHERE '%d'=(SELECT COUNT(DISTINCT atTime) 
                        FROM Sensor_Data p
                        WHERE e.atTime<=p.atTime);""" % (id2))
      record = cursor.fetchone()
  print(record)
  print("timeRecord")
  db.close()
  time_id = ""
  distance_id = ""
  return set_record(record)

def get_distance_range(req):
  global time_id
  global distance_id
  db = mysql.connect(host=db_host, user=db_user, passwd=db_pass, database=db_name)
  cursor = db.cursor()
    #get the id from the request
  distance_id = req.matchdict['distance_range_id']
  #connect to the database
  id2 = int(distance_id)
  if time_id is not "":
      record = check_range(id2, time_id)
  else: #works!!!!
      cursor.execute(
          """SELECT id, motion_sensor, second_sensor, atTime 
          FROM Sensor_Data e
           WHERE '%d'=(SELECT COUNT(DISTINCT motion_sensor) 
                        FROM Sensor_Data p
                        WHERE e.motion_sensor<=p.motion_sensor);""" % (id2))

      record = cursor.fetchone()
  db.close()

  time_id = ""
  distance_id = ""
  return set_record(record)


def set_record(record):
  #if no record found, return error json
  if record is None:
    return {
      'id': "",
      'motion_sensor': "",
      'button_press': "",
      'time': ""
    }

  #populate json with values
  response = {
    'id':           record[0],
    'motion_sensor':         record[1],
    'button_press':        record[2],
    'time':       record[3],
  }

  return response



if __name__ == '__main__':
      #exec("randomTest.py")
      with Configurator() as config:

        # Create a route called home
        config.add_route('home', '/')
        # Bind the view (defined by index_page) to the route named ‘home’
        config.add_view(index_page, route_name='home')

        config.add_route('get_distance_range', '/distance_range/{distance_range_id}')
        config.add_view(get_distance_range, route_name='get_distance_range', renderer='json')

        config.add_route('get_time_rank', '/time_rank/{time_rank_id}')
        config.add_view(get_time_rank, route_name='get_time_rank', renderer='json')

        config.add_route('buzzIt','/buzzIt/')
        config.add_view(buzzIt, route_name='buzzIt', renderer='json')

        config.add_route('ledIt', '/ledIt/')
        config.add_view(ledIt, route_name='ledIt', renderer='json')

        config.add_static_view(name='/', path='./public', cache_max_age=3600)
        app = config.make_wsgi_app()

server = make_server('0.0.0.0', 6543, app)
print('Web server started on: http://0.0.0.0:6543')
try:
  setup()
  loop()
  server.serve_forever()
except KeyboardInterrupt:
  GPIO.cleanup()