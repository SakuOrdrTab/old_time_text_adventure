from flask import Flask, render_template, request, redirect, url_for
import uuid

# Import your game engine and adventures.
from src.game_engine import Game
from src.adventures.icu_disaster import CONTEXT as icu_context, SYNOPSIS as icu_synopsis

app = Flask(__name__)
app.secret_key = "your_secret_key_here" # Implement later for sessions

# Dictionary to store ongoing game sessions.
game_statuses = {}

# A dictionary of available adventures.
adventures = [
    "icu_disaster",
    "kalevala",
    "paranoia",
    "edo_romance",
    "zombie_apocalypse",
]

@app.route('/new_game', methods=['GET', 'POST'])
def new_game():
    if request.method == 'POST':
        # Get the adventure name from the form
        adventure_name = request.form.get('adventure')
        if adventure_name not in adventures:
            return "Invalid adventure selected", 400
        
        # Initialize the game engine for the selected adventure.
        if adventure_name == "icu_disaster":
            from src.adventures.icu_disaster import CONTEXT as game_context, SYNOPSIS as game_synopsis
        elif adventure_name == "kalevala":
            from src.adventures.kalevala import CONTEXT as game_context, SYNOPSIS as game_synopsis
        elif adventure_name == "paranoia":
            from src.adventures.paranoia import CONTEXT as game_context, SYNOPSIS as game_synopsis
        elif adventure_name == "edo_romance":
            from src.adventures.edo_romance import CONTEXT as game_context, SYNOPSIS as game_synopsis
        elif adventure_name == "zombie_apocalypse":
            from src.adventures.zombie_apocalypse import CONTEXT as game_context, SYNOPSIS as game_synopsis
        else:
            return "Error in adventure import", 400
        game = Game(game_context=game_context, game_synopsis=game_synopsis)
        
        # Create a unique game session ID.
        game_id = str(uuid.uuid4())
        game_statuses[game_id] = game
        
        # Start the game and render the initial scene.
        initial_scene = game.start_game()
        return render_template("next_scene.html", scene=initial_scene, game_id=game_id, game_over=False)
    
    # GET request: render the adventure selector.
    return render_template("new_game.html", adventures=adventures)

@app.route('/next_scene', methods=['POST'])
def next_scene():
    game_id = request.form.get('game_id')
    player_action = request.form.get('action')
    
    if not game_id or game_id not in game_statuses:
        return "Invalid or expired game session.", 400
    
    game = game_statuses[game_id]
    game_output = game.play_turn(player_action)
    game_over = "game over" in game_output.lower()

    if game_over:
        report = game.end_game_report()
        del game_statuses[game_id]
        return render_template("end_game.html", report=game.end_game_report())
        return render_template("end_game.html", report=report)
    
    return render_template("next_scene.html", scene=game_output, game_id=game_id, game_over=game_over)

@app.route('/')
def index():
    return redirect(url_for('new_game'))

if __name__ == "__main__":
    app.run(debug=True)
