import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, GenerationConfig

class LocalLLM:
    def __init__(self, model_path: str = "meta-llama/Llama-2-7b-chat-hf"):
        # Load tokenizer and quantized model
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_path,
            load_in_8bit=True,
            device_map="auto"
        )
        # Set generation config for consistent output
        self.generation_config = GenerationConfig(
            temperature=0.3,
            max_new_tokens=150,
            top_p=0.95,
            do_sample=True
        )

    def __call__(self, prompt: str) -> str:
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        with torch.autocast(device_type=self.model.device.type):
            outputs = self.model.generate(
                **inputs,
                generation_config=self.generation_config
            )
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)