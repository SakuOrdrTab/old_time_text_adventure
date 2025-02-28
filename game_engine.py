'''The main game engine (control and model) for old time text adventure game.'''

import torch
from transformers import pipeline

from context import CONTEXT as game_context
from synopsis import SYNOPSIS as game_synopsis
import game_memory

class Game():

    def __init__(self, model : str = "meta-llama/Llama-3.2-3B-Instruct") -> None:
        # init model
        self._model = model
        self._game_memory = game_memory.GameMemory(llm=model)
        self._synopsis = game_synopsis
        self._context = game_context
        # initialize agents

        # start the game
        self._start_game()

    def _start_game(self) -> str:
        # describe the game scene at start
        pass

    def play_turn(self, player_input : str) -> str:
        pass

    def _end_game_report(self) -> str:
        pass


if __name__ == "__main__":
    game = Game()



