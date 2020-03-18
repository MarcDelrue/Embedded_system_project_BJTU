import cv2
import numpy as np
from threading import Timer, Thread
import os 
import pyttsx3

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('trainer/trainer.yml')
cascadePath = "/home/pi/opencv/data/haarcascades/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)
engine = pyttsx3.init()
engine.setProperty('rate', 130)
font = cv2.FONT_HERSHEY_SIMPLEX
WAIT_SECONDS = 120
id = 0
count_face_appear = 0
path = 'dataset/Users/'

def getNames():
    names_array = []
    for f in os.listdir(path):
        names_array.insert(int(f.split(".")[0]) - 1, f.split(".")[1])
    return names_array

names = getNames()
cam = cv2.VideoCapture(0)
cam.set(3, 640)
cam.set(4, 480)
minW = 0.1*cam.get(3)
minH = 0.1*cam.get(4)

reapeared = 0

def user_gone():
    global count_face_appear
    global reapeared
    if reapeared == 0:
        print ("restart")
        count_face_appear = 0
        
    else:
        print ("still on camera")
        Timer(WAIT_SECONDS, user_gone).start()
        reapeared = 0

def register_new_comer(id):
    global count_face_appear
    global reapeared

    if count_face_appear <= 10:
        count_face_appear += 1
    if count_face_appear == 10:
        engine.say("Oh hello there " + id)
        engine.runAndWait()
        engine.stop()
        try:
            Timer(WAIT_SECONDS, user_gone).start()
            print ("See you in 5 second")
        except:
            pass
    if count_face_appear == 11:
        reapeared = 1



def life_cycle(): 
    while True:
        ret, img = cam.read()
        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        
        faces = faceCascade.detectMultiScale( 
            gray,
            scaleFactor = 1.2,
            minNeighbors = 5,
            minSize = (int(minW), int(minH)),
        )
        for(x,y,w,h) in faces:
            cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
            id, confidence = recognizer.predict(gray[y:y+h,x:x+w])
            if (confidence < 100):
                id = names[id - 1]
                if (100 - confidence > 35):
                    register_new_comer(id)
                confidence = "  {0}%".format(round(100 - confidence))
            else:
                id = "unknown"
                confidence = "  {0}%".format(round(100 - confidence))
            
            cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,255,255), 2)
            cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)  
        
        cv2.imshow('camera',img) 
        k = cv2.waitKey(10) & 0xff
        if k == 27:
            break

life_cycle()
print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()
