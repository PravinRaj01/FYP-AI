import streamlit as st
import os
import re
from firebase.firebase_config import firebase_auth  # Import the initialized authentication instance
import firebase_admin
from firebase_admin import auth, firestore, credentials

# Ensure Firebase is initialized
if not firebase_admin._apps:
    st.error("Firebase is not initialized. Check configuration.")
    cred = credentials.Certificate("path/to/serviceAccountKey.json")  # Ensure correct path
    firebase_admin.initialize_app(cred)

db = firestore.client()  # Initialize Firestore client

# ✅ Email and Password Validation
def is_valid_email(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def is_valid_password(password):
    return bool(re.match(r"^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$", password))

# ✅ Title
st.title("👤 Account Management")

# ✅ Initialize State
if "account_page" not in st.session_state:
    st.session_state["account_page"] = "login"

# ✅ LOGIN FORM
if st.session_state["account_page"] == "login":
    st.subheader("🔐 Login")
    email = st.text_input("Enter your email")
    password = st.text_input("Enter your password", type="password")

    if st.button("Login"):
        email = st.text_input("Enter your email")  # Define email before use
        password = st.text_input("Enter your password", type="password")

        if not email:
            st.error("❌ Please enter an email.")
        elif not password:
            st.error("❌ Please enter a password.")
        else:
            try:
                user = auth.get_user_by_email(email)  # Ensure authentication is correct
                st.success(f"✅ Welcome back, {email}!")  # ✅ Email is defined before use
                st.session_state["user"] = email
                st.session_state["account_page"] = "profile"
                st.rerun()
            except firebase_admin.auth.UserNotFoundError:
                st.error("❌ Invalid email or password.")


    # ✅ Password Reset Redirect
    if st.button("Forgot Password?"):
        st.session_state["account_page"] = "password_reset"
        st.rerun()

    if st.button("Go to Sign Up"):
        st.session_state["account_page"] = "signup"
        st.rerun()

# ✅ SIGN-UP FORM
elif st.session_state["account_page"] == "signup":
    st.subheader("📝 Create an Account")
    new_email = st.text_input("Enter your email for sign up")
    new_password = st.text_input("Create a password", type="password")
    confirm_password = st.text_input("Confirm password", type="password")

    # Display password requirements
    st.info("Password must contain:\n"
            "- At least 8 characters\n"
            "- One uppercase letter\n"
            "- One number\n"
            "- One special character (@$!%*?&)")

    if st.button("Sign Up"):
        if not is_valid_email(new_email):
            st.error("❌ Invalid email format.")
        elif new_password != confirm_password:
            st.error("❌ Passwords do not match.")
        elif not is_valid_password(new_password):
            st.error("❌ Password must meet all requirements.")
        else:
            try:
                # ✅ Create a new user
                user = firebase_auth.create_user(email=new_email, password=new_password)
                st.toast("✅ Account created successfully! Please log in.")
                st.session_state["account_page"] = "login"
                st.rerun()
            except Exception as e:
                st.error(f"❌ Error creating account: {e}")

    if st.button("Back to Login"):
        st.session_state["account_page"] = "login"
        st.rerun()

# ✅ PROFILE PAGE
elif st.session_state["account_page"] == "profile":
    st.subheader(f"✅ Welcome, {st.session_state['user']}!")

    # ✅ Fetch user data from Firestore
    user_email = st.session_state["user"]
    user_doc_ref = db.collection("users").document(user_email)
    user_doc = user_doc_ref.get()

    if user_doc.exists:
        user_data = user_doc.to_dict()
        profile_pic_url = user_data.get("profile_pic_url", "https://www.w3schools.com/w3images/avatar2.png")
    else:
        profile_pic_url = "https://www.w3schools.com/w3images/avatar2.png"

    # ✅ Display user profile
    st.image(profile_pic_url, width=150)
    st.markdown(f"📧 **Email:** {user_email}")

    # ✅ Fetch and display total translations
    translations_ref = db.collection("translations").where("user", "==", user_email).stream()
    translation_count = sum(1 for _ in translations_ref)
    st.markdown(f"📄 **Total Translations:** {translation_count}")

    # ✅ Logout Button
    if st.button("Logout"):
        st.session_state["user"] = None
        st.session_state["account_page"] = "login"
        st.success("You have been logged out.")
        st.rerun()


# ✅ PASSWORD RESET PAGE (with Email Verification)
elif st.session_state["account_page"] == "password_reset":
    st.subheader("🔑 Password Reset")
    reset_email = st.text_input("Enter your email for password reset")

    if st.button("Send Password Reset Email"):
        try:
            # ✅ Check if the email exists before sending the reset link
            auth.get_user_by_email(reset_email)
            # ✅ If it exists, generate a reset link
            link = auth.generate_password_reset_link(reset_email)
            st.success(f"✅ Password reset link sent to: {reset_email}")
            st.info("Check your inbox for the reset link.")
        except firebase_admin.auth.UserNotFoundError:
            st.error("❌ This email is not registered. Please Sign Up.")
        except Exception as e:
            st.error(f"❌ Error sending reset email: {str(e)}")

    if st.button("Back to Login"):
        st.session_state["account_page"] = "login"
        st.rerun()
    
    if st.button("Go to Sign Up"):
        st.session_state["account_page"] = "signup"
        st.rerun()