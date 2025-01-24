import firebase_admin
from firebase_admin import credentials, auth, firestore
import streamlit as st

if not firebase_admin._apps:
    try:
        cred = credentials.Certificate(st.secrets["FIREBASE_SERVICE_ACCOUNT"])  # Fetch from Streamlit secrets
        firebase_admin.initialize_app(cred)
    except Exception as e:
        st.error(f"Error initializing Firebase: {e}")

# Define authentication and database globally
firebase_auth = auth
db = firestore.client()
