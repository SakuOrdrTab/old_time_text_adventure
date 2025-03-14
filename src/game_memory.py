''' Game memory. Currently just a list of last 10 turns. 
TODO: needs a concise whole game summary. See LangChain Memories, they are WIP.
'''
from collections import deque

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
    