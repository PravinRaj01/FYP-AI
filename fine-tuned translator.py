import logging
import streamlit as st
from transformers import BartForConditionalGeneration, AutoTokenizer


# Initialize logging
logging.basicConfig(
    level=logging.ERROR,
    filename="error_logs.log",
    filemode="a",
    format="%(asctime)s - %(message)s"
)
logger = logging.getLogger()


# Load the fine-tuned model and tokenizer with error handling
@st.cache_resource
def load_model():
    try:
        device = "cpu"  # Use CPU for inference
        model = BartForConditionalGeneration.from_pretrained("./fine_tuned_bart").to(device)
        tokenizer = AutoTokenizer.from_pretrained("./fine_tuned_bart")
        return model, tokenizer
    except Exception as e:
        logger.error(f"Error loading model or tokenizer: {str(e)}")
        st.error("Failed to load the model. Please check the model path or configuration.")
        st.stop()  # Stop further execution


# Streamlit Page Configuration
st.set_page_config(
    page_title="ROJAK | Malaysian Code-Switched Language Translator",
    page_icon="image/logo4.png",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Get help": "https://github.com/PravinRaj01/",
        "Report a bug": "https://github.com/PravinRaj01/",
        "About": """
            ## Malaysian Code-Switched Language Translator
            
            **GitHub**: https://github.com/PravinRaj01/
            
            This is a machine translation system developed to
            translate Malaysian code-switched language using Large Language Model (LLM).
            This translator can translate "Malay - English" code-switched language to "English".

            Developed by:
            **PRAVIN RAJ A/L MURALITHARAN**
        """
    }
)

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
</style>
"""

# Apply Dark Mode
st.markdown(css_dark_mode, unsafe_allow_html=True)

def slang_translation_fallback(input_text):
    fallback_dict = {
        "dekat": "at",
        "gi": "go",
        "pasal": "about",
        "macam": "like",
        "kan": "right",
        "tak": "not",
        "lah": "",  # Remove filler words if needed
    # Add more slang words as required
    }

    words = input_text.split()
    return " ".join([fallback_dict.get(word, word) for word in words])

def main():
    # Ensure compatibility with the latest Streamlit
    try:
        st.sidebar.image("image/logo3.png", use_container_width=True)
    except TypeError:
        st.sidebar.image("image/logo3.png", use_column_width=True)

    # Sidebar Content
    st.sidebar.title("Basic Instructions")
    st.sidebar.markdown("""
    - **Enter Code-Switched Text**: Type your Malay-English code-switched text in the prompt box.
    - **Translate**: Click the 'Send' icon to translate the text to English.
    - **View Results**: The translated text will be displayed above the prompt box.
    """)

    # Load the model and tokenizer
    model, tokenizer = load_model()

    # Title and Input Section
    st.markdown('<h1 style="color: #65CCB8;">Malaysian Code-Switched Language Translator</h1>', unsafe_allow_html=True)
    st.markdown('<p style="font-size: 18px; color: #F2F2F2;">🤖 Enter your code-switched text in the prompt box below</p>', unsafe_allow_html=True)

    # Chat Input Placeholder
    chat_input = st.chat_input("Enter your code-switched text here")
    
    if chat_input:
        try:
            # Validate Input
            if not chat_input.strip():
                st.error("Input cannot be empty. Please enter some text.")
                return

            # Apply slang fallback translation
            preprocessed_text = slang_translation_fallback(chat_input)

            # Process input and generate translation
            input_ids = tokenizer.encode(preprocessed_text, return_tensors="pt").to("cpu")
            outputs = model.generate(input_ids, max_length=256, num_beams=4, early_stopping=True)
            translated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)

            # Display Inputed Text
            st.markdown('<h2 style="color: #65CCB8;">Inputed Text:</h2>', unsafe_allow_html=True)
            st.markdown(f'<p style="font-size: 18px; color: #F2F2F2;">{chat_input}</p>', unsafe_allow_html=True)

            # Display translated text
            st.markdown('<h2 style="color: #65CCB8;">Translated Text:</h2>', unsafe_allow_html=True)
            st.markdown(f'<p style="font-size: 18px; color: #F2F2F2;">{translated_text}</p>', unsafe_allow_html=True)

        except Exception as e:
            logger.error(f"Error during translation: {str(e)}")
            st.error("An unexpected error occurred while processing the translation. Please try again.")

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
