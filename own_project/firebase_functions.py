import firebase_admin
import datetime
import os
from firebase_admin import credentials, firestore, storage
from face_dataset import remove_tmp_pictures

def download_user_picture(path, bucket):
    blob_iter = bucket.list_blobs(delimiter='/', prefix="user_picture/")
    prefixes = set()
    id = 0
    for page in blob_iter.pages:
        prefixes.update(page.prefixes)
    for url in prefixes:
        blob_iter = bucket.list_blobs(delimiter='/', prefix=url)
        all_img_of_user = set()
        count = 0
        for single_img in blob_iter:
            print (single_img.name)
            blob = bucket.blob(single_img.name)
            with open(path  + "/" + str(id) + "." + str(count) + ".jpg", "wb") as file_obj:
                blob.download_to_file(file_obj)
            count += 1
        id += 1

def download_trained_data(bucket):
    path = "tmp/trainer.yml"
    blob = bucket.blob(path)
    try:
        os.mkdir("./tmp")
    except:
        pass
    with open(path, "wb") as file_obj:
        blob.download_to_file(file_obj)


def upload_trained_data(path, bucket):
        imageBlob = bucket.blob(path)
        imageBlob.upload_from_filename("tmp/trainer.yml")
        # remove_tmp_pictures("yml")