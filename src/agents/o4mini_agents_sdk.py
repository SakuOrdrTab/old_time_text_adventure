'''Agent using OpenAI Assistants api'''

import os
from openai import OpenAI
from agents import Agent, Runner, AsyncOpenAI, OpenAIChatCompletionsModel
import asyncio



class O4miniAgentsSDK():
    '''O4 mini using the openai agents SDK'''

    def __init__(self, context : str, synopsis : str, memory, logger=None):
        """O4 mini agent with two subagents

        Args:
            context (str): the context of the game
            synopsis (str): the suggested synopsis of the story
            memory (_type_): The memory needs to be passed
            logger (_type_, optional): If you want to use a logger, currently not implemented. Defaults to None.

        Raises:
            ValueError: If no OPEN AI api key

        """        
        self.context = context
        self.synopsis = synopsis
        self.memory = memory

        # Initialize LLM o4 mini
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        if not OPENAI_API_KEY:
            raise ValueError("Please set your OPENAI_API_KEY environment variable.")

        # Use chatCompletions for agent interaction for now
        self.model=OpenAIChatCompletionsModel( 
            model="gpt-4o-mini",
            openai_client=AsyncOpenAI()
        )

        # Creates the scene text
        self.scene_generator_agent = Agent(
            name="Scene Generator Agent",
            model=self.model,
            instructions=f'''
        You are a text game engine that provides rich and vivid adventure story and a scene description, 
        to what the player then reacts to.
        The setting and context for the text adventure game is:\n{self.context}.
        The suggested synopsis, how the story could progress, is:\n{self.synopsis}.
        Always return the actual description of the scene, not the meta information.
        ''',
        )

        # Verifies scene to specs
        # TODO: health, progress of story
        self.scene_verificator_agent = Agent(
            name="Scene Verificator Agent",
            model=self.model,
            instructions='''You receive a text adventure game scene description and provide feedback if it'
        conforms to the predefined context of the game. Also, you check that the scene description follows
        the general synopsis of the game and the story going onwards in a steady text adventure game style.
        If the scene description needs clear improvements, provide suggestions for the Scene Generator Agent to
        improve the scene description. If the scene is OK, return 'Scene OK'. 
        ''',
        )

        # The orchestrator agent
        self.game_engine_agent = Agent(
            name="Game Engine Agent",
            model=self.model,
            instructions='''
        You are a text game engine that provides rich and vivid adventure story and a scene description, 
        to what the player reacts. 
        You have two agents that you orchestrate:
        - Scene Generator Agent => returns the suggested next scene text.
        - Scene Verificator Agent => returns either 'Scene OK' or suggestions for improvement.
        DO NOT reveal 'Scene OK' or other meta outputs as the final message.
        Always produce as output the final scene text that the user sees.
        ''',
            handoffs=[self.scene_generator_agent, self.scene_verificator_agent],
        )

    async def run(self, input) -> str:
        result = await Runner.run(self.game_engine_agent, input)
        return result.final_output
    

async def test_main():
    from src.adventures.kalevala import CONTEXT as game_context
    from src.adventures.kalevala import SYNOPSIS as game_synopsis
    test_agent = O4miniAgentsSDK(game_context, game_synopsis, "")
    print(await test_agent.run("Create a nice finnish adventure initial scene"))

if __name__ == "__main__":
    asyncio.run(test_main())