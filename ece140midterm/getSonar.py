#!/usr/bin/env python3
import RPi.GPIO as GPIO
from init_db import *
import time
from datetime import datetime

buttonPin = 22
trigPin = 23
echoPin = 24
MAX_DISTANCE = 220  # define maximum measuring distance, unit: cm
timeOut = MAX_DISTANCE * 60  # calculate timeout w.r.t to maximum distance
buzzerPin = 6
LED_PIN = 17


def pulseIn(pin, level, timeOut):  # obtain pulse time of a pin under timeOut
    t0 = time.time()
    while (GPIO.input(pin) != level):
        if ((time.time() - t0) > timeOut * 0.000001):
            return 0;
    t0 = time.time()
    while (GPIO.input(pin) == level):
        if ((time.time() - t0) > timeOut * 0.000001):
            return 0;
    pulseTime = (time.time() - t0) * 1000000
    return pulseTime


def getSonar():  # get measurement of ultrasonic module, unit: cm
    GPIO.output(trigPin, GPIO.HIGH)  # make trigPin output 10us HIGH level
    time.sleep(0.00001)  # 10us
    GPIO.output(trigPin, GPIO.LOW)  # make trigPin output LOW level
    pingTime = pulseIn(echoPin, GPIO.HIGH, timeOut)  # read echoPin pulse time
    distance = pingTime * 340.0 / 2.0 / 10000.0  # distance w/sound speed @ 340m/s
    return distance

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(trigPin, GPIO.OUT)  # set trigPin to OUTPUT mode
    GPIO.setup(echoPin, GPIO.IN)  # set echoPin to INPUT mode
    GPIO.setup(buzzerPin, GPIO.OUT)
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(LED_PIN, GPIO.OUT) #set LED to OUTPUT mode
    turnOffLed() #since LED is on by default
    GPIO.setup(buttonPin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # set buttonPin to INPUT mode


def sendDataToServer(distance, buttonPress):
    now = datetime.now()
    timeTo = now.strftime("%H%M%S")
    cursor.execute("""INSERT INTO Sensor_Data (motion_sensor, second_sensor, atTime) VALUES 
                   ('%d', '%d', '%d');""" %(int(distance), buttonPress, int(timeTo)))
    #print out most recent data:
    cursor.execute("""SELECT * FROM Sensor_Data WHERE id=(SELECT max(id) FROM Sensor_Data);""")
    result = cursor.fetchone()
    print('---SELECT---')
    [print(x) for x in result]
    db.commit()


def lightUpLed():
    GPIO.output(LED_PIN, GPIO.HIGH)

def turnOffLed():
    GPIO.output(LED_PIN, GPIO.LOW)

def startBuzz():
    GPIO.output(buzzerPin, GPIO.HIGH)

def stopBuzz():
    GPIO.output(buzzerPin, GPIO.LOW)

def Buzzer(distance):
    if distance > 0:
        #print("buzzing")
        GPIO.output(buzzerPin, GPIO.HIGH)
    else:
        GPIO.output(buzzerPin, GPIO.LOW)


def loop():
    #while(True):
    for i in range(30):
        distance = getSonar()  # get distance
        buttonPress = GPIO.input(buttonPin)
        print("The distance is : %.2f cm" % (distance))
        print("The button is %s" % (str(buttonPress==GPIO.HIGH)))
        #lightUpLed()
        Buzzer(distance)
        sendDataToServer(distance, buttonPress)
        time.sleep(1)
        
        #turnOffLed()
        #time.sleep(0.5)


if __name__ == '__main__':  # Program entrance
    print ('Program is starting...')
    setup()
    try:
        loop()
    except KeyboardInterrupt:  # Press CTRL-C to end the program
        GPIO.cleanup()  # release GPIO resources