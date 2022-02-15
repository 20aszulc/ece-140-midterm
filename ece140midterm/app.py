from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response, FileResponse
import mysql.connector as mysql
from getSonar import *
from init_db import *
from dotenv import load_dotenv
import os
import numpy as np
import cv2
ledOn = 0
buzzerOn = 0
time_id = 0
distance_id = 0

''''
load_dotenv('credentials.env')

 #Environment Variables 
db_host = os.environ['MYSQL_HOST']
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']
'''
def index_page(request):
   return FileResponse('index.html')


def buzz():
    global buzzerOn
    print("recieved")
    if(0 == buzzerOn):
         startBuzz()
    else:
        stopBuzz()

def led():
    global ledOn
    print("receved led")
    if (ledOn == 0):
        lightUpLed()
    else:
        turnOffLed()

def check_range(distance_id2, time_id2):
    db = mysql.connect(host=db_host, user=db_user, passwd=db_pass, database=db_name)
    cursor = db.cursor()
    cursor.execute(
        """"SELECT id, motion_sensor, second_sensor, atTime 
        FROM Midterm 
        WHERE time>='%d' AND time <'%d'
        AND '%d'=(SELECT COUNT(DISTINCT motion_sensor) 
                        FROM Midterm p
                        WHERE e.motion_sensor<=p.motion_sensor);""" % ((time_id2), time_id2+5, distance_id2))

    record = cursor.fetchone()
    db.close()
    return record


def get_time_rank(req):
  global time_id
  global distance_id
  #get the id from the request
  time_id = req.matchdict['time_rank_id']
  #connect to the database
  db = mysql.connect(host=db_host, user=db_user, passwd=db_pass, database=db_name)
  cursor = db.cursor()

  #query the database with the id
  id2 = int(time_id)-5
  if distance_id is not "":
      distance_id2 = int(distance_id)
      record = check_range(distance_id2, id2)
  else:
      cursor.execute( "SELECT id, motion_sensor, second_sensor, atTime FROM Midterm WHERE time>='%d' AND time <'%d';" % ((id2), id2+5))
      record = cursor.fetchone()
      db.close()
  distance_id = ""
  return set_record(record)

def get_distance_range(req):
  global time_id
  global distance_id
    #get the id from the request
  distance_id = req.matchdict['distance_range_id']
  #connect to the database
  db = mysql.connect(host=db_host, user=db_user, passwd=db_pass, database=db_name)
  cursor = db.cursor()

  id2 = int(distance_id)
  #query the database with the id
  if time_id is not "":
      time_id2 = int(time_id) - 5
      record = check_range(id2, time_id2)
  else:
      cursor.execute(
          """SELECT id, motion_sensor, second_sensor, atTime 
          FROM Midterm e
           WHERE '%d'=(SELECT COUNT(DISTINCT motion_sensor) 
                        FROM Midterm p
                        WHERE e.motion_sensor<=p.motion_sensor);""" % (id2))
      record = cursor.fetchone()
      db.close()

  time_id = ""
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
      exec("init_db.py")
      with Configurator() as config:

        # Create a route called home
        config.add_route('home', '/')
        # Bind the view (defined by index_page) to the route named ‘home’
        config.add_view(index_page, route_name='home')

        config.add_route('get_distance_range', '/distance_range/{distance_range_id}')
        config.add_view(get_distance_range, route_name='get_distance_range', renderer='json')

        config.add_route('get_time_rank', '/time_rank/{time_rank_id}')
        config.add_view(get_time_rank, route_name='get_time_rank', renderer='json')

        config.add_route('buzz','/buzz')
        config.add_view(buzz, route_name='buzz', renderer='json')

        config.add_route('led', '/led')
        config.add_view(led, route_name='led', renderer='json')

        config.add_static_view(name='/', path='./public', cache_max_age=3600)
        app = config.make_wsgi_app()

server = make_server('0.0.0.0', 6543, app)
print('Web server started on: http://0.0.0.0:6543')
server.serve_forever()
