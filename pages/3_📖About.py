import streamlit as st
import firebase_admin
from firebase_admin import firestore
from firebase_admin import firestore

from firebase.firebase_config import firebase_auth  # Import Firebase Authentication
from firebase_admin import firestore
st.title("📖 About This App")
st.markdown("""
This application is designed to translate Malaysian code-switched language using a fine-tuned *T5 model*.
It supports *Malay-English* translations and is part of a research project for code-switched language translation.

---

## 🚀 Features

- *Real-Time Translation*: Translates Malaysian code-switched language instantly.
- *Fine-Tuned Model Support*: Fine-tuned on a specialized dataset for higher accuracy.
- *Firebase Integration*: Save translations with Firebase Firestore.
- *Modern UI Design*: Dark mode interface with a clean chat style.
- *GPU Support*: Accelerated using CUDA (NVIDIA GPUs).

---

## 🔥 Technologies Used
- Python 🐍
- Streamlit 📊
- Hugging Face Transformers 🤗
- PyTorch 🔥
- Firebase Firestore ☁️
- CUDA (for GPU Acceleration) 🚀
        
            
""")

st.markdown("---")
st.markdown("""Developed by: *PRAVIN RAJ A/L MURALITHARAN*""")
st.markdown(
    """
    [![GitHub](https://img.shields.io/badge/View%20on-GitHub-181717?style=for-the-badge&logo=github)](https://github.com/PravinRaj01/FYP-AI.git)
    """,
    unsafe_allow_html=True
)



# ✅ Ensure Firestore client is obtained within the file
db = firestore.client()
# ✅ Sidebar Logout Button Implementation with Email Display
def sidebar_with_logout():
    st.sidebar.image("image/logo3.png", use_container_width=True)
    
    # ✅ Display user email and logout button if logged in
    if "user" in st.session_state and st.session_state["user"]:
        st.sidebar.markdown(f"*✅ Logged in as:* {st.session_state['user']}")
        if st.sidebar.button("🚪 Logout"):
            st.session_state["user"] = None
            st.session_state["account_page"] = "login"
            st.toast("✅ Successfully logged out!")
            st.rerun()
    else:
        st.sidebar.warning("⚠️ Not logged in!")
        

# ✅ Apply the sidebar fu nction
sidebar_with_logout()