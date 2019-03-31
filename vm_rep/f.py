import cv2
import sys
import numpy as np
cap = cv2.VideoCapture(sys.argv[1])
length = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
print( length )
im = cap.read(0)
im= cap.read(1)
im = cap.read(0)
print(type(im[1]))
cv2.imshow('frmae',im[1])
cv2.waitKey(0)