## Tutorial 1
    Using CAD software, we created a mount part to hold the camera. We had to create a cylinder then place 2 other 3' cylinders spaced evenly apart from the center rounded hexagonal shap to properly recreate the mount for the camera. We used m3 scres into the camera mount and the 3D part so the camera can move in accordance to the motor.

## Tutorial 2
    Tutorial 2 we tracked the location of our raspberryy pi using Global Positioning system.
    We connected an IC and atenna to our raspberry pi using VCC, GND, and RX.
    We accept the data into boot. We diable the serial0 port to recieve data. Then add a minicom library to analyze gps data. Get the atenna warmed up to understand signals and get a google maps linked to our location. If data is gibberish run echo command. Reverse geocoding allows human readable addresses.

## Tutorial 3
    We will  be locating a red colored object to object with color segmentation. Color segmentation takes region of the image within a color range to be extracted. Largest object in color space is returned. First, filter out only the right color with HSV where inRange() gets pixels with colors in that range.
    2) Do erosion then dilation to get rid of red shadows
    3)   IF neighbors are high then pixel takes value of label equal to lower left.
    4) Get largest object while all others are false
    5) Get distance from midpoint.

## Tutorial 4
    Step motors send a seperate pulse for each step and con only take 1 step at a time. A motor is used to repeat the same rotations over and over. Hybrid motor type is the most used motor, and it has tooth stealed caps. Half stepping improves angle resolution. 4096 half steps in our stepper motor, taking 8.192 seconds for 1 full rotation. Use a 9v battery to create a breadboard that moves the motor and thus rotates the camera set up to it.


## Tutorial 5
    When the output depends on the input, this is a closed-loop system. However there is overshoot, just like when the heater turns on in a cold room, the heater takes time to heat the already 60 degree room. We decrease overshoot by controlling the amount of output instead of a binary on/off system. For example, the heater should produce more heat at 55F than the small amount it would produce at 60F to stay at 60. Also known as proportional, integral, deivative. Rise time is time taken to go from 10% to 90%, settling time is time to reach 5% of desired error. Overshoot is max the output of system goes above output. Proportional gain changes input in proportion to error of system. Derivative gain damps to reduce overshoot and oscillations. Integral gain reduces steady state error. Reduce proportional gain to prevent oscillaion. In the code, we calculate speed control by summing gain times error values. High error means we want to have smaller step time. Delta t is the derivative of error. Sum error iss area under error curve. Buffer makes sure that we are tracking more than 20 px outside senter of image. Best pid values.


