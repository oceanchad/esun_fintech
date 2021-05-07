# hello preprocess

import cv2 as cv
import numpy as np
import os
import matplotlib.pyplot as plt
from torch import double
from skimage import metrics
prefix = "../competition"
data_path = prefix + "/train"
allFileList = os.listdir(data_path) # training data data_path 
img_1 = cv.imread(data_path+"/58222_煌.jpg", 0)
img_original_canny = cv.Canny(img_1, 100, 200)
kernel = np.ones((3,3), np.uint8)
closing = cv.morphologyEx(img_1, cv.MORPH_CLOSE, kernel)
opening = cv.morphologyEx(img_1, cv.MORPH_OPEN, kernel)

img_1_canny_o = cv.Canny(closing, 100, 200)
img_1_canny_c = cv.Canny(opening, 100, 200)

plt.subplot(221), plt.imshow(img_1, cmap="gray")
plt.subplot(222), plt.imshow(img_1_canny_o, cmap="gray")
plt.subplot(223), plt.imshow(img_1_canny_c, cmap="gray")
plt.show()

def ssim_origin_result(origin, result):
    (score, diff) = metrics.structural_similarity(origin, result, full=True)
    diff = (diff * 255).astype("uint8")
    return "SSIM: {}".format(score)

print(ssim_origin_result(img_original_canny, img_1_canny_o), ssim_origin_result(img_original_canny, img_1_canny_c))