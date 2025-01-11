import logging
import streamlit as st
from transformers import T5ForConditionalGeneration, AutoTokenizer
import torch
import firebase_admin
from firebase_admin import credentials, firestore
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
service_account_path = os.getenv("FIREBASE_KEY_PATH")

# ✅ Streamlit Page Configuration
st.set_page_config(
    page_title="ROJAK | Malaysian Code-Switched Translator",
    page_icon="image/logo4.png",
    layout="wide"
)

css_dark_mode = """
<style>
    .stApp {
        background-color: #222629;
        color: #F2F2F2;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    h1, p {
        color: #65CCB8;
        text-align: center;
    }
    .chat-container {
        width: 60%;
        max-width: 700px;
        margin: auto;
        display: flex;
        flex-direction: column;
        justify-content: center;
        align-items: center;
    }
    .chat-bubble-user {
        background-color: #65CCB8;
        color: black;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
        max-width: 70%;
        align-self: flex-end;
        text-align: right;
    }
    .chat-bubble-bot {
        background-color: #2E3238;
        color: white;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
        max-width: 70%;
        align-self: flex-start;
        text-align: left;
    }
    .stTextInput>div>div>input {
        background-color: #2E3238;
        color: #F2F2F2;
        border-radius: 8px;
        padding: 10px;
        width: 100%;
        max-width: 700px;
    }
</style>
"""
st.markdown(css_dark_mode, unsafe_allow_html=True)

# ✅ Initialize Firebase Admin SDK and Firestore
if not firebase_admin._apps:
    cred = credentials.Certificate(service_account_path)
    firebase_admin.initialize_app(cred)

db = firestore.client()

# ✅ Logging Configuration
logging.basicConfig(
    level=logging.ERROR,
    filename="error_logs.log",
    filemode="a",
    format="%(asctime)s - %(message)s"
)
logger = logging.getLogger()

# ✅ Load Model and Tokenizer (Cached)
@st.cache_resource
def load_model():
    device = "cuda" if torch.cuda.is_available() else "cpu"
    if device == "cuda":
        try:
            torch.cuda.init()  # Explicit CUDA check
            tokenizer = AutoTokenizer.from_pretrained("./fine_tuned_nanot5_model")
            model = T5ForConditionalGeneration.from_pretrained("./fine_tuned_nanot5_model")
            model.to(device)
            success_message = "✅ Fine-Tuned Model Loaded Successfully!"
        except torch.cuda.CudaError as e:
            device = "cpu"
            tokenizer = AutoTokenizer.from_pretrained('mesolitica/nanot5-small-malaysian-translation-v2')
            model = T5ForConditionalGeneration.from_pretrained('mesolitica/nanot5-small-malaysian-translation-v2')
            model.to(device)
            success_message = "⚠️ CUDA initialization error. Loaded base model on CPU."
    else:
        tokenizer = AutoTokenizer.from_pretrained('mesolitica/nanot5-small-malaysian-translation-v2')
        model = T5ForConditionalGeneration.from_pretrained('mesolitica/nanot5-small-malaysian-translation-v2')
        model.to(device)
        success_message = "⚠️ CUDA not available. Loaded base model on CPU."
    
    return model, tokenizer, device, success_message


# ✅ Cleaning Translation Results
def clean_translation(text):
    sentences = [s.strip() for s in text.split('.') if s.strip()]
    return sentences[0] if sentences else text

# ✅ Save Translation to Firestore (Auto-Save)
def save_translation_to_firestore(input_text, output_text):
    if "user" not in st.session_state or not st.session_state["user"]:
        st.warning("⚠️ Please log in to save translations.")
        return False

    try:
        db.collection("translations").add({
            "user": st.session_state["user"],
            "input_text": input_text,
            "output_text": output_text,
            "timestamp": firestore.SERVER_TIMESTAMP
        })
        st.success("✅ Translation saved successfully!")
        return True
    except Exception as e:
        st.error(f"❌ Failed to save translation: {e}")
        logger.error(f"Error saving translation: {e}")
        return False

# ✅ Main Translation Interface
def translator_page():
    model, tokenizer, device, success_message = load_model()
    st.toast(success_message)

    st.markdown('<h1 style="color: #65CCB8;">Malaysian Code-Switched Language Translator</h1>', unsafe_allow_html=True)

    if "user" not in st.session_state or not st.session_state["user"]:
        st.warning("⚠️ You are not logged in! Please log in to save translations.")

    st.markdown('<p style="font-size: 18px; color: #F2F2F2;">🤖 Enter your code-switched text below:</p>', unsafe_allow_html=True)

    # ✅ Initialize Conversation History
    if "conversation" not in st.session_state:
        st.session_state.conversation = []

    # ✅ Display Conversation History without Containers (Simplified Layout)
    for message in st.session_state.conversation:
        if message["role"] == "user":
            st.markdown(f'<p style="text-align: right; color: #65CCB8;">{message["text"]} 👤</p>', unsafe_allow_html=True)
        else:
            st.markdown(f'<p style="text-align: left; color: white;">🤖 {message["text"]}</p>', unsafe_allow_html=True)
            st.markdown("<hr style='border: 1px solid #65CCB8;'>", unsafe_allow_html=True)

    # ✅ User Input with Punctuation Handling
    chat_input = st.chat_input("Enter your code-switched text here")

    def ensure_punctuation(text):
        if text and text[-1] not in ['.', '!', '?']:
            return text + '.'
        return text

    if chat_input:
        chat_input = ensure_punctuation(chat_input)  

        try:
            st.session_state.conversation.append({"role": "user", "text": chat_input})
            prefix = "terjemah ke Inggeris: "
            input_text_prefixed = prefix + chat_input
            input_ids = tokenizer(input_text_prefixed, return_tensors="pt").input_ids.to(device)
            outputs = model.generate(input_ids, max_length=30, num_beams=2)
            translated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
            translated_text = clean_translation(translated_text)

            # ✅ Display and Save Translation
            st.session_state.conversation.append({"role": "bot", "text": translated_text})
            save_translation_to_firestore(chat_input, translated_text)
            st.rerun()

        except Exception as e:
            st.error(f"Translation error: {str(e)}")
            logger.error(f"Translation Error: {e}")

# ✅ Call the Translator Page
translator_page()

# ✅ Sidebar Footer (Info Section)
st.sidebar.image("image/logo3.png", use_container_width=True)
st.sidebar.title("Instructions")
st.sidebar.markdown("""
- **Enter Code-Switched Text**: Type your Malay-English code-switched text in the box.
- **Translation happens automatically.**
- **Save Translations**: You must log in to save translations.
""")

st.sidebar.markdown("---")
st.sidebar.markdown("""Developed by: **PRAVIN RAJ A/L MURALITHARAN**""")
st.sidebar.markdown(
    """
    [![GitHub](https://img.shields.io/badge/View%20on-GitHub-181717?style=for-the-badge&logo=github)](https://github.com/PravinRaj01/FYP-AI.git)
    """,
    unsafe_allow_html=True
)
