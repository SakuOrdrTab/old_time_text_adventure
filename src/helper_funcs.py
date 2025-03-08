'''Some helper functions for the game'''

import importlib

def load_adventure(adventure_name : str) -> tuple:
    ''' Loads the adventure data and returns a tuple: (game_context, game_synopsis, short_desc, style)
    context : str, 
    synopsis : str,
    short_desc : str,
    style : str
    '''
    try:
        module = importlib.import_module(f"src.adventures.{adventure_name}")
        game_context = getattr(module, "CONTEXT")
        game_synopsis = getattr(module, "SYNOPSIS")
        short_desc = getattr(module, 'SHORT_DESCRIPTION')
        style = getattr(module, 'STYLE')
        return game_context, game_synopsis, short_desc, style
    except (ModuleNotFoundError, AttributeError) as e:
        raise ImportError(f"Error in adventure import: {e}")
        return None, None
