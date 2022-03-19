from http.client import SWITCHING_PROTOCOLS
from pickle import REDUCE
from cv2 import REDUCE_AVG
import numpy as np
import cv2
import RPi.GPIO as GPIO
import time


# import the motor library
from RpiMotorLib import RpiMotorLib

#video capture likely to be 0 or 1
cap=cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

#name a template
template = cv2.imread('./Challenge/templates/ball_template.png',0)

#Stepper Motor Setup
GpioPins = [18, 23, 24, 25]

# Declare a named instance of class pass a name and motor type
mymotortest = RpiMotorLib.BYJMotor("MyMotorOne", "28BYJ")
#min time between motor steps (ie max speed)
step_time = .002
#turn direction
num = 0 


#PID Gain Values (these are just starter values)
Kp = 0.003
Kd = 0.0001
Ki = 0.0001

#error values
d_error = 0
last_error = 0
sum_error = 0
color_of_object = 0
RED = 1
GREEN = 2
BLUE = 3

#GPS portion, hardware not functional
def GPS_Info():
   #Create variables to store values
   global NMEA_buff
   global lat_in_degrees
   global long_in_degrees
   nmea_time = []
   nmea_latitude = []
   nmea_longitude = []
   nmea_time = NMEA_buff[0]                    #extract time from GPGGA string
   nmea_latitude = NMEA_buff[1]                #extract latitude from GPGGA string
   nmea_latitude_dir = NMEA_buff[2]            #extract the direction of latitude(N/S)
   nmea_longitude = NMEA_buff[3]               #extract longitude from GPGGA string
   nmea_longitude_dir = NMEA_buff[2]           #extract the direction of longitude(E/W)
   print("NMEA Time: ", nmea_time,'\n')
   print ("NMEA Latitude:", nmea_latitude,"NMEA Longitude:", nmea_longitude,'\n')

   lat = float(nmea_latitude)                  #convert string into float for calculation
   longi = float(nmea_longitude)               #convert string into float for calculation


   #get latitude in degree decimal format with direction
   lat_in_degrees = convert_to_degrees(lat) if nmea_latitude_dir == N else (-1 * convert_to_degrees(lat))  
   #get longitude in degree decimal format with direction
   long_in_degrees = convert_to_degrees(longi) if nmea_latitude_dir == N else (-1 * convert_to_degrees(lat))


#convert raw NMEA string into degree decimal format
def convert_to_degrees(raw_value):
   decimal_value = raw_value/100.00
   degrees = int(decimal_value)
   mm_mmmm = (decimal_value - int(decimal_value))/0.6
   position = degrees + mm_mmmm
   position = "%.4f" %(position)
   return position


#part 2

def choose_hsv_color(COLOR,hsv):
    global RED, GREEN, BLUE, Kp, Kd, Ki, d_error, last_error, sum_error, color_of_object, num
    global sleep_time, mymotortest, GpioPins, template, cap
    if 'RED' == COLOR:
            #color is on upper and lower of the hsv scale. Requires 2 ranges 
        lower1 = np.array([0, 150, 20])
        upper1 = np.array([10, 255, 255])
        lower2 = np.array([160,100,20])
        upper2 = np.array([179,255,255])
        
        #masks input image with upper and lower color ranges
        color_only1 = cv2.inRange(hsv, lower1, upper1)
        color_only2 = cv2.inRange(hsv, lower2 , upper2)
        
        color_only = color_only1 + color_only2
        return color_only
    if 'GREEN' == COLOR:
                    #color is on upper and lower of the hsv scale. Requires 2 ranges 
        lower1 = np.array([10, 100, 50])
        upper1 = np.array([150, 255, 220])
        lower2 = np.array([160,100,20])
        upper2 = np.array([179,255,255])
        
        #masks input image with upper and lower color ranges
        color_only1 = cv2.inRange(hsv, lower1, upper1)
        
        color_only = color_only1 
        return color_only
    if 'BLUE' == COLOR:
        
        #color is on upper and lower of the hsv scale. Requires 2 ranges 
        lower1 = np.array([90, 50, 50])
        upper1 = np.array([130, 255, 255])
        
        #masks input image with upper and lower color ranges
        color_only1 = cv2.inRange(hsv, lower1, upper1)
        
        color_only = color_only1 
        return color_only

def shape_recognition(contours,image):
    ret, test = cv2.threshold(image[:,:,0], 50, 255, cv2.THRESH_BINARY)
    test = cv2.Canny(test,100,100)
    contours, hierarchy = cv2.findContours(image=test, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_NONE)
    test = cv2.drawContour(image=image,contours=contours,contourIDx=-1,color=(0,255,0),thickness=1,lineType=cv2.LINE_AA)
    if contours:
        return contours
    else:
        return 0

def run_pid(object_name, color_range, contour, size):
    global RED, GREEN, BLUE, Kp, Kd, Ki, d_error, last_error, sum_error, color_of_object, num
    global sleep_time, mymotortest, GpioPins, template, cap
    print(mymotortest)
    start = time.time()
    object = "object not in view"
    end = time.time()
    time_elapsed = end - start
    while(time_elapsed < 15):
        print(GpioPins)
        print(time_elapsed)
        _,frame=cap.read()

        #convert to hsv deals better with lighting
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        bw = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        
        mask=np.ones((5,5),np.uint8)
        

        color_only = choose_hsv_color(color_range,hsv)
        
        #run an opening to get rid of any noise
        opening=cv2.morphologyEx(color_only,cv2.MORPH_OPEN,mask)
        ret, test = cv2.threshold(frame[:,:,0], 50, 255, cv2.THRESH_BINARY)
        cv2.imshow('binary', test)
        test = cv2.Canny(test,100,100)
        contours, hierarchy = cv2.findContours(image=test, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_NONE)
        # draw contours on the original image

        
        test = cv2.drawContours(image=frame, contours=contours, contourIdx=-1, color=(0, 255, 0), thickness=2, lineType=cv2.LINE_AA)
        cv2.imshow('contours',test)
        cv2.imshow('original', frame)
        #if contours:
            #print("Yep")
        #opening = shape_recognition(template,frame)
        cv2.imshow('Masked image', opening)

        #run connected components algo to return all objects it sees.        
        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(opening,4, cv2.CV_32S)
        b=np.matrix(labels)
        if num_labels > 5 and contours:
            #start = time.time()
            #extracts the label of the largest none background component and displays distance from center and image.
            max_label, max_size = max([(i, stats[i, cv2.CC_STAT_AREA]) for i in range(1, num_labels)], key = lambda x: x[1])
            Obj = b == max_label
            Obj = np.uint8(Obj)
            Obj[Obj > 0] = 255
            cv2.imshow('largest object', Obj)
            
            object = "Object found"
            
            #calculate error from center column of masked image
            error = -1 * (320 - centroids[max_label][0])

            #part 3

            #speed gain calculated from PID gain values
            speed = Kp * error + Ki * sum_error + Kd * d_error
            
            #if negative speed change direction
            if speed < 0:
                direction = False
            else:
                direction = True
            
            #inverse speed set for multiplying step time (lower step time = faster speed)
            speed_inv = abs(1/(speed))
            
            #get delta time between loops
            delta_t = time.time() - start
            #calculate derivative error
            d_error = (error - last_error)/delta_t
            #integrated error
            sum_error += (error * delta_t)
            last_error = error
            
            #buffer of 20 only runs within 20
            if abs(error) > 20:
                #rint(speed_inv*step_time)
                mymotortest.motor_run(GpioPins , speed_inv * step_time, 1, direction, False, "full", .05)
            else:
                #run 0 steps if within an error of 20
                print(step_time)
                mymotortest.motor_run(GpioPins , step_time, 0, direction, False, "full", .05)
            
        else:
            print('no object in view')
            if num >= 0 :
                mymotortest.motor_run(GpioPins , .002, 5, False, False, "half", 0.05)
                #print("turn")
                num = num + 1
                if num == 30:
                    num = -1
            if num < 0:
                mymotortest.motor_run(GpioPins , .002, 5, True, False, "half", .05)
                num = num - 1
                if num == -30:
                    num = 0
        end = time.time()
        time_elapsed = end - start
            #print(time_elapsed)
            

        k=cv2.waitKey(5)
        if k==27:
            break


    cv2.destroyAllWindows()
    
    return object


# objects: color toothbrush, green sphere, blue mouse

