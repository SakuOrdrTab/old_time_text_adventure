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
        """creates a chat completion in a similar manner as openai's
        chat.completions.create(). Returns only the actual output string. Please use openAI prompt template format, like
        messages = [
            {"role": "system", "content": "You are a text adventure game generato....."},
            {"role": "assistant", "content": "You create the next scene...."},
            {"role": "user", "content": "I go to my hut and start eating..."}
        ]

        Args:
            messages (_type_): Prompt in openAI format

        Returns:
            str: Actual text output from the model
        """             
        # Convert the list of messages into a single prompt string using ChatML markers.
        prompt = ""
        for msg in messages:
            role = msg["role"]
            content = msg["content"]
            if role == "system":
                prompt += f"<|system|>{content}<|end|>\n"
            elif role == "assistant":
                prompt += f"<|assistant|>{content}<|end|>\n"
            elif role == "user":
                prompt += f"<|user|>{content}<|end|>\n"
        # Append an assistant marker to signal that the model should generate a response.
        prompt += "<|assistant|>"

        outputs = self.text_gen(
            prompt,
            temperature=0.7,
            top_p=0.9,
            repetition_penalty=1.2,
            do_sample=True,
            return_full_text=False,
        )
        print("[DEBUG] Actual prompt:", prompt)
        print("[DEBUG] End of actual prompt")
        print("[DEBUG] Generated text:", outputs[0]["generated_text"])
        print("[DEBUG] End of Generated text.")
        return outputs[0]["generated_text"]

if __name__ == "__main__":
    if not torch.cuda.is_available():
        print("WARNING: CUDA is not available. Inference will run on CPU and be extremely slow.")
    llm = LLaMA3_2_8BLLM()
    # Sample messages in the OpenAI chat format
    messages = [
        {"role": "system", "content": "You are a text adventure game generator. Provide vivid descriptions and creative scenarios."},
        {"role": "assistant", "content": "The adventure begins in a bustling medieval marketplace at dawn."},
        {"role": "user", "content": "Describe the marketplace and hint at an underlying mystery."}
    ]
    print(llm.chat_completions_create(messages))
