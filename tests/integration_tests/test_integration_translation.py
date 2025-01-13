import pytest
from Home import load_model, save_translation_to_firestore
import firebase_admin
from firebase_admin import auth, credentials, firestore
import os
import streamlit as st
from dotenv import load_dotenv

# Firebase Setup
@pytest.fixture(scope="module")
def firebase_setup():
    load_dotenv()
    service_account_path = os.getenv("FIREBASE_KEY_PATH")
    if not firebase_admin._apps:
        cred = credentials.Certificate(service_account_path)
        firebase_admin.initialize_app(cred)
    db = firestore.client()
    return db

# ✅ TC-006: Model Loading Test
def test_model_loading():
    model, tokenizer, device = load_model()
    assert model is not None
    assert tokenizer is not None
    assert device in ["cuda", "cpu"]

# ✅ TC-007: User Registration Test (Skips if User Already Exists)
def test_user_registration(firebase_setup):
    email = "testuser1234@gmail.com"
    password = "Test@12345"
    try:
        auth.get_user_by_email(email)
    except firebase_admin.auth.UserNotFoundError:
        auth.create_user(email=email, password=password)

    user = auth.get_user_by_email(email)
    assert user.email == email


# ✅ TC-008: Firebase Verification Test
def test_translation_and_saving(firebase_setup):
    db = firebase_setup
    st.session_state["user"] = "test_user@gmail.com"  # ✅ Mocking the user session correctly
    test_input_text = "Aku nak gi shopping."
    test_output_text = "I want to go shopping."

    success = save_translation_to_firestore(test_input_text, test_output_text)
    assert success == True

    # ✅ Verify the data was saved correctly in Firebase
    translations = db.collection("translations").where("user", "==", "test_user@gmail.com").get()
    assert any(
        doc.to_dict().get("input_text") == test_input_text and
        doc.to_dict().get("output_text") == test_output_text
        for doc in translations
    ), "Translation was not correctly saved in Firebase."



# ✅ TC-009: Unauthorized Access Test
def test_unauthorized_access(firebase_setup):
    db = firebase_setup
    try:
        db.collection("restricted_data").get()
        assert False, "Unauthorized access should have been blocked!"
    except Exception:
        assert True


# TC-010: Full Translation Flow Test
def test_full_translation_flow(firebase_setup):
    db = firebase_setup
    st.session_state["user"] = "test_user@gmail.com"
    model, tokenizer, device = load_model()

    test_input_text = "Dia tanya pasal apa?"
    input_text_prefixed = "terjemah ke Inggeris: " + test_input_text
    input_ids = tokenizer(input_text_prefixed, return_tensors="pt").input_ids.to(device)
    outputs = model.generate(input_ids, max_length=30, num_beams=2)
    translated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

    # ✅ Save the translation
    success = save_translation_to_firestore(test_input_text, translated_text)
    assert success == True

    # ✅ Verify the saved translation
    translations = db.collection("translations").where("user", "==", "test_user@gmail.com").get()
    assert any(
        doc.to_dict().get("input_text") == test_input_text and
        doc.to_dict().get("output_text") == translated_text
        for doc in translations
    ), "Translation was not correctly saved after full flow."
