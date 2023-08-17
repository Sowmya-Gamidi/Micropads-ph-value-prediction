from PyQt5 import QtCore, QtGui, QtWidgets 
import sys
import cv2
import numpy as np
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QLabel, QFileDialog, QAction
from PyQt5.QtGui import QIcon, QPixmap, QFont
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
  
class Ui_MainWindow(object): 
  
    def setupUi(self, MainWindow): 
        MainWindow.resize(1900, 750) 
        self.centralwidget = QtWidgets.QWidget(MainWindow) 
          
        # adding pushbutton 
        self.pushButton = QtWidgets.QPushButton(self.centralwidget) 
        self.pushButton.setGeometry(QtCore.QRect(650, 150, 183, 28)) 

        # adding signal and slot  
        self.pushButton.clicked.connect(self.changelabeltext)



        self.label1 = QtWidgets.QLabel(self.centralwidget) 
        self.label1.setGeometry(QtCore.QRect(550, 50, 221, 200))       
        
        
        self.label1.setText("MPADs PH Prediction")
        self.label1.setFont(QFont('Arial', 50))

        
        self.label = QtWidgets.QLabel(self.centralwidget) 
        self.label.setGeometry(QtCore.QRect(550, 90, 221, 200))       
  
        # keeping the text of label empty before button get clicked 
        self.label.setText("")      
        self.label.setFont(QFont('Arial', 10)) 
        MainWindow.setCentralWidget(self.centralwidget) 
        self.retranslateUi(MainWindow) 
        QtCore.QMetaObject.connectSlotsByName(MainWindow)




      
    def retranslateUi(self, MainWindow): 
        _translate = QtCore.QCoreApplication.translate 
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow")) 
        self.pushButton.setText(_translate("MainWindow", "Push Button")) 
          
    def changelabeltext(self):
        global ROI_mean
    # This function is called when the user clicks File->Open Image.
        filename = QFileDialog.getOpenFileName()
        imagePath = filename[0]
        print(imagePath)
        
        image = cv2.imread(imagePath)
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
            ROI = original[y:y+66, x:x+66]
            cv2.rectangle(image, (x, y), (x + 66 , y + 66), (36,255,12), 2)
            break
        pr=np.mean(ROI)
        pr=round(pr,0)
        ph_means=[81, 95, 134, 129, 148, 182, 143, 120, 84, 58, 48, 59, 75, 63]
        predict=[]
        for i in ph_means:
            predict.append(abs(pr-i))
        pr=predict.index(min(predict))        
        cv2.imshow('close', close)
        cv2.imshow('image', image)
        cv2.imshow('ROI', ROI)
        cv2.waitKey()
        # changing the text of label after button get clicked 
        self.label.setText(str(pr))
        print(pr)
  
        # Hiding pushbutton from the main window 
        # after button get clicked.  
        self.pushButton.hide()    
  
app = QtWidgets.QApplication(sys.argv)  
    
MainWindow = QtWidgets.QMainWindow()  
ui = Ui_MainWindow()  
ui.setupUi(MainWindow)  
MainWindow.show() 
   
sys.exit(app.exec_())  
