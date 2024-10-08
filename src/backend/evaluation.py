import transformers
import torch
from transformers import BitsAndBytesConfig
from transformers import AutoModelForCausalLM, AutoTokenizer

from deepeval.models import DeepEvalBaseLLM
from utils.config import hf_token


class CustomLlama3_8B(DeepEvalBaseLLM):
    def __init__(self):
        quantization_config = BitsAndBytesConfig(
            load_in_4bit=True,
            bnb_4bit_compute_dtype=torch.float16,
            bnb_4bit_quant_type="nf4",
            bnb_4bit_use_double_quant=True,
        )
        model_4bit =  AutoModelForCausalLM.from_pretrained(
            "meta-llama/Meta-Llama-3-8B-Instruct", # llama-3.1-8b-instant
            device_map="auto",
            quantization_config=quantization_config,
            token=hf_token,
        )
        tokenizer = AutoTokenizer.from_pretrained(
            "meta-llama/Meta-Llama-3-8B-Instruct",
            token=hf_token,
        )

        self.model = model_4bit
        self.tokenizer = tokenizer

    def load_model(self):
        return self.model
    
    def get_model_name(self):
        return "Llama-3 8B"
    
    def generate(self, prompt: str) -> str:
        model = self.load_model()
        pipeline = transformers.pipeline(
            "text-generation",
            model=model,
            tokenizer=self.tokenizer,
            use_cache=True,
            device_map="auto",
            max_length=2500,
            do_sample=True,
            top_k=5,
            num_return_sequences=1,
            eos_token_id=self.tokenizer.eos_token_id,
            pad_token_id=self.tokenizer.eos_token_id,
        )
        return pipeline(prompt)
    
    async def a_generate(self, prompt: str) -> str:
        return self.generate(prompt)


if __name__ == "__main__":
    custom_llm = CustomLlama3_8B()
    print(custom_llm.generate("Write me a joke"))


