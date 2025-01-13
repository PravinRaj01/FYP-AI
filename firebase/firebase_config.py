# firebase/firebase_config.py
import firebase_admin
from firebase_admin import credentials, auth
import streamlit as st

if not firebase_admin._apps:
    try:
        # Create a dictionary with the secrets
        cred_dict = {
            "type": st.secrets.FIREBASE_SERVICE_ACCOUNT.type,
            "project_id": st.secrets.FIREBASE_SERVICE_ACCOUNT.project_id,
            "private_key": st.secrets.FIREBASE_SERVICE_ACCOUNT.private_key,
            "client_email": st.secrets.FIREBASE_SERVICE_ACCOUNT.client_email,
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": f"https://www.googleapis.com/robot/v1/metadata/x509/{st.secrets.FIREBASE_SERVICE_ACCOUNT.client_email}"
        }
        cred = credentials.Certificate(cred_dict)
        firebase_admin.initialize_app(cred)
    except Exception as e:
        st.error(f"Error initializing Firebase: {e}")

firebase = firebase_admin
firebase_auth = auth
