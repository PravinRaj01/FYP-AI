import firebase_admin
from firebase_admin import credentials, auth, firestore
import streamlit as st
import json

# Ensure Firebase initializes only once
if not firebase_admin._apps:
    try:
        # Convert Streamlit secrets to JSON
        cred_dict = json.loads(st.secrets["FIREBASE_SERVICE_ACCOUNT"])

        # Initialize Firebase Admin SDK
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred)

        # Initialize Firestore client
        db = firestore.client()

    except Exception as e:
        st.error(f"🔥 Firebase Initialization Error: {e}")

# Export Firebase authentication
firebase_auth = auth
