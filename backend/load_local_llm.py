from transformers import AutoTokenizer, AutoModelForCausalLM
import os
from dotenv import load_dotenv
from huggingface_hub import login

"""
The purpose of this script is to load a local LLM model (Llama-2-7b-chat) in 8-bit quantization.
The model will be saved on disk for faster reloading in future runs.
"""

# Load environment variables from .env file
load_dotenv()

huggingface_token = os.getenv("HUGGING_FACE_TOKEN")
login(huggingface_token)

# 1) Load tokenizer
tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-chat-hf")

# 2) Load model in 8-bit
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-2-7b-chat-hf",
    load_in_8bit=True,
    device_map="auto"
)

# 3) (Optional) Save quantized model for faster reload
model.save_pretrained("./models/llama2-7b-8bit")
tokenizer.save_pretrained("./models/llama2-7b-8bit")