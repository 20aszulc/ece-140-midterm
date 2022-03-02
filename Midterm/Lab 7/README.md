## Tutorial 1
First we connect arucam to usb of raspberry pi. Then import cv2 on it.
Then run ISUSB and take a picture with your camera. Saving the image as test.jpg

## Tutorial 2

Install pytesseract to extract text from an image. First blur filers gets out high frequency noise. Then binary threshold keeps edges. Inversion swithces black and white colors by subracting pixel intensity from max. Dilation enlarge fragments.
Then we group together pixels with similar color by the largest 15 contouring groups. We approximate polygons by storing corners of polygons, then we shape them into a rectangle and rotate.
Finally, we work on rextracting the image into a 9 by 9 block. Send box to pytesseract image string to get test.