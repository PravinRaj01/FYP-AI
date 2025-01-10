# firebase/firebase_config.py
import firebase_admin
from firebase_admin import credentials, auth

# Ensure Firebase initializes only once
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase/serviceAccountKey.json")
    firebase_admin.initialize_app(cred)
