# create_readme.py
readme_content = '''
# ROJAK | Malaysian Code-Switched Translator 🇲🇾

This project is a **Malaysian Code-Switched Language Translator** powered by **Streamlit** and **T5 Transformers**. It allows users to translate code-switched Malay-English text into proper English using a fine-tuned T5 model.

---

## 🚀 Features

- **Real-Time Translation**: Translates Malaysian code-switched language instantly.
- **Fine-Tuned Model Support**: Fine-tuned on a specialized dataset for higher accuracy.
- **Firebase Integration**: Save translations with Firebase Firestore.
- **Modern UI Design**: Dark mode interface with a clean chat style.
- **GPU Support**: Accelerated using CUDA (NVIDIA GPUs).

---

## 📦 Project Structure

```plaintext
├── fine_tuned_nanot5_model/          # Fine-tuned T5 model directory
├── image/                            # UI assets like logo and icons
├── 🤖Home.py                         # Streamlit main application file
├── account.py                        # User authentication and profile page
├── saved.py                          # Saved translations page
├── about.py                          # About page for the project
├── requirements.txt                  # Python package dependencies
├── .env                              # Environment variables (Firebase keys)
├── cleaned_manglish.csv              # Preprocessed dataset for training
├── train_manglish.csv                # Training dataset after splitting
├── valid_manglish.csv                # Validation dataset after splitting
├── test_manglish.csv                 # Test dataset for evaluation
├── train_fine_tuned_model.py         # Script for model fine-tuning
├── evaluate_model.py                 # Evaluation script for BLEU and ROUGE scores
├── README.md                         # This file!


---

## 🛠️ Installation

1. **Clone the repository:**

```bash
git clone https://github.com/PravinRaj01/FYP-AI.git
cd FYP-AI



2. **Create a virtual environment (optional but recommended):**
```bash
python -m venv venv
source venv/bin/activate  # On Windows use: .\venv\Scripts\activate

3. **Install the dependencies:**
```bash
pip install -r requirements.txt


4. **Set up Firebase:**
Add your Firebase service account key to the root directory.
Create a .env file in the root directory and include the key path:
plaintext
Copy code
FIREBASE_KEY_PATH=serviceAccountKey.json


## ▶️ Usage
1. **Run the Streamlit App:**
```bash
streamlit run 🤖Home.py


2. **Functionalities:**
- Home: Translate code-switched Malay-English text.
- Saved: View saved translations.
- Account: Manage user login and sign-up.
- About: Learn about the project.


##🔥 Technologies Used
- Python 🐍
- Streamlit 📊
- Hugging Face Transformers 🤗
- PyTorch 🔥
- Firebase Firestore ☁️
- CUDA (for GPU Acceleration) 🚀


'''

# ✅ Writing the README content to a file and confirming success (with UTF-8 encoding)
with open("README.md", "w", encoding="utf-8") as readme_file:
    readme_file.write(readme_content)

print("✅ README.md file generated successfully!")

