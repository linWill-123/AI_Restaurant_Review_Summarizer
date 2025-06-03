import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, GenerationConfig
from langchain.schema import LLMResult, Generation, ChatGeneration
from langchain.schema.runnable import Runnable
from typing import Any, Mapping, Optional

class LocalLLMRunnable(Runnable):
    def __init__(self, local_llm):
        self.local_llm = local_llm

    def invoke(self, input: Any, config: Optional[Mapping[str, Any]] = None, **kwargs: Any) -> str:
        # Debug print to see what we're receiving
        print("Input received:", input)
        
        # Extract the prompt from the input
        if isinstance(input, dict):
            # Handle dictionary input
            prompt = ""
            for key in ['attribute', 'snippets']:
                if key in input:
                    prompt += f"{key}: {input[key]}\n"
        elif isinstance(input, str):
            prompt = input
        else:
            prompt = str(input)
            
        print("Formatted prompt:", prompt)  # Debug print
        return self.local_llm(prompt)

class LocalLLM:
    def __init__(self, model_path: str = "meta-llama/Llama-2-7b-chat-hf"):
        # Load tokenizer and quantized model, comment out the `load_in_8bit` line if you want to use the full precision model
        self.tokenizer = AutoTokenizer.from_pretrained(model_path)
        self.model = AutoModelForCausalLM.from_pretrained(
            model_path,
            # load_in_8bit=True,
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
        # Ensure prompt is a string
        if not isinstance(prompt, str):
            prompt = str(prompt)
            
        print("Final prompt to tokenizer:", prompt)  # Debug print
        
        # Tokenize and generate
        inputs = self.tokenizer(prompt, return_tensors="pt").to(self.model.device)
        with torch.no_grad(), torch.autocast(device_type=self.model.device.type):
            outputs = self.model.generate(
                **inputs,
                generation_config=self.generation_config
            )
        return self.tokenizer.decode(outputs[0], skip_special_tokens=True)