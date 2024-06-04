import firebase_admin
from firebase_admin import credentials, firestore_async

from config import settings

cred = credentials.Certificate(settings.FIRESTORE_CERT)
app = firebase_admin.initialize_app(cred)
db = firestore_async.client(app)
