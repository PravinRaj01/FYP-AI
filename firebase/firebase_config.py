import firebase_admin
from firebase_admin import credentials, firestore
import os
import json
from dotenv import load_dotenv

def initialize_firebase():
    """Initialize Firebase for both Local and Streamlit Cloud."""
    if os.getenv("STREAMLIT_ENV") == "cloud":
        try:
            # Load Streamlit Secret using TOML format (preloaded by Streamlit)
            service_account_info = {
                "type": os.getenv("FIREBASE_KEY_type"),
                "project_id": os.getenv("FIREBASE_KEY_project_id"),
                "private_key_id": os.getenv("FIREBASE_KEY_private_key_id"),
                "private_key": os.getenv("FIREBASE_KEY_private_key").replace("\\n", "\n"),
                "client_email": os.getenv("FIREBASE_KEY_client_email"),
                "client_id": os.getenv("FIREBASE_KEY_client_id"),
                "auth_uri": os.getenv("FIREBASE_KEY_auth_uri"),
                "token_uri": os.getenv("FIREBASE_KEY_token_uri"),
                "auth_provider_x509_cert_url": os.getenv("FIREBASE_KEY_auth_provider_x509_cert_url"),
                "client_x509_cert_url": os.getenv("FIREBASE_KEY_client_x509_cert_url"),
            }
            cred = credentials.Certificate(service_account_info)
        except Exception as e:
            raise ValueError(f"Error loading Firebase credentials from Streamlit Secrets: {e}")
    else:
        # Local Environment with .env
        load_dotenv()
        service_account_path = os.getenv("FIREBASE_KEY_PATH")
        if not service_account_path:
            raise ValueError("FIREBASE_KEY_PATH not set in .env file.")
        cred = credentials.Certificate(service_account_path)

    # Initialize Firebase if not already done
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)

    return firestore.client()

# ✅ Initialize Firestore globally
db = initialize_firebase()
