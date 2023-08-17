
import cv2

image = cv2.imread('1.jpg')
original = image.copy()
h, w, _ = image.shape

gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (15,1))
close = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)

cnts = cv2.findContours(close, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]
minimum_area = .75 * h * w
cnts = [c for c in cnts if cv2.contourArea(c) < minimum_area]
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
for c in cnts:
    x,y,w,h = cv2.boundingRect(c)
    ROI = 255 - original[y:y+h, x:x+w]
    cv2.rectangle(image, (x, y), (x + w, y + h), (36,255,12), 2)
    break

cv2.imshow('close', close)
cv2.imshow('image', image)
cv2.imshow('ROI', ROI)
cv2.waitKey()
