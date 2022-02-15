from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response, FileResponse
import mysql.connector as mysql
from getSonar import *
from dotenv import load_dotenv
import os
import numpy as np
import cv2
ledOn = 0
buzzerOn = 0

load_dotenv('credentials.env')

''' Environment Variables '''
db_host = os.environ['MYSQL_HOST']
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']

def index_page(request):
   return FileResponse('C:/Users/amber/PycharmProjects/ece140lab5/Challenge1/index.html')


def buzz():
    print("recieved")
    if(0 == buzzerOn):
         startBuzz()
    else:
        stopBuzz()

def led():
    print("receved led")
    if (ledOn == 0):
        lightUpLed()
    else:
        turnOffLed()

if __name__ == '__main__':
      with Configurator() as config:

        # Create a route called home
        config.add_route('home', '/')
        # Bind the view (defined by index_page) to the route named ‘home’
        config.add_view(index_page, route_name='home')


        config.add_route('buzz','/buzz')
        config.add_view(buzz, route_name='buzz', renderer='json')

        config.add_route('led', '/led')
        config.add_view(led, route_name='led', renderer='json')

        config.add_static_view(name='/', path='./public', cache_max_age=3600)
        app = config.make_wsgi_app()

server = make_server('0.0.0.0', 6543, app)
print('Web server started on: http://0.0.0.0:6543')
server.serve_forever()
