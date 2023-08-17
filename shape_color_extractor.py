import cv2
import numpy as np

img = cv2.imread('img8.jpg', cv2.IMREAD_COLOR)

img_resized = cv2.resize(img, (500,500))
img_gray = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)

ret, img_thresh = cv2.threshold(img_gray , 110, 255, cv2.THRESH_BINARY_INV)

# img_thresh = cv2.adaptiveThreshold(
#     img_resized,
#     255,
#     cv2.ADAPTIVE_THRESH_MEAN_C,
#     cv2.THRESH_BINARY,11,2
#     )

# img_thresh = cv2.adaptiveThreshold(
#     img_resized,
#     255,
#     cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
#     cv2.THRESH_BINARY,11,2
#     )

mask = cv2.cvtColor(img_thresh, cv2.COLOR_GRAY2BGR)

img_masked = cv2.bitwise_and(img_resized, mask) 

cv2.imshow('Original', img_resized)
# cv2.imshow('Gray', img_gray)
cv2.imshow('Masked', img_masked)
# cv2.imshow('Thresh', img_thresh)

while True:
    if cv2.waitkey(0) == ord('q'):
        cv2.destroyAllWindows()
        break
