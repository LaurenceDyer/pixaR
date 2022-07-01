import cv2
import os
import time

cam = cv2.VideoCapture("C:/Users/laure/Desktop/python/Movies/MonstersInc/monstersinc.mp4")

try:
    if not os.path.exists('Image/monsters'):
        os.makedirs('Image/monsters')

except OSError:
    print('Error: Creating directory for images')

intvl = 10 #interval in second(s)

fps= int(cam.get(cv2.CAP_PROP_FPS))
print("fps : " ,fps)

currentframe = 0
while (True):
    ret, frame = cam.read()
    if ret:
        if(currentframe % (fps*intvl) == 0):
            name = './Image/monsters/monsters' + str(currentframe) + '.jpg'
            print('Creating...' + name)
            cv2.imwrite(name, frame)
        currentframe += 1
    else:
        break

cam.release()
cv2.destroyAllWindows()