import cv2
import numpy as np
from PIL import Image
from firebase_functions import download_user_picture, upload_trained_data
from face_dataset import remove_tmp_pictures
import os

recognizer = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier("/home/pi/opencv/data/haarcascades/haarcascade_frontalface_default.xml")
path = "./tmp"

def getImagesAndLabels(path):
    faceSamples=[]
    ids = []
    imagePaths = [os.path.join(path,f) for f in os.listdir(path)]
    for imagePath in imagePaths:
        if (imagePath.find(".jpg") != -1):
            PIL_img = Image.open(imagePath).convert('L')
            img_numpy = np.array(PIL_img,'uint8')
            id = os.path.split(imagePath)[-1].split(".")[0]
            faces = detector.detectMultiScale(img_numpy)
            for (x,y,w,h) in faces:
                faceSamples.append(img_numpy[y:y+h,x:x+w])
                ids.append(int(id))
    return faceSamples,ids

def download_images(user, bucket):
    try:
        os.mkdir(path)
    except:
        pass
    download_user_picture(path, bucket)

def initiate_image_training(user, bucket):
    print ("\n [INFO] Training faces. It will take a few seconds. Wait ...")
    download_images(user, bucket)
    faces,ids = getImagesAndLabels(path)
    recognizer.train(faces, np.array(ids))
    recognizer.write('tmp/trainer.yml')
    upload_trained_data('tmp/trainer.yml', bucket)
    remove_tmp_pictures("jpg")
    print("\n [INFO] {0} faces trained. Exiting Program".format(len(np.unique(ids))))