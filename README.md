# WIP

# A text adventure game in the style of old computer text games

Instead of a parser, natural language is used to interact with the game engine. The motor of the game engine is currently openai's o4-mini, which seems to be capable and costeffective solution. Open source models runnable locally with 16 GB VRAM did not seem to achieve good enough outputs yet. The game engine can handle different types of adventures; the context and hint-level synopsis are passed to the LLM in the prompt and they can be found in the adventures folder. Just replace the `main.py` imports accordingly and you have a couple of alternatives.

O4-mini seems to be quite cheap, I have now tweaked with the game for a coupla days and I have spent only twenty cents.

## TODO

- End game conditions on right time: .endswith(".END.")
- Strip occasional "Text Adventure game:"

- Try local models
- Make a C64 React frontend
- Add DallE images to a scene, not cheap however.

## Agents

My original intention was to use multiagent generation with LangChain. However, LangChain is not very stabil and it seems to develop faster than I can code. I also don't have currently time to migrate to LangGraph. OpenAI Swarm could be a solution, but that could impede later incorporation of SLM's.

Anyhow, if you want to see how my agent with two tools (text generator and assesser) work, you can run:

>python -m src.agents.o4mini_agent

This works from the project root folder, otherwise the module imports get screwed.

## Installing

After cloning, create a venv:
>python -m .venv

Activate the venv (Windows):
>.venv\Scripts\activate

Install dependancies:
>pip install -r requirements.txt

In you environment, set you openAI API key to the environment variable `OPENAI_API_KEY`
You can also do this in the code, if you prefer; the init of the LLM happens in O4miniLLM class, as `chat.completions.create()` is called in the initial scene description.

Now just run the main entry point:
>py main.py