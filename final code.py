from tkinter import *
import tkinter as tk
from tkinter.ttk import *
import cv2
import numpy as np
from PIL import *
from PIL import ImageTk, Image

from tkinter import filedialog
import PIL
root = Tk()  
root.title("PH Value PREDICTOR")
ph_means=[87.43245891753354, 99.72433983926521, 139.3525920063316, 132.31701390881784,
          149.18109889229413, 182.1787693205016, 142.72771074974258, 125.98292242233491,
          92.75963718820861, 69.5447079236553, 56.01988136241867, 71.64766124661247,
          82.71428266666666, 69.359]
predict=[]

def open_img(): 
    global pr
    x = openfilename()
    image = cv2.imread(x)
    original = image.copy
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
        ROI = original[y:y+h, x:x+w]
        cv2.rectangle(image, (x, y), (x + w, y + h), (36,255,12), 2)
        break

    cv2.imwrite('blue.jpg',ROI)
    cv2.waitKey()

    
    ROI_mean=ROI.mean()
    for i in ph_means:
        predict.append(abs(ROI_mean-i))
    pr=predict.index(min(predict))+1
    label = tk.Label(root, fg="orange")
    label.config(text='The Predicted ph value for the given M-Pad image is %d'%(pr), font=("Times New Roman", 15))
    label.place(x=430,y=350)

def openfilename(): 
    filename = filedialog.askopenfilename(title ='Open') 
    return filename 

root.geometry("{0}x{1}+0+0".format(root.winfo_screenwidth(), root.winfo_screenheight()))
root.resizable(width = True, height = True)

'''canvas = tk.Canvas(root, width = 1080, height = 800)
    canvas.pack()
    photo =ImageTk.PhotoImage(Image.open('13.png'))
    canvas.create_image(0, 0,  anchor=NW, image=photo)'''
lbl=tk.Label(root, fg= 'black')
lbl.config(text="Predicting water Ph using M-Pads", font=("Monotype Corsiva", 30))
lbl.place(x=300, y=70)
btn = Button(root, text =' UPLOAD IMAGE & PREDICT', command = open_img)
btn.place(x=570,y=400)
lbl1=tk.Label(root, fg= 'green')
lbl1.config(text="Project Associates:\n\tHemaMadhusri", font=("Copperplate Gothic Light", 15))
lbl1.place(x=950, y=550)
root.mainloop() 

