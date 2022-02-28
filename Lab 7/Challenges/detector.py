#detects a number plate text
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import FileResponse
import cv2
import numpy as np
# JSON which maps photos to ID
car_photos = [
 {"id":1, "img_src": "Arizona_47.jpg", "plate": "Test1"},
 {"id":2, "img_src": "Contrast.jpg", "plate": "Test2"},
 {"id":3, "img_src": "Delaware_Plate.png", "plate": "Test3"},
]

def preprocessing(img):
    # Preprocessing
    # Add a Gaussian Blur to smoothen the noise
    blur = cv2.GaussianBlur(img.copy(), (9, 9), 0)
    cv2.imwrite("Blur.png", blur)

    # Threshold the image to get a binary image
    thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    cv2.imwrite("Threshold.png", thresh)

    # Invert the image to swap the foreground and background
    invert = 255 - thresh
    cv2.imwrite("Inverted.png", invert)

    # Dilate the image to join disconnected fragments
    kernel = np.array([[0., 1., 0.], [1., 1., 1.], [0., 1., 0.]], np.uint8)
    dilated = cv2.dilate(invert, kernel)
    cv2.imwrite("Dilated.png", dilated)

    #CONTOURS PART 2 OF THIS FUNCTION
    contours, hierarchy = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Find the largest 15 contours
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:15]

    # Find best polygon and get location
    location = None

    # Finds rectangular contour
    for contour in contours:
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
        if len(approx) == 4:
            location = approx
            break

    # Handle cases when no quadrilaterals are found
    if type(location) != type(None):
        print("Corners of the contour are: ", location)
    else:
        print("No quadrilaterals found")

    if type(location) != type(None):
        result = get_perspective(img, location)
        result = cv2.rotate(result, cv2.ROTATE_90_CLOCKWISE)
        cv2.imwrite("Result.png", result)
    return result



# Sudoku Specific: Transform a skewed quadrilateral
def get_perspective(img, location, height = 900, width = 900):
    pts1 = np.float32([location[0], location[3], location[1], location[2]])
    pts2 = np.float32([[0, 0], [width, 0], [0, height], [width, height]])
    # Apply Perspective Transform Algorithm
    matrix = cv2.getPerspectiveTransform(pts1, pts2)
    result = cv2.warpPerspective(img, matrix, (width, height))
    return result

# Split the board into 9 individual images, 1 row 9 columns
# Append the thresholded value of each box to get the output
def split_boxes(board, input_size=100):
	rows = np.vsplit(board,9)
	boxes = []
	for r in rows:
        cols = np.hsplit(r,9)
    	for box in cols:
        	bThresh = cv2.threshold(box, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        	boxes.append(bThresh)
	return boxes


#This function detects the number plate in the image and returns
# a cropped image focused on the number plate.
def detect_plate(img):
    result = preprocessing(img)
    Array = get_text(result)
    if(0 != Array):
        return Array


    print("Error: No Plate Found")
    nullArray =  [ [-1, -1], [-1, -1], [-1, -1], [-1, -1] ]
    return nullArray


#This function uses pytesseract to get text from the image
def get_text(img):
    try:
        result = img;
        ans = split_boxes(result)

        # Get text from each box
        out = np.zeros((9, 9))
        for i in range(9):
            for j in range(9):
                # Get the text from each thresholded box
                text = pytesseract.image_to_string(Image.fromarray(ans[9 * i + j].astype(np.uint8)),
                                                   lang='eng',
                                                   config='--psm 10 --oem 3 -c tessedit_char_whitelist=123456789')
                # Clear whitespaces in text
                text = text.replace(" ", "")

                # If no text is detected make the text element zero
                if len(text) == 0:
                    text = '0'

                # Sanity check: add to out only if numbers are found
                if ord(text[0]) >= 48 and ord(text[0]) <= 57:
                    out[i][j] = text[0]

        plateNumber = out
        print("Car Detected.Number Plate:")
        print(plateNumber)
        return plateNumber
    except:
        print("Error: No Plate Found")
        return 0



#Read the images in grayscale.
# If you feel the images are dark, modify them with cv2.normalize

def get_plate(request):
    #gets entire line
    idx = int(request.matchdict['photo_id']) - 1
    json_object = json.loads(car_photos[idx])
    image_url = json_object["img_src"]
    print(image_url)
    image_url = "sudoku_test.jpg"
    img = cv2.imread(image_url, 0)
    roiArray = detect_plate(img)
    json_object["plate"] = roiArray
    return roiArray


# function to access data
def get_photo(request):
   # post_id retrieves the value that is sent by the client
   # the -1 is needed because arrays are 0-indexed
   idx = int(request.matchdict['photo_id'])-1
   # we return the value at the given index from car_photos
   return car_photos[idx]

def index_page(request):
   return FileResponse('index.html')

# Main entrypoint
if __name__ == '__main__':
    with Configurator() as config:
        img = [1]
        roiArray = detect_plate(img)
        get_text(roiArray)


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