import cv2
import matplotlib.pyplot as plt
import numpy as np
import imutils

blueLower = (7,  44,  126)
blueUpper = (26, 255, 255)


def find_marker(image):
    image=cv2.resize(image,(500,500))
    blurred = cv2.GaussianBlur(image, (11,11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, blueLower, blueUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    center = None
    c = max(contours, key=cv2.contourArea)
    marker=cv2.minAreaRect(c)
    return marker,c


#def focal_length(value,KNOWN_DISTANCE,KNOWN_WIDTH):
    #return (value * KNOWN_DISTANCE) / KNOWN_WIDTH
 
def distance_to_camera(KNOWN_WIDTH, focalLength, value):
    return (KNOWN_WIDTH * focalLength) / value
     


