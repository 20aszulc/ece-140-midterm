from http.client import SWITCHING_PROTOCOLS
from pickle import REDUCE
from cv2 import REDUCE_AVG
import numpy as np
import cv2
import RPi.GPIO as GPIO
import time

# import the motor library
from RpiMotorLib import RpiMotorLib


def run_pid(object_name, color_range, contour, size):

    #video capture likely to be 0 or 1
    cap=cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
    object = "object not in view"


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
    color_of_object = color_range
    RED = 1
    GREEN = 2
    BLUE = 3


    #part 2

    def choose_hsv_color(COLOR):
        if RED == COLOR:
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
        if GREEN == COLOR:
                        #color is on upper and lower of the hsv scale. Requires 2 ranges
            lower1 = np.array([10, 100, 50])
            upper1 = np.array([150, 255, 220])
            lower2 = np.array([160,100,20])
            upper2 = np.array([179,255,255])

            #masks input image with upper and lower color ranges
            color_only1 = cv2.inRange(hsv, lower1, upper1)

            color_only = color_only1
            return color_only
        if BLUE == COLOR:
            #color is on upper and lower of the hsv scale. Requires 2 ranges
            lower1 = np.array([90, 50, 50])
            upper1 = np.array([130, 255, 255])

            #masks input image with upper and lower color ranges
            color_only1 = cv2.inRange(hsv, lower1, upper1)

            color_only = color_only1
            return color_only


    while(1):
        _,frame=cap.read()

        #convert to hsv deals better with lighting
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)



        mask=np.ones((5,5),np.uint8)

        color_only = choose_hsv_color(color_range)

        #run an opening to get rid of any noise
        opening=cv2.morphologyEx(color_only,cv2.MORPH_OPEN,mask)
        cv2.imshow('Masked image', opening)

        #run connected components algo to return all objects it sees.
        num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(opening,4, cv2.CV_32S)
        b=np.matrix(labels)
        if num_labels > 1:
            start = time.time()
            #extracts the label of the largest none background component and displays distance from center and image.
            max_label, max_size = max([(i, stats[i, cv2.CC_STAT_AREA]) for i in range(1, num_labels)], key = lambda x: x[1])
            Obj = b == max_label
            Obj = np.uint8(Obj)
            Obj[Obj > 0] = 255
            cv2.imshow('largest object', Obj)

            object = "found object" + object_name
            print(object+ " "+color_range)

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
                print(speed_inv*step_time)
                print("hi")
                mymotortest.motor_run(GpioPins , speed_inv * step_time, 1, direction, False, "full", .05)
            else:
                #run 0 steps if within an error of 20
                print(step_time)
                mymotortest.motor_run(GpioPins , step_time, 0, direction, False, "full", .05)

        else:
            print('no object in view')
            if num >= 0 :
                mymotortest.motor_run(GpioPins , .002, 5, False, False, "half", 0.05)
                print("turn")
                num = num + 1
                if num == 30:
                    num = -1
            if num < 0:
                mymotortest.motor_run(GpioPins , .002, 5, True, False, "half", .05)
                num = num - 1
                if num == -30:
                    num = 0


        k=cv2.waitKey(5)
        if k==27:
            break

    cv2.destroyAllWindows()
    GPIO.cleanup()
    return object
    # objects: color toothbrush, green sphere, blue mouse