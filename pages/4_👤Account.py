import streamlit as st
import firebase_admin
from firebase_admin import auth, firestore
import re
from google.auth.transport.requests import Request
from google.oauth2 import service_account
from firebase_admin import credentials
import os
from dotenv import load_dotenv
from firebase_admin import firestore
from firebase.firebase_config import firebase  # This will ensure Firebase is initialized
from firebase.firebase_config import firebase  # Ensures Firebase is initialized

# Get Firestore client
db = firestore.client()
# ✅ Centered Profile Styling
css_center_profile = """
    <style>
        .profile-container {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
        }
        .profile-pic {
            border-radius: 50%;
            width: 150px;
            height: 150px;
            object-fit: cover;
            border: 4px solid #65CCB8;
        }
        .email-link {
            font-size: 20px;
            font-weight: bold;
        }
    </style>
"""
st.markdown(css_center_profile, unsafe_allow_html=True)
st.sidebar.image("image/logo3.png", use_container_width=True)
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
        if not is_valid_email(email):
            st.error("❌ Please enter a valid email.")
        elif not password:
            st.error("❌ Please enter a password.")
        else:
            try:
                # Sign in with email and password
                user = auth.sign_in_with_email_and_password(email, password)
                st.session_state["user"] = email
                st.success(f"✅ Welcome back, {email}!")
                st.session_state["account_page"] = "profile"
                st.toast("⚠️Successfully logged in")
                st.rerun()
            except:
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
    
    # Display password requirements
    st.info("Password must contain:\n"
            "- At least 8 characters\n"
            "- One uppercase letter\n"
            "- One number\n"
            "- One special character (@$!%*?&)")

    if st.button("Sign Up"):
        if not new_email:
            st.error("❌ Please enter an email.")
        elif not is_valid_email(new_email):
            st.error("❌ Invalid email format.")
        elif not new_password:
            st.error("❌ Please enter a password.")
        elif not is_valid_password(new_password):
            st.error("❌ Password must meet all requirements.")
        else:
            try:
                # Check if email already exists
                try:
                    existing_user = auth.get_user_by_email(new_email)
                    st.error("❌ This email is already registered.")
                except:
                    # Create new user if email doesn't exist
                    auth.create_user(email=new_email, password=new_password)
                    st.success("✅ Account created successfully! Please log in.")
                    st.session_state["account_page"] = "login"
                    st.rerun()
            except Exception as e:
                st.error(f"❌ Error creating account: {str(e)}")

    if st.button("Back to Login"):
        st.session_state["account_page"] = "login"
        st.rerun()

# ✅ PROFILE PAGE (Redirects after Login)
elif st.session_state["account_page"] == "profile":
    st.subheader(f"✅ Welcome, {st.session_state['user']}!")

    # ✅ Fetch User Details and Profile Picture
    user_email = st.session_state["user"]
    user_doc_ref = db.collection("users").document(user_email)
    user_doc = user_doc_ref.get()

    # ✅ Default Profile Picture
    if user_doc.exists:
        user_data = user_doc.to_dict()
        profile_pic_url = user_data.get("profile_pic_url", "https://www.w3schools.com/w3images/avatar2.png")
    else:
        profile_pic_url = "https://www.w3schools.com/w3images/avatar2.png"

    # ✅ Display Profile Section
    st.markdown('<div class="profile-container">', unsafe_allow_html=True)
    st.markdown(f'<img src="{profile_pic_url}" class="profile-pic">', unsafe_allow_html=True)
    st.markdown(f'<p class="email-link">📧 {user_email}</p>', unsafe_allow_html=True)

    # ✅ Display Total Translations
    translations_ref = db.collection("translations").where("user", "==", user_email).stream()
    translation_count = sum(1 for _ in translations_ref)
    st.markdown(f"*Total Translations:* {translation_count}")

    # ✅ Logout Button
    if st.button("Logout"):
        st.session_state["user"] = None
        st.session_state["account_page"] = "login"
        st.success("You have been logged out.")
        st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)


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