import firebase_app_initializer
import json

user_data_ref = firebase_app_initializer.db.collection(u'user_data')

def update_user_history(user_id, data):
    print(user_id)
    print(json.dumps(data.__dict__, indent=4, sort_keys=True, default=str))
    doc = user_data_ref.document(str(user_id)).get()
    user_data_ref.document(str(user_id)).update({u'search_history': [data.__dict__] + doc.to_dict()["search_history"]})
