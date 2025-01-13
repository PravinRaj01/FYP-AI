import firebase_admin
from firebase_admin import credentials, firestore
import os
import json

def initialize_firebase():
    # Check if running on Streamlit Cloud using the Secrets Manager
    if os.getenv("STREAMLIT_ENV") == "cloud":
        # Load credentials from Streamlit secrets
        service_account_info = json.loads(os.getenv("FIREBASE_KEY"))
        cred = credentials.Certificate(service_account_info)
    else:
        # Load from local .env file (for localhost use)
        from dotenv import load_dotenv
        load_dotenv()
        service_account_path = os.getenv("FIREBASE_KEY_PATH")
        if not service_account_path:
            raise ValueError("FIREBASE_KEY_PATH not set in .env file.")
        cred = credentials.Certificate(service_account_path)

    # Initialize Firebase if not already done
    if not firebase_admin._apps:
        firebase_admin.initialize_app(cred)

    # Return Firestore client for use in the app
    return firestore.client()

# Initialize and return Firestore instance
db = initialize_firebase()
