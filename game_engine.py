'''The main game engine (control and model) for old-time text adventure game.'''

import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
from langchain_huggingface import HuggingFacePipeline
from langchain.chains import ConversationChain

from context import CONTEXT as game_context
from synopsis import SYNOPSIS as game_synopsis
import game_memory

class Game:

    def __init__(self, model_name: str = "meta-llama/Llama-3.2-3B-Instruct") -> None:
        """Initialize the game with LLM, memory, and game context."""
        
        # Load LLM
        print("Loading game model...")
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name, device_map="auto", torch_dtype=torch.float16)
        self._llm_pipeline = pipeline("text-generation", model=model, tokenizer=tokenizer)
        self._llm = HuggingFacePipeline(pipeline=self._llm_pipeline)
        
        # Initialize game memory
        # self._game_memory = game_memory.GameMemory(llm=self._llm)

        # Store game synopsis and context
        self._synopsis = game_synopsis
        self._context = game_context

        # Initialize conversation chain with memory
        self._conversation = ConversationChain(llm=self._llm)

        # Start the game
        self._start_game()

    def _start_game(self) -> None:
        """Start the game by describing the first scene."""
        print("\n==== Welcome to the Adventure Game ====\n")
        print("Synopsis:\n", self._synopsis)
        print("\nGame Context:\n", self._context)
        print("\nThe game begins...\n")

        # Generate the initial game scene using the LLM
        initial_prompt = (
            "You return from a successful hunting trip. As you approach your home, "
            "you smell smoke and hear eerie silence. Something is wrong. Describe the scene."
        )

        initial_scene = self._conversation.predict(input=initial_prompt)
        print(initial_scene)

    def play_turn(self, player_input: str) -> None:
        """Processes player's input and generates the next game response."""
        if not player_input.strip():
            print("You need to enter an action.")
            return

        # Get the game's response using the LLM
        response = self._conversation.predict(input=player_input)
        print(response)

    def _end_game_report(self) -> None:
        """End the game and summarize what happened."""
        print("\n==== GAME OVER ====")
        # memory_state = self._game_memory.load_memory_variables({})
        # print("\nSummary of Your Journey:\n", memory_state["long_term"])
        print("\nThank you for playing!")

if __name__ == "__main__":
    game = Game()
    
    # Simple game loop
    while True:
        player_action = input("\nWhat do you do? ")
        if player_action.lower() in ["quit", "exit"]:
            game._end_game_report()
            break
        game.play_turn(player_action)



