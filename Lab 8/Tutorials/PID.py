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


#Stepper Motor Setup
GpioPins = [18, 23, 24, 25]

# Declare a named instance of class pass a name and motor type
mymotortest = RpiMotorLib.BYJMotor("MyMotorOne", "28BYJ")
#min time between motor steps (ie max speed)
step_time = .002

#PID Gain Values (these are just starter values)
Kp = 0.003
Kd = 0.0001
Ki = 0.0001

#error values
d_error = 0
last_error = 0
sum_error = 0