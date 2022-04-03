import cv2

vidcap = cv2.VideoCapture('score.mp4')

print("successfully read video")
count = 0
framessaved = 0

starttime = 90
endtime = 95
interval = 60

print("starting to read")
while True:
    success,image = vidcap.read()   
    if (not success):
        break
    if ((count > 60 * starttime) and (count < 60 * endtime)):
        if ((count % interval) == 0):   
            cv2.imwrite("./frames/frame%d.jpg" % framessaved, image)     # save frame as JPEG file 
            print("saving %d", framessaved)
            framessaved += 1  
    count += 1
print("saved: %d of %d", framessaved, count)