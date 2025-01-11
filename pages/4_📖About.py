import streamlit as st

st.title("📖 About This App")
st.markdown("""
This application is designed to translate Malaysian code-switched language using a fine-tuned **T5 model**.
It supports **Malay-English** translations and is part of a research project for code-switched language translation.

---

## 🚀 Features

- **Real-Time Translation**: Translates Malaysian code-switched language instantly.
- **Fine-Tuned Model Support**: Fine-tuned on a specialized dataset for higher accuracy.
- **Firebase Integration**: Save translations with Firebase Firestore.
- **Modern UI Design**: Dark mode interface with a clean chat style.
- **GPU Support**: Accelerated using CUDA (NVIDIA GPUs).

---

## 🔥 Technologies Used
- Python 🐍
- Streamlit 📊
- Hugging Face Transformers 🤗
- PyTorch 🔥
- Firebase Firestore ☁️
- CUDA (for GPU Acceleration) 🚀
        
            
""")
