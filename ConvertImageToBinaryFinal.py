"""
Author: Ruaa Abdulmajeed 101074335

This program will take an image and turn it into a bitmap that can be used for 
an OLED screen.

"""

#from Cimpl import * # Carleton image editing library, uses PIL library


from tkinter import *
import tkinter.filedialog
from PIL import Image
import PIL.ImageTk

IMAGE_FILE_TYPES = [('All files', '.*'),
                    ('BMP', '.bmp'),
                    ('GIF', '.gif'),
                    ('PNG', '.png'),
                    ('TIFF', '.tif'),
                    ('TIFF', '.tiff'),
                    ('JPEG', '.jpg'),
                    ('JPEG', '.jpeg')]

OLED_HEIGHT = 128
OLED_WIDTH = 32

def convertImageToBinary(filePath):
    
    image = PIL.Image.open(filePath)
    imageWidth, imageHeight = image.size
    
    if(imageWidth % 8 != 0 or imageHeight % 8 != 0 or imageHeight > OLED_HEIGHT  \
       or imageWidth > OLED_WIDTH):
        
        image = fixSize(image)
        imageWidth, imageHeight = image.size
    
    name = input("Please enter a name for the bitmap: ")
    bitmap = "static const unsigned char PROGMEM " + name.upper() + "[] = \n{" 
    
    pix = image.load()
    thresh = 200
    
    for y in range(imageHeight):
        count = 0
        for x in range(imageWidth):
            if(count == 0):
                bitmap = bitmap + "B"
            if(count < 8):
                if(pix[x,y] < (thresh, thresh, thresh)):
                    bitmap = bitmap + "1"
                else:
                    bitmap = bitmap + "0"
            count = count + 1
            if(count == 8):
                if(y==imageHeight-1 and x == imageWidth-1):
                    bitmap = bitmap + "\n};"
                else:
                    bitmap = bitmap + ", "
                    count = 0
        bitmap = bitmap + "\n"
    chooseCopyOrFile(bitmap, name)
    
    
def fixSize(image):
    image = image.resize((64,32), PIL.Image.ANTIALIAS)

    return image

def choose_file():
    root = Tk()
    # Hide the top-level window. (We only want the Open dialogue box
    # to appear.)
    root.withdraw()
    
    path = tkinter.filedialog.askopenfilename(filetypes=IMAGE_FILE_TYPES)
    
    root.destroy()
    return path

def chooseCopyOrFile(bitmap, name):
    copy = input("Would you like the bitmap to be added to your clipboard?\n(Yes/No)")
    file = input("Would you like a file containing the bitmap to be created?\n(Yes/No)")
    if(copy.lower() == "yes"):
        root = Tk()
        root.withdraw()
        root.clipboard_clear()
        root.clipboard_append(bitmap)
        root.update() # now it stays on the clipboard after the window is closed
        root.destroy()
    if(file.lower() == "yes"):
        filename = name.lower() + ".txt"
        file = open( filename,"w+")
        file.write(bitmap)
    return 0

# Main Script
try:
    convertImageToBinary(choose_file())
except:
    print("There was an error, please try again")