#app.py
import logging
import streamlit as st
from transformers import T5ForConditionalGeneration, AutoTokenizer
import torch
import re

# Initialize logging
logging.basicConfig(
    level=logging.ERROR,
    filename="error_logs.log",
    filemode="a",
    format="%(asctime)s - %(message)s"
)
logger = logging.getLogger()

# Load the model and tokenizer
@st.cache_resource
def load_model():
    try:
        device = "cuda" if torch.cuda.is_available() else "cpu"
        tokenizer = AutoTokenizer.from_pretrained('mesolitica/nanot5-small-malaysian-translation-v2')
        model = T5ForConditionalGeneration.from_pretrained('mesolitica/nanot5-small-malaysian-translation-v2')
        model.to(device)
        return model, tokenizer, device
    except Exception as e:
        logger.error(f"Error loading model or tokenizer: {str(e)}")
        st.error("Failed to load the model. Please verify your settings.")
        st.stop()

# Define CSS for Dark Mode
css_dark_mode = """
<style>
    .stApp {
        background-color: #222629;
        color: #F2F2F2;
    }
    .sidebar .sidebar-content {
        background-color: #65CCB8;
        color: #F2F2F2;
    }
    h1, p {
        color: #65CCB8;
    }
    .stButton>button {
        color: #222629;
        background-color: #65CCB8;
        border-radius: 5px;
    }
    .stTextInput>div>div>input {
        background-color: #2E3238;
        color: #F2F2F2;
    }
</style>
"""

def clean_translation(text):
    """
    Clean translation and remove irrelevant additions
    """
    # Split into sentences
    sentences = [s.strip() for s in text.split('.') if s.strip()]
    if not sentences:
        return text
    
    # Keep only the first sentence if it contains the main action/intent
    main_sentence = sentences[0]
    
    # List of patterns that indicate an irrelevant sentence
    irrelevant_patterns = [
        r"it'?s time",
        r"let'?s go",
        r"i need to",
        r"i would like",
        r"i am going",
        r"i will",
    ]
    
    # If the first sentence matches any irrelevant pattern and there are multiple sentences,
    # try the second sentence
    if len(sentences) > 1:
        if any(re.search(pattern, main_sentence.lower()) for pattern in irrelevant_patterns):
            main_sentence = sentences[1]
    
    # Final cleanup
    main_sentence = re.sub(r'\s+', ' ', main_sentence)  # Remove extra spaces
    main_sentence = main_sentence.strip()
    
    return main_sentence + '.'

def main():
    # Streamlit Page Configuration
    st.set_page_config(
        page_title="ROJAK | Malaysian Code-Switched Language Translator",
        page_icon="image/logo4.png",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    # Apply Dark Mode
    st.markdown(css_dark_mode, unsafe_allow_html=True)

    # Sidebar
    st.sidebar.image("image/logo3.png", use_container_width=True)
    st.sidebar.title("Instructions")
    st.sidebar.markdown("""
    - **Enter Code-Switched Text**: Type your Malay-English code-switched text in the box.
    - **Translate**: Click 'Translate' to see the results.
    """)

    # Load model and tokenizer
    model, tokenizer, device = load_model()

    # Main content
    st.markdown('<h1 style="color: #65CCB8;">Malaysian Code-Switched Language Translator</h1>', unsafe_allow_html=True)
    st.markdown('<p style="font-size: 18px; color: #F2F2F2;">🤖 Enter your code-switched text below</p>', unsafe_allow_html=True)

    # Text Input
    chat_input = st.chat_input("Enter your code-switched text here")
    
    if chat_input:
        try:
            if not chat_input.strip():
                st.error("Input cannot be empty. Please enter some text.")
                return

            prefix = "terjemah ke Inggeris: "
            input_text_prefixed = prefix + chat_input

            # Generation with strict parameters
            input_ids = tokenizer(input_text_prefixed, return_tensors="pt").input_ids.to(device)
            outputs = model.generate(
                input_ids,
                max_length=30,                # Short max length
                num_beams=2,                  # Minimal beam search
                no_repeat_ngram_size=2,       # Prevent bigram repetition
                repetition_penalty=3.0,       # Very high repetition penalty
                temperature=0.2,              # Very low temperature for deterministic output
                do_sample=False,              # No sampling
                early_stopping=True,
                length_penalty=0.4,           # Stronger penalty for longer sequences
                num_return_sequences=1,
                min_length=5,                 # Allow shorter outputs
                max_new_tokens=15,            # Strict limit on new tokens
            )
            translated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

            # Clean the translation
            translated_text = clean_translation(translated_text)

            # Display results
            st.markdown('<h2 style="color: #65CCB8;">Inputted Text:</h2>', unsafe_allow_html=True)
            st.markdown(f'<p style="font-size: 18px; color: #F2F2F2;">{chat_input}</p>', unsafe_allow_html=True)

            st.markdown('<h2 style="color: #65CCB8;">Translated Text:</h2>', unsafe_allow_html=True)
            st.markdown(f'<p style="font-size: 18px; color: #F2F2F2;">{translated_text}</p>', unsafe_allow_html=True)

        except Exception as e:
            logger.error(f"Error during translation: {str(e)}")
            st.error("An unexpected error occurred. Please try again.")

    # About Section in Sidebar
    st.sidebar.markdown("---")

    # About Section
    st.sidebar.title("About")
    markdown = """
    This is a machine translation system developed to translate Malaysian code-switched language using Large Language Model (LLM).

    &nbsp;
    &nbsp;

    This translator can translate "Malay - English" code-switched language to "English".

    &nbsp;
    &nbsp;

    Developed by:
    **PRAVIN RAJ A/L MURALITHARAN**
    """
    st.sidebar.info(markdown)
    st.sidebar.markdown(
        """
        [![GitHub](https://img.shields.io/badge/View%20on-GitHub-181717?style=for-the-badge&logo=github)](https://github.com/PravinRaj01/ProductivityManager-JamAI.git)
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()