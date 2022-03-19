import RPi.GPIO as GPIO

# import the library
from RpiMotorLib import RpiMotorLib

GpioPins = [18, 23, 24, 25]
mymotortest = RpiMotorLib.BYJMotor("MyMotorOne", "28BYJ")
GPIO.cleanup()