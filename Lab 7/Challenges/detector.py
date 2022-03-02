#detects a number plate text
import json
from wsgiref.simple_server import make_server
from cv2 import isContourConvex
from pyramid.config import Configurator
from pyramid.response import FileResponse
import mysql.connector as mysql
from dotenv import load_dotenv

from datetime import datetime
import os
import cv2
import numpy as np
from PIL import Image
import pytesseract
# JSON which maps photos to ID

load_dotenv()

 #Environment Variables
db_host = os.environ['MYSQL_HOST']
db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']

car_photos = [
 {"id":1, "img_src": "Arizona_47.jpg", "plate": "Test1"},
 {"id":2, "img_src": "Contrast.jpg", "plate": "Test2"},
 {"id":3, "img_src": "Delaware_Plate.png", "plate": "Test3"},
]



def preprocessing(img):
    # Preprocessing
    # Normalize
    #img = cv2.normalize(img,img, 50, 255, cv2.NORM_MINMAX)
    # Add a Gaussian Blur to smoothen the noise
    blur = cv2.GaussianBlur(img.copy(), (3, 3), 0)
    cv2.imwrite("Blur.png", blur)

    # Threshold the image to get a binary image
    thresh = cv2.threshold(blur, 200, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    cv2.imwrite("Threshold.png", thresh)

    # Invert the image to swap the foreground and background
    invert = 255 - thresh
    cv2.imwrite("Inverted.png", invert)

    # Dilate the image to join disconnected fragments
    kernel = np.array([[0., 1., 0.], [1., 1., 1.], [0., 1., 0.]], np.uint8)
    dilated = cv2.dilate(invert, kernel)
    cv2.imwrite("Dilated.png", dilated)

    #CONTOURS PART 2 OF THIS FUNCTION
    contours, hierarchy = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Find the largest 15 contours
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:15]


    # Find best polygon and get location
    location = None

    # Finds rectangular contour
    for contour in contours:
        peri = cv2.arcLength(contour, True)
        coord = cv2.approxPolyDP(contour, 0.05 * peri, True)
        if len(coord) == 4 and cv2.contourArea(coord) > 1500:
            print("Area of contour")
            print(cv2.contourArea(coord))
            location = coord
            break
    
    if location[3][0][0] > location[1][0][0]:
        temp = location[1][0][0]
        temp2 = location[1][0][1]
        location[1][0][0] = location[3][0][0]
        location[1][0][1] = location[3][0][1]
        location[3][0][0] = temp
        location[3][0][1] = temp2
        print("swap")
    
    '''
    print(coord)
    print(cv2.contourArea(coord))
    print("location is here")
    print(location)
    '''

    # Handle cases when no quadrilaterals are found
    if type(location) != type(None):
        print("Corners of the contour are: ", location)
    else:
        print("No quadrilaterals found")

    if type(location) != type(None):
        result = get_perspective(img, location)
        #result = cv2.rotate(result, cv2.ROTATE_90_CLOCKWISE)
        cv2.imwrite("Result.png", result)
        print("There was a result")
    print(result)
    return result



# Sudoku Specific: Transform a skewed quadrilateral
def get_perspective(img, location, height = 700, width = 700):
    pts1 = np.float32([location[0], location[3], location[1], location[2]])
    pts2 = np.float32([[0, 0], [0,height], [width,0], [width, height]])
    # Apply Perspective Transform Algorithm
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    result = cv2.warpPerspective(img, matrix, (width, height))
    return result

# Split the board into 9 individual images, 1 row 9 columns
# Append the thresholded value of each box to get the output
def split_boxes(board, input_size=100):
    print(np.shape(board))
    rows = np.vsplit(board,1)
    
    boxes = []
    for r in rows:
        cols = np.hsplit(r,7)
        for box in cols:
            bThresh = cv2.threshold(box, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
            #cv2.imshow('image',bThresh)
            #cv2.waitKey(0)
            boxes.append(bThresh)
    #cv2.destroyAllWindows()
    return boxes



#This function detects the number plate in the image and returns
# a cropped image focused on the number plate.
def detect_plate(img):
    result = preprocessing(img)
    Array = get_text(result)
    if any(Array[0]):
        return Array

    print(Array)
    print("Error: No Plate Found")
    nullArray =  [ [-1, -1], [-1, -1], [-1, -1], [-1, -1] ]
    return nullArray


#This function uses pytesseract to get text from the image
def get_text(img):
    result = img
    ans = split_boxes(result)

    try:

    # Get text from each box
        out = []
        for i in range(1):
            for j in range(7):
                # Get the text from each thresholded box
                #cv2.imshow('image',ans[7 * i + j])
                #cv2.waitKey(0)
                text = pytesseract.image_to_string(Image.fromarray(ans[7 * i + j].astype(np.uint8)),
                                                   lang='eng',
                                                   config='--psm 10 --oem 3') #-c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789 
                # Clear whitespaces in text
                text = text.replace(" ", "")
                text = text.replace("\n", "")
                text = text.replace("\x0c", " ")
                print("Text: ", text)
                print(j)
                # If no text is detected make the text element zero
                if len(text) == 0 or text == '/x0c':
                    text = '0'
                    print('yep')
            
                out.append(text)
            # Sanity check: add to out only if numbers are found
            #if ord(text[0]) >= 0 and ord(text[0]) <= 1000:
                #out[i][j] = text[0]

        plateNumber = out
        #cv2.destroyAllWindows()
        print("Car Detected.Number Plate:")
        print(plateNumber)
    except not plateNumber:
        print("No Car Detected")
        plateNumber = ['N/A']
    return plateNumber




#Read the images in grayscale.
# If you feel the images are dark, modify them with cv2.normalize

db = mysql.connect(host=db_host, user=db_user, passwd=db_pass, database=db_name)
cursor = db.cursor()

def editDataInServer(aName, aPlate):

    db = mysql.connect(host=db_host, user=db_user, passwd=db_pass, database=db_name)
    cursor = db.cursor()
    cursor.execute("""
       UPDATE car
       SET namePlate=%s
       WHERE name=%s
    """, (aPlate, aName))
    print(aPlate)
    print(aName)
    db.commit()



def get_plate(request):
    db = mysql.connect(host=db_host, user=db_user, passwd=db_pass, database=db_name)
    cursor = db.cursor()
    #gets entire line
    idx = int(request.matchdict['plate_id']) - 1

    json_object = (car_photos[idx])
    image_url = "./Lab 7/Challenges/public/images/"+json_object["img_src"]
    #print(image_url)
    #image_url = "./Lab 7/Challenges/public/images/sudoku_test.jpeg"
    img = cv2.imread(image_url, 0)

    roiArray = detect_plate(img)
    print("Plate Detected: ")
    print(''.join(roiArray))
    plateJoin = ''.join(roiArray)
    json_object["plate"] = plateJoin
    
    id = int(request.matchdict['plate_id'])
    #print("This is the id")
    #print(id)
    #print(json_object["plate"])
    editDataInServer(json_object["img_src"], plateJoin)
    
    cursor.execute(
        """SELECT id, namePlate, name, created_at 
        FROM car
         WHERE '%d'=id""" % (id))
    record = cursor.fetchone()
    print(record)
    db.close()
    # we return the value at the given index from car_photos
    return set_record(record)
    
    #return roiArray

# function to access data
def get_photo(request):
   # post_id retrieves the value that is sent by the client
   # the -1 is needed because arrays are 0-indexed
   idx = int(request.matchdict['photo_id'])-1
   print(idx)
   return car_photos[idx]

def set_record(record):
  #if no record found, return error json
  if record is None:
    return {
      'id': "error",
      'name': "",
      'licensePlate:': "",
    }

  #populate json with values
  response = {
    'id':           record[0],
    'name':         record[2],
    'licensePlate':        record[1],
  }

  return response


def index_page(request):
   return FileResponse('./Lab 7/Challenges/index.html')

# Main entrypoint
if __name__ == '__main__':
    with Configurator() as config:
        # Create a route called home
        config.add_route('home', '/')
        # Bind the view (defined by index_page) to the route named ‘home’
        config.add_view(index_page, route_name='home')

        # Create a route that handles server HTTP requests at: /photos/photo_id
        config.add_route('photos', '/photos/{photo_id}')
        # Binds the function get_photo to the photos route and returns JSON
        config.add_view(get_photo, route_name='photos', renderer='json')

        # Create a route that handles server HTTP requests at: /photos/photo_id
        config.add_route('plate', '/plate/{plate_id}')
        # Binds the function get_photo to the photos route and returns JSON
        config.add_view(get_plate, route_name='plate', renderer='json')

        config.add_static_view(name='/', path='./public', cache_max_age=3600)
        # Create an app with the configuration specified above
        app = config.make_wsgi_app()
    print("Server started on port 6543")
    server = make_server('0.0.0.0', 6543, app)  # Start the application on port 6543
    server.serve_forever()