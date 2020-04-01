import cv2
import os
import numpy as np
from PIL import Image
import shutil
from text_to_speech import say_out_loud

def life_cycle(count, user_id, cam, user_photo):
    image_list = []
    image_path = []
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    face_detector = cv2.CascadeClassifier('/home/pi/opencv/data/haarcascades/haarcascade_frontalface_default.xml')
    img_name = []
    for x in range(30):
        img_name.append(x)
    for x in user_photo:
        img_name.remove(int(x.split("/")[2].split(".")[0]))
    print (img_name)
    index = 0
    while(True):
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
            cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)     
            count += 1
            picture_name="user_picture/" + user_id + "/" + str(img_name[index]) + ".jpg"
            index += 1
            path = "tmp/" + picture_name.replace("/", "_")
            image_list.append(picture_name)
            image_path.append(path)
            # # Save the captured image into the datasets folder
            cv2.imwrite(path, gray[y:y+h,x:x+w])
            cv2.imshow('image', img)
        k = cv2.waitKey(100) & 0xff # Press 'ESC' for exiting video
        if k == 27:
            break
        elif count >= 30:
            return image_list, image_path

def remove_tmp_pictures(extension):
    filelist = [ f for f in os.listdir("tmp/") if f.endswith(extension) ]
    for f in filelist:
        os.remove(os.path.join("tmp/", f))

def take_picture(user):
    cam = cv2.VideoCapture(0)
    cam.set(3, 640) # set video width
    cam.set(4, 480) # set video height
    
    user_id = user["id"]
    count = len(user["photos"])
    if count == 30:
        say_out_loud("You can only have 30 pictures per user. Please delete some.")
        cam.release()
        cv2.destroyAllWindows()
        return (image_list, image_path)
    try:
        os.mkdir("./tmp")
    except:
        pass
    print("\n [INFO] Initializing face capture. Look the camera and wait ...")
    image_list, image_path = life_cycle(count, user_id, cam, user["photos"])
    print("\n [INFO] Exiting Program and cleanup stuff")
    cam.release()
    cv2.destroyAllWindows()
    return (image_list, image_path)