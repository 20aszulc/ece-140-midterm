# ece-140-midterm

## Tutorial 1
![Lab 5 Tutorial 3 on Pi](./public/media/Lab5Tutorial3.gif)
Above is the Lab 5 Tutorial 3 but running on the Raspberry Pi. We had immense difficulty during the Raspberry Pi setup since we UCSD-GUEST and UCSD-PROTECTED were not viable internet to download and operate the Pi on. As a result, in the situation that we were not able to secure a working monitor and lack the ethernet connection to do so. The Tutorial had to be completed at a private network (at home). We then ssh into the Pi, enabled the VNC through ifconfig menu, and worked on the lab from there on. Using our private computers as a monitor, instead of a direct HDMI access.

## Tutorial 2
Tutorial 2 was a simple GPIO pin based device that would interface with the Raspberry Pi. The setup was reminiscent of an Arduino setup, complete with a Python script that receives input and sends output to the desired pins. Here a simple distance gauge was made with a HC-SR04 ultrasonic sensor to judge a distance, then beyond a distance threshold a buzzer (alarm) would ring. A piece of code to note is GPIO.cleanup(). If this code was not included, the Raspberry Pi can easily malfuction and break because of conflicting signals at setup. .cleanup() "cleans" or reset all of the GPIO pins to their standard state to avoid multiple signals going through or throwing a high when it's not supposed to and overload the circuit, thus breaking the Pi.

Demonstration to the the Raspberry Pi device:
https://youtu.be/KNaq1svNrok
