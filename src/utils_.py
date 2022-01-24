from random import random
import pyautogui
import time

pt = pyautogui

def getImage_(image, conf=0.8):
    folder = 'images/'
    file = folder + image
    position = pt.locateCenterOnScreen(file, confidence=0.8)
    
    if (position == None):
        return None
    
    x = position.x + (random() * 10)
    y = position.y + (random() * 10)

    return (x,y)

def mouseClick_(image):
    x,y = image
    pt.moveTo(x, y, random())
    pt.click()
    
    return True

def reloadPage_():
    pt.hotkey('ctrl','f5')

def dateFormatted_(format = '%Y-%m-%d %H:%M:%S'):
    datetime = time.localtime()
    now = time.strftime(format, datetime)
    return now