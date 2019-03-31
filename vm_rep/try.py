import cv2
import sys
cap = cv2.VideoCapture(sys.argv[1])
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 200)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 200)
im = cap.read()

print(im[1].shape)
'''
b = image.copy()
# set green and red channels to 0
b[:, :, 1] = 0
b[:, :, 2] = 0


g = image.copy()
# set blue and red channels to 0
g[:, :, 0] = 0
g[:, :, 2] = 0

r = image.copy()
# set blue and green channels to 0
r[:, :, 0] = 0
r[:, :, 1] = 0


# RGB - Blue
cv2.imshow('B-RGB', b)

# RGB - Green
cv2.imshow('G-RGB', g)

# RGB - Red
cv2.imshow('R-RGB', r)

cv2.waitKey(0)
'''