import firebase_admin
from firebase_admin import credentials, firestore

# ✅ Initialize Firebase Admin SDK (Ensure this path is correct)
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase/serviceAccountKey.json")
    firebase_admin.initialize_app(cred)

# ✅ Initialize Firestore Client
db = firestore.client()

# ✅ Function to Verify Firestore Connection
def verify_firestore_connection():
    try:
        # ✅ Write Test Data
        test_data = {
            "test_field": "Testing Firestore Connection",
            "timestamp": firestore.SERVER_TIMESTAMP
        }
        doc_ref = db.collection("test_collection").document("test_document")
        doc_ref.set(test_data)
        print("✅ Data successfully written to Firestore!")

        # ✅ Read Test Data
        retrieved_data = doc_ref.get()
        if retrieved_data.exists:
            print(f"✅ Data retrieved successfully: {retrieved_data.to_dict()}")
        else:
            print("❌ No data found!")
    except Exception as e:
        print(f"❌ Error connecting to Firestore: {e}")

# ✅ Run the Test
verify_firestore_connection()
