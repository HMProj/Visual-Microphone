import numpy as np
import cv2
import sys
cap  = cv2.VideoCapture(sys.argv[1])
im = cap.read()
im =im[1]
frame = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

print(frame.shape)

for x in frame.transpose():
    print(x)