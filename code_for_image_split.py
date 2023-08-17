# importing Image class from PIL package 
from PIL import Image 
  
# opening a multiband image (RGB specifically) 
im = Image.open("Desktop\5.jpg") 
  
# split() method 
# this will split the image in individual bands 
# and return a tuple 
im1 = Image.Image.split(im) 
  
# showing each band 
im1[0].show() 
im1[1].show() 
im1[2].show() 
