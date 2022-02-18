# ece-140-midterm
## Mike Liu (A15409210)

## Tutorial 1
![Lab 5 Tutorial 3 on Pi](./public/media/Lab5Tutorial3.gif)
Above gif is the Lab 5 Tutorial 3 but running on the Raspberry Pi. We had immense difficulty during the Raspberry Pi setup since we UCSD-GUEST and UCSD-PROTECTED were not viable internet to download and operate the Pi on. As a result, in the situation that we were not able to secure a working monitor and lack the ethernet connection to do so. The Tutorial had to be completed at a private network (at home). We then ssh into the Pi, enabled the VNC through ifconfig menu, and worked on the lab from there on. Using our private computers as a monitor, instead of a direct HDMI access.

## Tutorial 2
Tutorial 2 was a simple GPIO pin based device that would interface with the Raspberry Pi. The setup was reminiscent of an Arduino setup, complete with a Python script that receives input and sends output to the desired pins. Here a simple distance gauge was made with a HC-SR04 ultrasonic sensor to judge a distance, then beyond a distance threshold a buzzer (alarm) would ring. A piece of code to note is GPIO.cleanup(). If this code was not included, the Raspberry Pi can easily malfuction and break because of conflicting signals at setup. .cleanup() "cleans" or reset all of the GPIO pins to their standard state to avoid multiple signals going through or throwing a high when it's not supposed to and overload the circuit, thus breaking the Pi.

## Challenge 1/ Midterm
#### Summary
![Lab 6 Schematic](./public/media/Lab_6_Schematic.png)
Above is our Lab 6 Schematic, it is an extension of the Tutorial 2 schematic with addition of a working LED and Buzzer (replaced by Piezzo Speaker in Schematic). For this Challenge we have three main file catagories working together in conjunction: website, database, and raspberry pi.

#### Purpose of each File
Website file(s) are the following: ```./public/rest.js``` ; ```index.html``` ;  ```app.py```.
 Website files handles all execution of starting and maintaining the website. At the base level, when we run ```app.py``` it is suppose to create a website in the format specified in ```index.html``` and specific functions for pressing buttons or dropdown menus are specified in ```./public/rest.js```. 

Database file(s) are the following: ```init_db.py``` ; ```credentials.env``` (the .env files that hold your MYSQL credentials)
The Database files are suppose to initiate the MYSQL database from the format specified in ```init_db.py```. But in order to access the MYSQL without manually creating one on the command prompt, ```init_db.py``` also automatically signs into the host's MYSQL from the credentials from ```credentials.env```. Data streams will be updated to the MYSQL tables (in Raspberry Pi it uses Mariadb) which certain functions depend on the data points to carry out their functions. Specific use and pulling of MYSQL data will happen in ```app.py```

Raspberry Pi file(s) are the following: ```getSonar.py```
The Raspberry Pi file(s) are the references and functions that will directly interact with the GPIO pins on the Raspberry Pi. ```getSonar.py``` is written with function defs that will carry out processes such as, turning on and off LED, turning and off buzzer, gather sensor data from ultrasonic sensor and button, and populate the corresponding data to the MYSQL table. 

#### How to Test
In order to test our project, you must load all of the files in ```./Midterm```

Demonstration to the the Raspberry Pi device:
https://youtu.be/KNaq1svNrok
