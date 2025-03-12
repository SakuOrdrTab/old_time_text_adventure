# WIP

# A text adventure game in the style of old computer text games

Instead of a parser, natural language is used to interact with the game engine. The motor of the game engine is currently openai's o4-mini, which seems to be capable and costeffective solution. Open source models runnable locally with 16 GB VRAM did not seem to achieve good enough outputs yet. The game engine can handle different types of adventures; the context and hint-level synopsis are passed to the LLM in the prompt and they can be found in the adventures folder. 

O4-mini seems to be quite cheap, I have now tweaked with the game for a coupla days and I have spent only twenty cents.

## TODO

- Strip occasional "Text Adventure game:"
- Add short descriptions to adventures and directory browsing
- Add Authentication and user administration in Mongo
- Session handling (with Redis?)

- Try local models and Stable diffusion

## Agents

My original intention was to use multiagent generation with LangChain. However, LangChain is not very stabil and it seems to develop faster than I can code. I also don't have currently time to migrate to LangGraph. OpenAI Swarm could be a solution, but that could impede later incorporation of SLM's.

Anyhow, if you want to see how my agent with two tools (text generator and assesser) work, you can run:

>python -m src.agents.<agent>

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

There are two entry points.

There is the flask webUI, that also incorporates scene visualizations using DALL-E 2. This however is not free. Using o4-mini is really cheap and a game costs only about cent or another to play. However, creating images with DALL-E is more costly, costing about 2 cents an image. This means that playing the game through webUI with images costs maybe 1€ if the game lasts about 50 turns. However, this is the way I intended this game to be, and to run it:
>py app.py

The main.py is the CLI variant for playing the game. It does not use DALL-E, so it is cheaper
>py main.py

## Adventures

Different adventures are in the `adventures` folder in each files as constants. Currently there is:
- kalevala (finnish iron age traditional adventure)
- zombie_apocalypse (Traditional zombie survival horror in northern Norway)
- edo_romance (Late samurai period romance)
- icu_disaster (A medical RPG)
