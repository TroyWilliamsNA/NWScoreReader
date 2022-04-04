import numpy as np
import cv2
from PIL import Image
import pytesseract

#Vars to be edited
num_frames = 35

x = 485
y = 325
w = 905
h = 490
k = 60

tesseract_path = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
pytesseract.pytesseract.tesseract_cmd = tesseract_path


def printrow(out):
    for item in out:
        print(item, end = ' ')
    print("\n")

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


def count_none(entry):
    n_count = 0
    for idx in entry:
        if idx == None:
            n_count += 1
    return n_count

def validate_entry(entry):
    if not (entry[0] != None and entry[0].isnumeric() and (int(entry[0]) > 0) and int(entry[0]) < 60):
        entry[0] = None

    if not (entry[0] != None and entry[0].isalnum()):
        entry[0] = None

    if not (entry[0] != None and entry[2].isnumeric() and (int(entry[2]) >= 0) and int(entry[2]) < 100000):
        entry[2] = None

    if not (entry[0] != None and entry[3].isnumeric() and (int(entry[3]) >= 0) and int(entry[3]) < 100):
        entry[3] = None

    if not (entry[0] != None and entry[4].isnumeric() and (int(entry[4]) >= 0) and int(entry[4]) < 100):
        entry[4] = None

    if not (entry[0] != None and entry[5].isnumeric() and (int(entry[5]) >= 0) and int(entry[5]) < 1000):
        entry[5] = None
    
    if not (entry[0] != None and entry[6].isnumeric() and (int(entry[6]) >= 0) and int(entry[6]) < 10000000):
        entry[6] = None

    if not (entry[0] != None and entry[7].isnumeric() and (int(entry[7]) >= 0) and int(entry[7]) < 10000000):
        entry[7] = None


def make_csv(data):
    csv_string = "Rank,Name,Score,Kills,Deaths,Assists,Healing,Damage\n"

    for line in data:
        for i, entry in enumerate(line):
            if (entry == None):
                line[i] = "CNR"
        sep = ","
        line_string = sep.join(line) + "\n"
        csv_string += line_string

    return csv_string

data = []

def parseImg(idx):

    crop = cv2.imread("./frames/frame%d.jpg" % idx)[y:y+h,x:x+w]

    greycrop = cv2.imread("./frames/frame%d.jpg" % idx, cv2.IMREAD_GRAYSCALE)[y:y+h,x:x+w]
    (thresh, black_white_img) = cv2.threshold(greycrop, 20, 255, cv2.THRESH_BINARY)

    s = findstart(black_white_img)

    #cv2.imshow('crop', crop)
    #cv2.waitKey(0)

    
    
    alpha = 1.2 # Contrast control (1.0-3.0)
    beta = 30 # Brightness control (0-100)

    adjusted = cv2.convertScaleAbs(greycrop, alpha=alpha, beta=beta)

    (th, bli) = cv2.threshold(greycrop, 80, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    blur = cv2.GaussianBlur(adjusted,(3,3),0)
    #gaussian_3 = cv2.GaussianBlur(bli, (0, 0), 2.0)
    #unsharp_image = cv2.addWeighted(bli, 2.0, gaussian_3, -1.0, 0)

    

    filter = blur

    col_s = (5 ,110,305,430,530,620,700,800)
    col_e = (45,295,405,460,560,670,790,890)
    col_conf = (
        '--psm 7 -c tessedit_char_whitelist=0123456789', # Rank
        '--psm 7 -c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', # Name
        '--psm 7 -c tessedit_char_whitelist=0123456789', # Score
        '--psm 8 -c tessedit_char_whitelist=0123456789', # Kills
        '--psm 8 -c tessedit_char_whitelist=0123456789', # Deaths
        '--psm 7 -c tessedit_char_whitelist=0123456789', # Assists
        '--psm 7 -c tessedit_char_whitelist=0123456789', # Healing
        '--psm 7 -c tessedit_char_whitelist=0123456789'  # Damage
        ) 

    for n in range (0,7):
        start = s + (n * k)
        end = start + k

        col_output = [None,None,None,None,None,None,None,None]
        # Segment into columns
        for m in range (0,8):
            seg = filter[start:end,col_s[m]:col_e[m]]
            #cv2.imshow('crop', seg)
            #cv2.waitKey(0)
            cv2.imwrite("./frames/croppedframe%d.jpg" % idx, seg)
            seg_text = pytesseract.image_to_string(Image.open("./frames/croppedframe.jpg"), lang='eng', config=col_conf[m])
            col_output[m] = seg_text.strip("\n")
        validate_entry(col_output)
        if (count_none(col_output) < 3):
            data.append(col_output)


    
for n in range(0,num_frames):
    parseImg(n)

#for line in data:
#    print(line)

#print(make_csv(data))
f = open("parse_result.csv", "w")
f.write(make_csv(data))
f.close()