# firebase/firebase_config.py
import firebase_admin
from firebase_admin import credentials, auth, firestore
import streamlit as st

# ✅ Ensure Firebase is initialized only once
if not firebase_admin._apps:
    try:
        # ✅ Convert Streamlit secrets to a dictionary
        cred_dict = dict(st.secrets["FIREBASE_SERVICE_ACCOUNT"])

        # ✅ Initialize Firebase Admin SDK
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred)

        # ✅ Initialize Firestore client
        db = firestore.client()

    except Exception as e:
        st.error(f"🔥 Firebase Initialization Error: {e}")

# ✅ Export Firestore and Firebase authentication
firebase_auth = auth
