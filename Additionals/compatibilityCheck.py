from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig
import torch

# ✅ Config for 4-bit NF4 Quantization
nf4_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type='nf4',
    bnb_4bit_use_double_quant=True,
    bnb_4bit_compute_dtype=torch.bfloat16
)

# ✅ Load the model and tokenizer with 4-bit compression
tokenizer = AutoTokenizer.from_pretrained("mesolitica/mallam-1.1B-4096")
model = AutoModelForCausalLM.from_pretrained(
    "mesolitica/mallam-1.1B-4096",
    quantization_config=nf4_config
).to("cuda")  # ✅ 4-bit supports .to("cuda")

print("✅ Model loaded successfully using 4-bit quantization!")
