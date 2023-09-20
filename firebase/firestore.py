import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore_async

cred = credentials.Certificate(
    "firebase/firnow-12092023-firebase-adminsdk-wzo4l-bba1a3ce63.json"
)
app = firebase_admin.initialize_app(cred)
db = firestore_async.client(app)
