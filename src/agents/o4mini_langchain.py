import os
from langchain.agents import Tool, initialize_agent, AgentType
from langchain_openai import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

class O4miniLangChainAgent():

    def __init__(self, context : str, synopsis : str, memory, logger = None):
        """LangChain framework agent. Currently using still openAI, WIP to use open source
        models

        Args:
            context (str): context of the adventure
            synopsis (str): suggested synopsis of the adventure
            memory (_type_): memory of past interactions
            logger (_type_, optional): Not currently implemented. Defaults to None.

        Raises:
            ValueError: If openAI API key is missing
        """        
        
        # Initialize LLM o4 mini
        OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
        if not OPENAI_API_KEY:
            raise ValueError("Please set your OPENAI_API_KEY environment variable.")

        # Use chat for agent behaviour
        self.llm = ChatOpenAI(
            model_name="gpt-4o-mini",  # or "gpt-4", "gpt-3.5-turbo", etc.
            openai_api_key=OPENAI_API_KEY,
            temperature=0.7
        )

        # Load data
        self.game_context = context
        self.game_synopsis = synopsis
        self.memory = memory

        # Build Tools
        self.tools = [
            Tool(
                name="TextGenerator",
                func=self.text_generation_tool,
                description=(
                    "Use this tool to generate a new scene description in the text adventure "
                    "based on the player's last action."
                ),
            ),
            Tool(
                name="SceneEvaluator",
                func=self.scene_evaluation_tool,
                description=(
                    "Use this tool to evaluate a scene for narrative consistency and provide "
                    "suggestions if needed. Input is a string describing the scene."
                ),
            ),
        ]
        
        custom_prefix = '''
You are a text game engine that provides rich and vivid adventure story and a scene description, 
to what the player reacts. 
You have two tools:\n
1) TextGenerator => returns the next scene text.
2) SceneEvaluator => returns either 'Scene OK' or suggestions for improvement.
Your final answer to the user MUST be the final scene text provided by the TextGenerator after it has been modified by the tools when necessary.
Process:\n
- Step 1: Call TextGenerator to get the game scene.
- Step 2: Call SceneEvaluator to check if the scene is OK or needs improvements.
- Step 3: If SceneEvaluator says 'Scene OK', return the scene from Step 1.
  If it suggests improvements, return the scene with improvement ideas for TextGenerator to be improved.
- Step 4: Return the rich and compelling output from TextGenerator, after improvements when necessary.
DO NOT reveal 'Scene OK' or other meta outputs as the final message.
Always produce as output the final scene text that the user sees.
If SceneEvaluator returns suggestions, incorporate them exactly into the scene text. Then produce that improved scene as your final answer.
Do not call any tool more than three times; if three calls are reached, immediately return the best scene text you have.
YOUR FINAL ANSWER MUST BE THE EXACT OUTPUT OF MODIFIED OR NONMODIFIED TEXTGENERATOR!!
'''

        # Initialize the agent
        # We use ZERO_SHOT_REACT_DESCRIPTION so that the agent attempts to figure out
        # which tool(s) to call and in what order, based on the user's query.
        self.agent = initialize_agent(
            tools=self.tools,
            llm=self.llm,
            agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
            verbose=True,
            agent_kwargs={
                "max_iterations" : 3,
                "system_message": custom_prefix  
            }
        )

    def text_generation_tool(self, player_action: str) -> str:
        # (A) Text Generation Tool
        text_gen_prompt_template = PromptTemplate(
            input_variables=["game_context", "game_synopsis", "memory", "player_action"],
            template="""
You are a text adventure game text generator. You generate text for the player that describes the current scene
at the game on the basis of game context, previous game history and most importantly the player's last action. The game synopsis
gives the overall game plot, how the game could advance in general. However, the player's actions are more important
and anything can happen; you generate text according to these specifications.
Game context:
{game_context}

Game synopsis:
{game_synopsis}

Recent game turns:
{memory}

Based on the player's action: "{player_action}",
generate the next scene description. Be detailed, consistent, and immersive.
        """
        )
        text_gen_chain = LLMChain(llm=self.llm, prompt=text_gen_prompt_template)
        return text_gen_chain.run(
            game_context=self.game_context,
            game_synopsis=self.game_synopsis,
            memory=self.memory.get_memory(),
            player_action=player_action
        )

    def scene_evaluation_tool(self, scene_description: str) -> str:
        # (B) Scene Evaluation Tool
        scene_evaluation_prompt = PromptTemplate(
            input_variables=["scene_description", "game_context", "memory"],
            template="""
You are a scene evaluator for an old fashioned text adventure game.
Please evaluate the scene description below for consistency to synopsis and
context.

Scene description:
{scene_description}

Check that the scene description is not in conflict with the game context, which is:
{game_context}

Also see, that there are no conflicts and the narraticve of the adventure aligns with 
the previous turns in the game, which is:
{memory}

If the scene does not have clear errors, respond with "Scene OK".
Otherwise, point out any issues or suggestions for improvement.
        """
        )
        scene_evaluation_chain = LLMChain(llm=self.llm, prompt=scene_evaluation_prompt)
        return scene_evaluation_chain.run(
            scene_description=scene_description,
            game_context=self.game_context,
            memory=self.memory.get_memory()
        )

    def run(self, user_input: str) -> str:
        return self.agent.run(user_input)

# For testing
if __name__ == "__main__":
    print("Welcome to the multi-tool text adventure demonstration!")
    from src.adventures.kalevala import CONTEXT as context
    from src.adventures.kalevala import SYNOPSIS as synopsis

    from src.game_memory import GameMemory
    game_memory = GameMemory()
    agent = O4miniLangChainAgent(context=context, synopsis=synopsis, memory=game_memory)
    while True:
        user_input = input("\nPlayer Action (or 'quit' to exit): ")
        if user_input.lower() in ["quit", "exit"]:
            print("Exiting the game.")
            break

        response = agent.run(user_input)
        print(f"\nAgent Output:\n{response}")
        
        game_memory.add_turn_to_memory(user_input, response)
