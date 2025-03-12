'''Agent using OpenAI Assistants api'''

import os
from openai import OpenAI
from agents import Agent, Runner
import asyncio

from src.adventures.kalevala import CONTEXT as game_context
from src.adventures.kalevala import SYNOPSIS as game_synopsis

# Initialize LLM o4 mini
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("Please set your OPENAI_API_KEY environment variable.")

client = OpenAI()

scene_generator_agent = Agent(
    name="Scene Generator Agent",
    model="o4-mini",
    instructions=f'''
You are a text game engine that provides rich and vivid adventure story and a scene description, 
to what the player then reacts to.
The setting and context for the text adventure game is:\n{game_context}.
The suggested synopsis, how the story could progress, is:\n{game_synopsis}.
Always return the actual description of the scene, not the meta information.
''',
)

scene_verificator_agent = Agent(
    name="Scene Verificator Agent",
    model="o4-mini",
    instructions='''You receive a text adventure game scene description and provide feedback if it'
conforms to the predefined context of the game. Also, you check that the scene description follows
the general synopsis of the game and the story going onwards in a steady text adventure game style.
If the scene description needs clear improvements, provide suggestions for the Scene Generator Agent to
improve the scene description. If the scene is OK, return 'Scene OK'. 
''',
)


game_engine_agent = Agent(
    name="Game Engine Agent",
    model="o4-mini",
    instructions='''
You are a text game engine that provides rich and vivid adventure story and a scene description, 
to what the player reacts. 
You have two agents that you orchestrate:
- Scene Generator Agent => returns the suggested next scene text.
- Scene Verificator Agent => returns either 'Scene OK' or suggestions for improvement.
DO NOT reveal 'Scene OK' or other meta outputs as the final message.
Always produce as output the final scene text that the user sees.
''',
    handoffs=[scene_generator_agent, scene_verificator_agent],
)

async def main():
    input = f"""
Create a new game session for the adventure 'kalevala'.
"""
    result = await Runner.run(game_engine_agent, game_context, game_synopsis, memory=None)
    print(result.final_output)

if __name__ == "__main__":
    asyncio.run(main())