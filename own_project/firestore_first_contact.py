from face_dataset import take_picture, remove_tmp_pictures
from text_to_speech import say_out_loud
from qr_code_reader import search_qr_code
from train_ml import initiate_image_training
from firebase_functions import download_trained_data
import os.path
from os import path
from face_recognition import face_recognition_starter
from multiprocessing import Process
import firebase_app_initializer
from firestore_functions import update_user_history
from face_recognition import request_summary

user_list = []

class user_minimal_info:
    def __init__(self, id, name):
        self.id = id
        self.name = name  

def update_user(id, data):
        user_data_ref.document(id).update(data)

def raspberry_on_off(doc_snapshot, changes, read_time):
    global start_proc
    
    for doc in doc_snapshot:
        if (doc.to_dict()["is_launched"] == True):
            print ("ON")
            say_out_loud("Turning program on")
            if (not path.exists("tmp/trainer.yml")):
                say_out_loud("Downloading faces, wait for a bit.")
                download_trained_data(firebase_app_initializer.bucket)
                say_out_loud("Done.")
            face_recognition_starter(user_list)
            # start_proc.start()
        else:
            print ("OFF")
            say_out_loud("Turning program off")
            # remove_tmp_pictures("yml")
            # try:
            #     start_proc.terminate()
            #     start_proc = Process(target=face_recognition_starter, args=(user_list, ))
            # except:
            #     pass

def check_user_photos_request(doc_snapshot, changes, read_time):
    for doc in doc_snapshot:
        update_user(doc.to_dict()["id"], {u'request_photos': False})
        print (doc.to_dict()["name"] + " request new photos")
        say_out_loud("Taking pictures of " + doc.to_dict()["name"])
        image_list, image_path = take_picture(doc.to_dict())
        if len(image_list) > 0:
            say_out_loud("Done.")
            say_out_loud("Sending the photos on the cloud.")
            for i in range(len(image_list)):
                imageBlob = firebase_app_initializer.bucket.blob(image_list[i])
                imageBlob.upload_from_filename(image_path[i])
            user_data_ref.document(doc.to_dict()["id"]).update({u'photos': doc.to_dict()["photos"] + image_list})
            remove_tmp_pictures("jpg")
            say_out_loud("Done.")

def check_train_request(doc_snapshot, changes, read_time):
        for doc in doc_snapshot:
            say_out_loud("Start training on your images. It will take some time.")
            initiate_image_training(doc.to_dict(), firebase_app_initializer.bucket)
            update_user(doc.to_dict()["id"], {u'request_train': False})
            say_out_loud("Done.")

def security_check(doc_snapshot, changes, read_time):
    for doc in doc_snapshot:
        say_out_loud("Show the QR code to the camera")
        phone_code = search_qr_code()
        if phone_code == doc.to_dict()["uid"]:
            update_user(doc.to_dict()["id"], {u'accept_modify_account': True, u'request_security_check': False})
        else:
            say_out_loud("Wrong QR Code")
            update_user(doc.to_dict()["id"], {u'request_security_check': False})

user_data_ref = firebase_app_initializer.db.collection(u'user_data')
python_function_ref = firebase_app_initializer.db.collection(u'python_function')
doc_ref_is_working = python_function_ref.document(u'g9y4AYxRUFBkTnUDvxW2')
doc_ref_request_photos = user_data_ref.where(u'request_photos', u'==',True)
doc_ref_request_security_check = user_data_ref.where(u'request_security_check', u'==',True)
doc_ref_request_train = user_data_ref.where(u'request_train', u'==',True)

doc_watch_is_working = doc_ref_is_working.on_snapshot(raspberry_on_off)
doc_watch_request_photos = doc_ref_request_photos.on_snapshot(check_user_photos_request)
doc_watch_request_security_check = doc_ref_request_security_check.on_snapshot(security_check)
doc_watch_request_train = doc_ref_request_train.on_snapshot(check_train_request)
for doc in user_data_ref.stream():
    user_list.append(user_minimal_info(doc.id, doc.to_dict()["name"]))
start_proc = Process(target=face_recognition_starter, args=(user_list, ))
while True:
    x = 1