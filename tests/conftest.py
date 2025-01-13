import pytest
from Home import load_model

@pytest.fixture(scope="module")
def load_translation_model():
    model, tokenizer, device, success_message = load_model()
    return model, tokenizer, device
