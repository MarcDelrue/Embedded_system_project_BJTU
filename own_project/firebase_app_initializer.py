import firebase_admin
from firebase_admin import credentials, firestore, storage

cred = credentials.Certificate("./config/coronavirus-user-data-firebase-adminsdk-srsr6-1703c50010.json")
firebase_admin.initialize_app(cred, {'storageBucket': 'coronavirus-user-data.appspot.com'})
bucket = storage.bucket()
db = firestore.client()