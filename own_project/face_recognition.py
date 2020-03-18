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
USER_DATA = []
WAIT_SECONDS = 120
id = 0
count_face_appear = 0
path = 'dataset/Users/'

class users:  
    def __init__(self, id, name, on_camera):
        self.id = id
        self.name = name  
        self.on_camera = on_camera 

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

def user_gone(id):
    global count_face_appear

    if USER_DATA[id - 1].on_camera == 0:
        print ("restart")
        count_face_appear = 0
        
    else:
        print ("still on camera")
        Timer(WAIT_SECONDS, user_gone, [id]).start()
        USER_DATA[id - 1].on_camera = 0

def register_new_comer(id, name):
    global count_face_appear

    if count_face_appear <= 10:
        count_face_appear += 1
    if count_face_appear == 10:
        engine.say("Oh hello there " + name)
        USER_DATA.append(users(id, name, 0))
        engine.runAndWait()
        engine.stop()
        try:
            Timer(WAIT_SECONDS, user_gone, [id]).start()
        except:
            pass
    if count_face_appear == 11 and USER_DATA[id - 1].on_camera != 1:
        USER_DATA[id - 1].on_camera = 1



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
                name = names[id - 1]
                if (100 - confidence > 35):
                    register_new_comer(id, name)
                confidence = "  {0}%".format(round(100 - confidence))
            else:
                name = "unknown"
                confidence = "  {0}%".format(round(100 - confidence))
            
            cv2.putText(img, str(name), (x+5,y-5), font, 1, (255,255,255), 2)
            cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1)  
        
        cv2.imshow('camera',img) 
        k = cv2.waitKey(10) & 0xff
        if k == 27:
            break

life_cycle()
print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()
