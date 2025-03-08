from flask import Flask, render_template, request, redirect, url_for
from openai import OpenAI
import uuid

# Import your game engine and adventures.
from src.game_engine import Game
from src.helper_funcs import load_adventure
from src.ImageGenerator import ImageGenerator

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
  
image_generator = ImageGenerator()

@app.route('/new_game', methods=['GET', 'POST'])
def new_game():
    if request.method == 'POST':
        # Get the adventure name from the form
        adventure_name = request.form.get('adventure')
        if adventure_name not in adventures:
            return "Invalid adventure selected", 400
        
        # Initialize the game engine for the selected adventure.
        game_context, game_synopsis, short_desc, style = load_adventure(adventure_name)
        image_generator.set_style(style)
        game = Game(game_context=game_context, game_synopsis=game_synopsis)
        
        # Create a unique game session ID.
        game_id = str(uuid.uuid4())
        game_statuses[game_id] = game
        
        # Start the game and render the initial scene.
        initial_scene = game.start_game()
        image = image_generator.get_image(initial_scene)
        return render_template("next_scene.html", scene=initial_scene, game_id=game_id, game_over=False, image=image)
    
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
        image = image_generator.get_image(report)
        del game_statuses[game_id]
        return render_template("end_game.html", report=report, image=image)
    
    image = image_generator.get_image(game_output)
    return render_template("next_scene.html", scene=game_output, game_id=game_id, game_over=game_over, image=image)

@app.route('/')
def index():
    return redirect(url_for('new_game'))

if __name__ == "__main__":
    app.run(debug=True)
