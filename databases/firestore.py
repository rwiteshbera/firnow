import firebase_admin
from firebase_admin import credentials, firestore_async

from settings import config

cert: str = config["FIRESTORE_CERT"] or ""

cred = credentials.Certificate(cert)
app = firebase_admin.initialize_app(cred)
db = firestore_async.client(app)
