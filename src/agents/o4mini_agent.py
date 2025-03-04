import os
from langchain.agents import Tool, initialize_agent, AgentType
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

from context import CONTEXT
from synopsis import SYNOPSIS

from src.game_memory import GameMemory

game_memory = GameMemory()

# -----------------------------------------------------------------------------
# 1. Define your LLM
# -----------------------------------------------------------------------------
# Make sure you have set OPENAI_API_KEY in your environment.
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    raise ValueError("Please set your OPENAI_API_KEY environment variable.")

llm = ChatOpenAI(
    model_name="gpt-4o-mini",  # or "gpt-4", "gpt-3.5-turbo", etc.
    openai_api_key=OPENAI_API_KEY,
    temperature=0.7
)

# -----------------------------------------------------------------------------
# 2. Define your game data (context, synopsis, memory).
#    In practice, you would pass these in from your main code or config.
# -----------------------------------------------------------------------------
GAME_CONTEXT = CONTEXT
GAME_SYNOPSIS = SYNOPSIS


# A helper method just to get the last few memory lines as a single string.
def get_memory_string():
    # You might have a more sophisticated memory object; here's a simple example.
    return game_memory.get_memory()

# -----------------------------------------------------------------------------
# 3. Build the Tools
# -----------------------------------------------------------------------------

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

# We create an LLMChain for text generation.
text_gen_chain = LLMChain(llm=llm, prompt=text_gen_prompt_template)

def text_generation_tool(player_action: str) -> str:
    return text_gen_chain.run(
        game_context=GAME_CONTEXT,
        game_synopsis=GAME_SYNOPSIS,
        memory=get_memory_string(),
        player_action=player_action
    )

text_generation = Tool(
    name="TextGenerator",
    func=text_generation_tool,
    description=(
        "Use this tool to generate a new scene description in the text adventure "
        "based on the player's last action."
    ),
)

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

assessment_chain = LLMChain(llm=llm, prompt=assessment_prompt_template)

def status_assessment_tool(scene_description: str) -> str:
    return assessment_chain.run(scene_description=scene_description)

status_assessment = Tool(
    name="StatusAssessor",
    func=status_assessment_tool,
    description=(
        "Use this tool to evaluate a scene for narrative consistency and provide "
        "suggestions if needed. Input is a string describing the scene."
    ),
)

# -----------------------------------------------------------------------------
# 4. Initialize an Agent
# -----------------------------------------------------------------------------
# We use ZERO_SHOT_REACT_DESCRIPTION so that the agent attempts to figure out
# which tool(s) to call and in what order, based on the user's query.
agent = initialize_agent(
    tools=[text_generation, status_assessment],
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# -----------------------------------------------------------------------------
# 5. Example usage
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    print("Welcome to the multi-tool text adventure demonstration!")
    while True:
        user_input = input("\nPlayer Action (or 'quit' to exit): ")
        if user_input.lower() in ["quit", "exit"]:
            print("Exiting the game.")
            break

        # The agent will parse your request, call the relevant tool(s), and produce a final output.
        response = agent.run(user_input)
        print(f"\nAgent Output:\n{response}")
        
        # Optionally, store the generated scene in your memory for later steps
        # (this is a basic approach—use your own memory class logic).
        game_memory.add_turn_to_memory(user_input, response)
