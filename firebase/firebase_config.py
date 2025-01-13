# firebase/firebase_config.py
import firebase_admin
from firebase_admin import credentials
import streamlit as st
import json

def initialize_firebase():
    if not firebase_admin._apps:
        try:
            # For production (Streamlit Cloud)
            if 'FIREBASE_SERVICE_ACCOUNT' in st.secrets:
                cred = credentials.Certificate(
                    json.loads(st.secrets["FIREBASE_SERVICE_ACCOUNT"])
                )
            # For local development
            else:
                import os
                from dotenv import load_dotenv
                load_dotenv()
                service_account_path = os.getenv("FIREBASE_KEY_PATH")
                cred = credentials.Certificate(service_account_path)
            
            firebase_admin.initialize_app(cred)
        except Exception as e:
            st.error(f"Error initializing Firebase: {e}")
    
    return firebase_admin

# Initialize Firebase when this module is imported
firebase = initialize_firebase()