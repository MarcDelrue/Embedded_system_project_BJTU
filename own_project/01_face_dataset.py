import cv2
import os
import numpy as np
from PIL import Image
import shutil

# FEATURES :
# choose id + Name
# propose add picture if id known

# TODO:
# iterate on users for training

def check_id_taken():
    for filename in os.listdir(path):
        if (filename.split(".")[0] == face_id):
            return (int(input (" Id " + face_id + " already taken.\nPress 1 to override user, press 2 to add new photos ==>  ")), filename)
    return (1, None)

def life_cycle(count):
    memo_count = count
    while(True):
        ret, img = cam.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, 1.3, 5)
        for (x,y,w,h) in faces:
            cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)     
            count += 1
            # Save the captured image into the datasets folder
            cv2.imwrite(path + face_folder + "/" + str(face_id) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])
            cv2.imshow('image', img)
        k = cv2.waitKey(100) & 0xff # Press 'ESC' for exiting video
        if k == 27:
            break
        elif count >= memo_count + 30: # Take 30 face sample and stop video
            break


path = 'dataset/Users/'
cam = cv2.VideoCapture(0)
cam.set(3, 640) # set video width
cam.set(4, 480) # set video height
recognizer = cv2.face.LBPHFaceRecognizer_create()
face_detector = cv2.CascadeClassifier('/home/pi/opencv/data/haarcascades/haarcascade_frontalface_default.xml')
face_id = input('\n enter user id and press <return> ==>  ')
choice, working_dir = check_id_taken()
count = 0
if choice == 1:
    face_name = input('\n enter user name and press <return> ==>  ')
    face_folder = face_id + "." + face_name
    try:
        if working_dir:
            shutil.rmtree(path + working_dir)
        os.mkdir(path + face_folder)
    except:
        print("error")
else:
    count = (len(os.listdir(path + working_dir)))
    face_folder = working_dir
print("\n [INFO] Initializing face capture. Look the camera and wait ...")
life_cycle(count)
# Do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()

def getImagesAndLabels(path):
    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]     
    faceSamples=[]
    ids = []
    for subFolder in imagePaths:
        newDir = [os.path.join(subFolder,f) for f in os.listdir(subFolder)]
        for imagePath in newDir:
            PIL_img = Image.open(imagePath).convert('L') # convert it to grayscale
            img_numpy = np.array(PIL_img,'uint8')
            id = int(os.path.split(imagePath)[-1].split(".")[0])
            print (id)
            faces = face_detector.detectMultiScale(img_numpy)
            for (x,y,w,h) in faces:
                faceSamples.append(img_numpy[y:y+h,x:x+w])
                ids.append(id)
    return faceSamples,ids
print ("\n [INFO] Training faces. It will take a few seconds. Wait ...")
faces,ids = getImagesAndLabels(path)
recognizer.train(faces, np.array(ids))
# Save the model into trainer/trainer.yml
recognizer.write('trainer/trainer.yml') # recognizer.save() worked on Mac, but not on Pi
# Print the numer of faces trained and end program
print("\n [INFO] {0} faces trained. Exiting Program".format(len(np.unique(ids))))
