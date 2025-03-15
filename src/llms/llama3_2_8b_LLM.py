from .abstract_LLM import AbstractLLM

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline

class LLaMA3_2_8BLLM(AbstractLLM):
    """Meta LLaMa 3.2 8B """
    def __init__(self):
        print("Initializing Meta LLaMa 3-8B...")
            # Load the tokenizer
        self.tokenizer = AutoTokenizer.from_pretrained("meta-llama/Meta-Llama-3-8B")

        # Load the model in float16 on GPU (device_map="auto" tries to place model on GPU if available)
        self.model = AutoModelForCausalLM.from_pretrained(
            "meta-llama/Meta-Llama-3-8B",   
            device_map="auto",
            # load_in_4bit=True,
            torch_dtype=torch.float16      # Use half precision
        )

            # Create a text-generation pipeline
        self.text_gen = pipeline(
            "text-generation",
            model=self.model,
            tokenizer=self.tokenizer,
            device_map="auto",
        )

    def chat_completions_create(self, messages) -> str:
        outputs = self.text_gen(
            messages,
            # max_new_tokens=256,
            temperature=0.7,
            top_p=0.9,
            repetition_penalty=1.2,
            do_sample=True
        )

        return outputs[0]["generated_text"]

if __name__ == "__main__":
    if not torch.cuda.is_available():
        print("WARNING: CUDA is not available. Inference will run on CPU and be extremely slow.")
    llm = LLaMA3_2_8BLLM()
    print(llm.chat_completions_create("Create a text adventure scene in ancient egypt."))
