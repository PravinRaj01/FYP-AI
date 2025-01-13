import pytest
from Home import load_model, clean_translation
from transformers import T5ForConditionalGeneration, AutoTokenizer
import torch

# ✅ TC-001: Tokenizer Behavior Test
def test_tokenizer_behavior():
    model, tokenizer, device = load_model()  # Fixed here
    input_text = "Saya lapar."
    tokens = tokenizer(input_text, return_tensors="pt")
    assert tokens is not None
    assert "input_ids" in tokens

# ✅ TC-002: Simple Translation Test
def test_simple_translation():
    model, tokenizer, device = load_model()
    input_text = "terjemah ke Inggeris: Saya lapar."
    input_ids = tokenizer(input_text, return_tensors="pt").input_ids.to(device)
    outputs = model.generate(input_ids, max_length=30, num_beams=2)
    translated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    assert "hungry" in translated_text.lower()  # Allow flexible matching


# ✅ TC-003: Mixed Translation Test
def test_mixed_translation():
    model, tokenizer, device = load_model()
    input_text = "terjemah ke Inggeris: Aku nak eat."
    input_ids = tokenizer(input_text, return_tensors="pt").input_ids.to(device)
    outputs = model.generate(input_ids, max_length=30, num_beams=2)
    translated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    assert "eat" in translated_text.lower()  # Allow flexible matching

#✅ TC-004: Empty Input Handling Test
def ensure_punctuation(text):
    if not text.strip():
        raise ValueError("Input cannot be empty. Please enter some text.")
    if text and text[-1] not in ['.', '!', '?']:
        return text + '.'
    return text

def test_empty_input():
    with pytest.raises(ValueError):
        ensure_punctuation("")


# ✅ TC-005: Invalid Input Handling Test
def test_invalid_input():
    model, tokenizer, device = load_model()
    invalid_text = "terjemah ke Inggeris: @#$%^&*"
    input_ids = tokenizer(invalid_text, return_tensors="pt").input_ids.to(device)
    outputs = model.generate(input_ids, max_length=30, num_beams=2)
    translated_text = tokenizer.decode(outputs[0], skip_special_tokens=True)
    assert any(word in translated_text.lower() for word in ["invalid", "error", "@#$%"])  # More flexible matching
