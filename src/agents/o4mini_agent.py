import os
from langchain.agents import Tool, initialize_agent, AgentType
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

class O4miniAgent():

    def __init__(self, context : str, synopsis : str, memory):
        
        # Initialize LLM o4 mini
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        if not OPENAI_API_KEY:
            raise ValueError("Please set your OPENAI_API_KEY environment variable.")

        self.llm = ChatOpenAI(
            model_name="gpt-4o-mini",  # or "gpt-4", "gpt-3.5-turbo", etc.
            openai_api_key=OPENAI_API_KEY,
            temperature=0.7
        )

        # Load data
        self.GAME_CONTEXT = context
        self.GAME_SYNOPSIS = synopsis
        self.memory = memory

        # Build Tools
        self.text_generation = Tool(
            name="TextGenerator",
            func=self.text_generation_tool,
            description=(
                "Use this tool to generate a new scene description in the text adventure "
                "based on the player's last action."
            ),
        )       
        self.status_assessment = Tool(
            name="StatusAssessor",
            func=self.status_assessment_tool,
            description=(
                "Use this tool to evaluate a scene for narrative consistency and provide "
                "suggestions if needed. Input is a string describing the scene."
            ),
        )

        # # We create an LLMChain for text generation.
        # self.text_gen_chain = LLMChain(llm=self.llm, prompt=self.text_gen_prompt_template)

        # self.assessment_chain = LLMChain(llm=self.llm, prompt=self.assessment_prompt_template)

        # Initialize the agent
        # We use ZERO_SHOT_REACT_DESCRIPTION so that the agent attempts to figure out
        # which tool(s) to call and in what order, based on the user's query.
        self.agent = initialize_agent(
            tools=[self.text_generation, self.status_assessment],
            llm=self.llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True
        )

    def text_generation_tool(self, player_action: str) -> str:
        # (A) Text Generation Tool
        text_gen_prompt_template = PromptTemplate(
            input_variables=["game_context", "game_synopsis", "memory", "player_action"],
            template="""
You are a text adventure game text generator. You generate text for the player that describes the current scene
at the game on the basis of game context, previous game history and most importantly the last player action. The game synopsis
gives the overall game plot, how the game could advance in general. However, the player's actions are more important
and anything can happen, you generate text according to these specifications.
Game context:
{game_context}

Game synopsis:
{game_synopsis}

Recent game memory:
{memory}

Based on the player's action: "{player_action}",
generate the next scene description. Be detailed, consistent, and immersive.
        """
        )
        text_gen_chain = LLMChain(llm=self.llm, prompt=text_gen_prompt_template)
        return text_gen_chain.run(
            game_context=self.GAME_CONTEXT,
            game_synopsis=self.GAME_SYNOPSIS,
            memory=self.memory.get_memory(),
            player_action=player_action
        )

    def status_assessment_tool(self, scene_description: str) -> str:
        # (B) Status Assessment Tool
        assessment_prompt_template = PromptTemplate(
            input_variables=["scene_description"],
            template="""
You are a status assessor for a text adventure game.
Please evaluate the scene description below for consistency to synopsis and
context.

Scene description:
{scene_description}

If the scene is fine, respond with "Scene OK".
Otherwise, point out any issues or suggestions for improvement.
        """
        )
        assessment_chain = LLMChain(llm=self.llm, prompt=assessment_prompt_template)
        return assessment_chain.run(scene_description=scene_description)

    def run(self, user_input: str) -> str:
        return self.agent.run(user_input)

# For testing
if __name__ == "__main__":
    print("Welcome to the multi-tool text adventure demonstration!")
    from context import CONTEXT as context
    from synopsis import SYNOPSIS as synopsis

    from src.game_memory import GameMemory
    game_memory = GameMemory()
    agent = O4miniAgent(context=context, synopsis=synopsis, memory=game_memory)
    while True:
        user_input = input("\nPlayer Action (or 'quit' to exit): ")
        if user_input.lower() in ["quit", "exit"]:
            print("Exiting the game.")
            break

        response = agent.run(user_input)
        print(f"\nAgent Output:\n{response}")
        
        game_memory.add_turn_to_memory(user_input, response)
