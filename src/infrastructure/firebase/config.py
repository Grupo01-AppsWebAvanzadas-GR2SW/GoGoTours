import firebase_admin
from firebase_admin import credentials
from firebase_admin import db


def initialize_firebase():
    cred = credentials.Certificate("config/firebase-credentials.json")
    firebase_admin.initialize_app(cred)
