from .abstract_LLM import AbstractLLM

import os
from openai import OpenAI

class O4miniLLM(AbstractLLM):
    """OpenAI o4 mini LLM """
    def __init__(self):

        print("Initializing LLM OpenAI o4 mini...")
        # You could also pass the api_key directly to OpenAI's client if needed.
        self.model = "gpt-4o-mini"
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        if OPENAI_API_KEY is None:
            raise ValueError("Please set your OpenAI API key as an environment variable.")
        self._client = OpenAI()

    def chat_completions_create(self, messages) -> str:
        return self._client.chat.completions.create(
            model=self.model,
            messages=messages
        ).choices[0].message.content
