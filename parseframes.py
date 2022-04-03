import numpy as np
import cv2
from PIL import Image
import pytesseract

x = 595
y = 325
w = 805
h = 490
k = 60

tesseract_path = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
pytesseract.pytesseract.tesseract_cmd = tesseract_path


def findstart(img):
    rows,cols = img.shape
    firstblack = []
    for i in range(cols):
        for j in range(rows):
            k = img[j,i]
            if (k == 0):
                firstblack.append(j)
                break
    return max(set(firstblack), key=firstblack.count)
            

def parseImg(idx):

    crop = cv2.imread("./frames/frame%d.jpg" % idx)[y:y+h,x:x+w]

    greycrop = cv2.imread("./frames/frame%d.jpg" % idx, cv2.IMREAD_GRAYSCALE)[y:y+h,x:x+w]
    (thresh, black_white_img) = cv2.threshold(greycrop, 20, 255, cv2.THRESH_BINARY)

    s = findstart(black_white_img)

    cv2.imshow('crop', black_white_img)
    cv2.waitKey(0)

    
    
    alpha = 1.2 # Contrast control (1.0-3.0)
    beta = 30 # Brightness control (0-100)

    adjusted = cv2.convertScaleAbs(greycrop, alpha=alpha, beta=beta)

    (th, bli) = cv2.threshold(greycrop, 80, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    blur = cv2.GaussianBlur(adjusted,(3,3),0)
    #gaussian_3 = cv2.GaussianBlur(bli, (0, 0), 2.0)
    #unsharp_image = cv2.addWeighted(bli, 2.0, gaussian_3, -1.0, 0)

    

    filter = blur



    for n in range (0,7):
        start = s + (n * k)
        end = start + k
        row = filter[start:end,0:805]
        cv2.imshow('crop', row)
        cv2.waitKey(0)
        cv2.imwrite("./frames/croppedframe%d.jpg" % idx, row)
        row_text = pytesseract.image_to_string(Image.open("./frames/croppedframe%d.jpg" % idx), lang='eng', config='--psm 7')
        print(row_text)
    

parseImg(2)