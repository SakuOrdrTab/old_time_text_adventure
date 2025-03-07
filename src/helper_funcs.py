'''Some helper functions for the game'''

import importlib

def load_adventure(adventure_name : str) -> tuple:
    ''' Loads the adventure data and returns a tuple: (game_context, game_synopsis)
    context : str, 
    synopsis : str'''
    try:
        module = importlib.import_module(f"src.adventures.{adventure_name}")
        game_context = getattr(module, "CONTEXT")
        game_synopsis = getattr(module, "SYNOPSIS")
        return game_context, game_synopsis
    except (ModuleNotFoundError, AttributeError) as e:
        raise ImportError(f"Error in adventure import: {e}")
        return None, None
