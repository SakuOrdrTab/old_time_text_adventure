'''The main game engine (control and model) for old-time text adventure game.'''

from .game_memory import GameMemory
from .llms.o4mini_LLM import O4miniLLM

class Game():

    def __init__(self, game_context, game_synopsis) -> None:
        """Initialize the game with LLM, memory, and game context."""
        
        # Load LLM
        print("Loading game model...")
        
        self._client = O4miniLLM()
        
        # Save reference to memory
        self._game_memory = GameMemory()
        # Store game synopsis and context
        self._synopsis = game_synopsis
        self._context = game_context


    def start_game(self) -> str:

        """Start the game by describing the first scene."""
        print("\n==== Welcome to the Adventure Game ====\n")
        # print("Synopsis:\n", self._synopsis)
        # print("\nGame Context:\n", self._context)
        print("\nThe game begins...\n")

        initial_prompt = f'''
You are a text game ganerator, like in the old time computer text adventure games. 
You will describe the current scene in the adventure and the user gives actions in natural language and you decide what
happens next.
The context of the game is:\n {self._context}\n
The suggested synopsis, or what should happen during the game is:\n {self._synopsis}\n
'''

        initial_scene = self._client.chat_completions_create(
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
        self.game_turn = 1

        self._game_memory.add_turn_to_memory("", initial_scene)
        return initial_scene

    def play_turn(self, player_input: str) -> str:
        """Processes player's input and generates the next game response."""
        if not player_input.strip():
            print("You need to enter an action.")
            return

        # Get the game's response using the LLM
        output = self._client.chat_completions_create(
            messages=[
                {
                    "role": "assistant",
                    "content": f"You create the next scene in the adventure according to player's last action.\
                        the context of the game is:\n {self._context}\n\
                        The suggested synopsis, or what should happen during the game is:\n {self._synopsis}\n\
                        the previous turns in the game were:\n {self._game_memory.get_memory()}\n\
                        Remember to stay in character output only text describing the game situation to the player.\n\
                        The suggested length of game is around 20-60 turns and the game get's more difficult as it progresses. \
                        The current turn is {self.game_turn}.\n\
                        It is also possible, that the current action kills the player, or the end conditions of the \
                        game are met. In that case, the end of the output must be marked with 'GAME OVER'.\n\
                        "
                },
                {
                    "role": "user",
                    "content": f"the player's action: '{player_input}'"
                },
            ]
        )

        self._game_memory.add_turn_to_memory(player_input, output)
        self.game_turn += 1
        return output

    def end_game_report(self) -> str:
        """End the game and summarize what happened."""
        response = ""
        response += ("\n==== GAME OVER ====\n")
        assessment = self._client.chat_completions_create(
            messages=[
                {
                    "role": "assistant",
                    "content": f"""
You are an end summarizer of an adventure game. Assess the player's performance in the text adventure
 game, where the suggested synopsis of the adventure was:\n {self._synopsis}
. Last 10 turns in the game were:
{self._game_memory.get_memory()}

Give a summary of the adventure and assess the player's performance in the text adventure.
Assess especially if the player failed or completed the adventure.
"""
                }
            ]
        )
        response += assessment + "\n"
        response += "\nThank you for playing!"
        return response

if __name__ == "__main__":
    from src.adventures.kalevala import CONTEXT, SYNOPSIS
    game = Game(CONTEXT, SYNOPSIS)
    
    initial_setting = game.start_game()
    print(initial_setting)

    # Simple game loop
    while True:
        player_action = input("\n: ")
        if player_action.lower() in ["quit", "exit"]:
            break
        game_output = game.play_turn(player_action)
        print(game_output)
    print(game.end_game_report())
