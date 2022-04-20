import time
import numpy as np
import urllib.request
from main import *
import argparse

#assign  value based on reference 
KNOWN_DISTANCE = 50.0
KNOWN_WIDTH = 7.0

parser = argparse.ArgumentParser()
parser.add_argument('--webcam', type=bool, default=True)
parser.add_argument('--url', type=str, default=r'C:\Users\MYTHRY\Desktop\1.jpeg')
args = parser.parse_args()

url = args.url
time.sleep(2)
if args.webcam:
    cap =  cv2.VideoCapture(0)
    _,c_image = cap.read()


else:
    imgResp = urllib.request.urlopen(url)
    imgNp = np.array(bytearray(imgResp.read()), dtype=np.uint8)
    c_image = cv2.imdecode(imgNp, -1)
    
marker,c = find_marker(c_image)
print("<======focallength=======>")
focalLength = (marker[1][0] * KNOWN_DISTANCE) / KNOWN_WIDTH
print("focalLength",focalLength)

time.sleep(2)
while True:
    if args.webcam:
        _,image = cap.read()
    else:
        imgResp = urllib.request.urlopen(url)
        image = np.array(bytearray(imgResp.read()), dtype=np.uint8)


    marker,c = find_marker(image)
    CM = distance_to_camera(KNOWN_WIDTH, focalLength, marker[1][0]) 
    print("distance between camera to object", CM/100)

    ((x,y), (width, height), rotation) = marker
    s = f"x {np.round(x)}, y: {np.round(y)}, width: {np.round(width)}, height: {np.round(height)}, rotation: {np.round(rotation)}"
    box = cv2.boxPoints(marker)
    box = np.int64(box)
    M = cv2.moments(c)
    center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
    # for object detection
    cv2.circle(image, center, 5, (255, 0, 255), -1)
    cv2.drawContours(image, [box], 0, (0, 255, 255), 2)
    #image = cv2.putText(image, text, org, font, fontScale,color, thickness, cv2.LINE_AA, False)
    #cv2.putText(image, s, (25, 50),  cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 3)

    #for finding distance
    M=CM/100
    cv2.putText(image, "%.2fM" % M,
                (image.shape[1] - 350, image.shape[0] - 15), cv2.FONT_HERSHEY_SIMPLEX,
                2.0, (255, 0, 0), 3)
   # print(M)
    cv2.imshow("image", image)
    if cv2.waitKey(2)&0xFF==27:
        break
cap.release()
cv2.destroyAllWindows()


    

  


