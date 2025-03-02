'''The main game engine (control and model) for old-time text adventure game.'''

# import torch
# from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
# from langchain_huggingface import HuggingFacePipeline
# from langchain.chains import ConversationChain
from openai import OpenAI

from collections import deque
import os

from context import CONTEXT as game_context
from synopsis import SYNOPSIS as game_synopsis
# import game_memory

class GameMemory():

    def __init__(self) -> None:
        self._memory = deque(maxlen=10)

    def add_turn_to_memory(self, player_input: str, game_response: str) -> None:
        """Add the player's input and game response to the game memory."""
        self._memory.append((player_input, game_response))

    def get_memory(self) -> str:
        """Get the game memory as a string."""
        memory_str = ""
        for turn in self._memory:
            memory_str += f"Text Adventure Game: {turn[1]}\nPlayer: {turn[0]}\n\n"
        return memory_str

class Game():

    def __init__(self, memory, model_name: str = "meta-llama/Llama-3.2-3B-Instruct") -> None:
        """Initialize the game with LLM, memory, and game context."""
        
        # Load LLM
        print("Loading game model...")
        # tokenizer = AutoTokenizer.from_pretrained(model_name)
        # model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto", torch_dtype=torch.float16)
        # self._llm_pipeline = pipeline("text-generation", model=model, tokenizer=tokenizer)
        # self._llm = HuggingFacePipeline(pipeline=self._llm_pipeline)
        self._model = "gpt-4o-mini"
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        if OPENAI_API_KEY is None:
            raise ValueError("Please set your OpenAI API key as an environment variable.")
        self._client = OpenAI()
        
        # Save reference to memory
        self._game_memory = memory

        # Store game synopsis and context
        self._synopsis = game_synopsis
        self._context = game_context


    def start_game(self) -> str:

        """Start the game by describing the first scene."""
        print("\n==== Welcome to the Adventure Game ====\n")
        print("Synopsis:\n", self._synopsis)
        print("\nGame Context:\n", self._context)
        print("\nThe game begins...\n")

        initial_prompt = f'''
You are a text game ganerator, like in the old time computer text adventure games. 
You will describe the current scene in the adventure and the user gives actions in natural language and you decide what
happens next.
The context of the game is:\n {self._context}\n
The suggested synopsis, or what should happen during the game is:\n {self._synopsis}\n
'''

        initial_scene = self._client.chat.completions.create(
            model=self._model,
            messages=[
                {"role": "system", "content": initial_prompt },
                {"role": "assistant", "content":
'''
As the game now starts, give a small description of where and at what time the adventure happens.
Also, if some important setting for the adventure exist, describe them, for example if magic is possible,
or if the player has special skills or similar.
Now describe the first scene in the game, as the player would see it, and then the player will give an action to start the game.
'''
                },
                {
                    "role": "user",
                    "content": "Describe the start scene in the game."
                }
            ]
        )

        # print(initial_scene)
        return initial_scene.choices[0].message.content

    def play_turn(self, player_input: str) -> str:
        """Processes player's input and generates the next game response."""
        if not player_input.strip():
            print("You need to enter an action.")
            return

        # Get the game's response using the LLM
        response = self._client.chat.completions.create(
            model=self._model,
            messages=[
                {
                    "role": "assistant",
                    "content": f"You create the next scene in the adventure according to player's last action.\
                        the conxtext of the game is:\n {self._context}\n\
                        The suggested synopsis, or what should happen during the game is:\n {self._synopsis}\n\
                        the previous turns in the game were:\n {self._game_memory.get_memory()}\n\
                        Remember to stay in character output only text describing the game situation to the player."
                },
                {
                    "role": "user",
                    "content": f"the player's action: '{player_input}'"
                },
            ]
        )
        return response.choices[0].message.content

    def _end_game_report(self) -> str:
        """End the game and summarize what happened."""
        response = ""
        response += ("\n==== GAME OVER ====")
        assessment = self._client.chat.completions.create(
            model=self._model,
            messages=[
                {
                    "role": "system",
                    "content": "You summarize the game and assess the player's performance. Last 10 turns in the game were:\
                        \n" + self._game_memory.get_memory()
                }
            ]
        )
        response += assessment.choices[0].message.content + "\n"
        response += "\nThank you for playing!"
        return response

if __name__ == "__main__":
    game_memory = GameMemory()
    game = Game(memory=game_memory)
    
    initial_setting = game.start_game()
    print(initial_setting)
    game_memory.add_turn_to_memory("", initial_setting)

    # Simple game loop
    while True:
        player_action = input("\nWhat do you do? ")
        if player_action.lower() in ["quit", "exit"]:
            game._end_game_report()
            break
        game_output = game.play_turn(player_action)
        game_memory.add_turn_to_memory(player_action, game_output)
        print(game_output)
    print(game._end_game_report())



