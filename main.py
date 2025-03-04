from src.game_engine import Game

if __name__ == "__main__":
    game = Game()
    
    initial_setting = game.start_game()
    print(initial_setting)

    # Simple game loop
    while True:
        player_action = input("\n: ")
        if player_action.lower() in ["quit", "exit"]:
            break
        game_output = game.play_turn(player_action)
        print(game_output)
    print(game._end_game_report())
