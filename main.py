from src.game_engine import Game
from src.adventures.paranoia import CONTEXT as game_context, SYNOPSIS as game_synopsis

if __name__ == "__main__":
    game = Game(game_context=game_context, game_synopsis=game_synopsis)
    
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
