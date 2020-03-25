import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
import time
from face_dataset import take_picture
from text_to_speech import say_out_loud

cred = credentials.Certificate("./config/coronavirus-user-data-firebase-adminsdk-srsr6-1703c50010.json")
firebase_admin.initialize_app(cred)

db = firestore.client()

def raspberry_on_off(doc_snapshot, changes, read_time):
    for doc in doc_snapshot:
        if (doc.to_dict()["is_launched"] == True):
            print ("ON")
        else:
            print ("OFF")

def check_user_request(doc_snapshot, changes, read_time):
    for doc in doc_snapshot:
        user_data_ref.document(doc.to_dict()["id"]).update({u'request_photos': False})
        print (doc.to_dict()["name"] + " request new photos")
        say_out_loud("Taking pictures of " + doc.to_dict()["name"])
        take_picture()
        say_out_loud("Done.")

user_data_ref = db.collection(u'user_data')
python_function_ref = db.collection(u'python_function')
doc_ref_is_working = python_function_ref.document(u'g9y4AYxRUFBkTnUDvxW2')
doc_ref_request_photos = user_data_ref.where(u'request_photos', u'==',True)

doc_watch_is_working = doc_ref_is_working.on_snapshot(raspberry_on_off)
doc_watch_request_photos = doc_ref_request_photos.on_snapshot(check_user_request)
while True:
    x = 1