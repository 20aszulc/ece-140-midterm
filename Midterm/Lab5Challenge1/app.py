from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response, FileResponse
import mysql.connector as mysql
from dotenv import load_dotenv
import os
import numpy as np
import cv2
height_id = ""
age_id = ""

load_dotenv('credentials.env')

# JSON which maps photos to ID
geisel_photos = [
 {"id":1, "img_src": "geisel-1.jpg"},
 {"id":2, "img_src": "geisel-2.jpg"},
 {"id":3, "img_src": "geisel-3.jpg"},
 {"id":4, "img_src": "geisel-4.jpg"},
 {"id":5, "img_src": "geisel-5.jpg"},
]

''' Environment Variables '''
db_host = os.environ['MYSQL_HOST']
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']


# function to access data
def get_photo(request):
   # post_id retrieves the value that is sent by the client
   # the -1 is needed because arrays are 0-indexed
   idx = int(request.matchdict['photo_id'])-1
   # we return the value at the given index from geisel_photos
   return geisel_photos[idx]

def get_price(request):
   # post_id retrieves the value that is sent by the client
   # the -1 is needed because arrays are 0-indexed
   idx = int(request.matchdict['photo_id'])-1
   img1 = cv2.imread("./public/"+geisel_photos[idx]["img_src"])
   img2 = cv2.Canny(img1, 60, 200)
   (width_img2, height) = img2.shape
   mean_img2 = np.mean(img2)
   median_img2 = np.median(img2)
   std_img2 = np.std(img2)
   price_float = mean_img2 + (median_img2 * std_img2) + width_img2
   price = int(price_float)

   return price

def index_page(request):
   return FileResponse('C:/Users/amber/PycharmProjects/ece140lab5/Challenge1/index.html')

def check_range(height_id2, age_id2):
    db = mysql.connect(host=db_host, user=db_user, passwd=db_pass, database=db_name)
    cursor = db.cursor()
    cursor.execute(
        "SELECT id,name,owner,height, age FROM Gallery_Details WHERE height>='%d' AND height <'%d' AND age>='%d' AND age <'%d';" % (
        (height_id2 - 10), height_id2, (age_id2 - 10), age_id2))
    record = cursor.fetchone()
    db.close()
    return record

def get_age_range(req):
  global age_id
  global height_id
  #get the id from the request
  age_id = req.matchdict['age_range_id']
  #connect to the database
  db = mysql.connect(host=db_host, user=db_user, passwd=db_pass, database=db_name)
  cursor = db.cursor()

  #query the database with the id
  id2 = int(age_id)+10
  if height_id is not "":
      height_id2 = int(height_id) + 10
      record = check_range(height_id2, id2)
  else:
      cursor.execute("SELECT id,name,owner,height, age FROM Gallery_Details WHERE age>='%d' AND age <'%d';" % ((id2-10), id2))
      record = cursor.fetchone()
      db.close()
  height_id = ""
  return set_record(record)

def get_height_range(req):
  global age_id
  global height_id
    #get the id from the request
  height_id = req.matchdict['height_range_id']
  #connect to the database
  db = mysql.connect(host=db_host, user=db_user, passwd=db_pass, database=db_name)
  cursor = db.cursor()

  id2 = int(height_id) + 10
  #query the database with the id
  if age_id is not "":
      age_id2 = int(age_id) + 10
      record = check_range(id2, age_id2)
  else:
      cursor.execute(
          "SELECT id,name,owner,height, age FROM Gallery_Details WHERE height>='%d' AND height <'%d';" % ((id2 - 10), id2))
      record = cursor.fetchone()
      db.close()

  age_id = ""
  return set_record(record)


def set_record(record):
  #if no record found, return error json
  if record is None:
    return {
      'id': "",
      'name' : "",
      'owner': "",
      'height': "",
      'age': ""
    }

  #populate json with values
  response = {
    'id':           record[0],
    'name':         record[1],
    'owner':        record[2],
    'height':       record[3],
    'age':          record[4]
  }

  return response



def get_home(req):
  return FileResponse("C:/Users/amber/PycharmProjects/ece140lab5/Challenge1/index.html")


if __name__ == '__main__':
      with Configurator() as config:
        # Create a route called home
        config.add_route('home', '/')
        # Bind the view (defined by index_page) to the route named ‘home’
        config.add_view(index_page, route_name='home')


        # Create a route that handles server HTTP requests at: /photos/photo_id
        config.add_route('photos', '/photos/{photo_id}')
        # Binds the function get_photo to the photos route and returns JSON
        # Note: This is a REST route because we are returning a RESOURCE!
        config.add_view(get_photo, route_name='photos', renderer='json')

        config.add_route('price', '/price/{photo_id}')
        priceMe = config.add_view(get_price, route_name='price', renderer='json')

        config.add_route('get_age_range','/age_range/{age_range_id}')
        config.add_view(get_age_range, route_name='get_age_range', renderer='json')

        config.add_route('get_height_range','/height_range/{height_range_id}')
        config.add_view(get_height_range, route_name='get_height_range', renderer='json')

        config.add_static_view(name='/', path='./public', cache_max_age=3600)
        app = config.make_wsgi_app()

server = make_server('0.0.0.0', 6543, app)
print('Web server started on: http://0.0.0.0:6543')
server.serve_forever()
