import base64
import cv2 as cv
img = cv.imread("9738_土.jpg")
img_str = cv.imencode('.jpg', img)[1].tostring()

print(img_str[2])