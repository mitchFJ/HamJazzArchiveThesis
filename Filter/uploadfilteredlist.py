from firebase_admin import credentials
from firebase_admin import db

def upload_filtered_list():
    cred = credentials.Certificate("Data/fillius-jazz-archive-search-firebase-adminsdk-fbsvc-cda02f015f.json")
    firebase_admin.initialize_app(cred, {'databaseURL': 'https://fillius-jazz-archive-search-default-rtdb.firebaseio.com'})
    ref = db.reference('/filter_names')
    ref.update() # Upload dictionary

def upload_csv():