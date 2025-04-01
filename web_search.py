import asyncio
import yaml
from autogen_agentchat.ui import Console
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.agents import AssistantAgent
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.agents.web_surfer import MultimodalWebSurfer

with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

model_client = OpenAIChatCompletionClient(**config["model_config"])
gemma_client = OpenAIChatCompletionClient(**config["gemma_model_config"])

async def main() -> None:
    # Define an agent
    web_surfer_agent = MultimodalWebSurfer(
        name="MultimodalWebSurfer",
        model_client=model_client,
        headless=False
    )

    summarizer_agent = AssistantAgent(
        name="summarizer",
        model_client=gemma_client,
        description="You are a summarizer agent. You will summarize the text provided to you. You will only respond with the summary of the text and nothing else."
    )
    # Define a team
    agent_team = RoundRobinGroupChat([web_surfer_agent], max_turns=5)

    # Run the team and stream messages to the console
    stream = agent_team.run_stream(task="search for myanmar earthquake 2025. Type myanmar earthquake 2025 in searchbar, open first link and get the info")
    await Console(stream)
    # Close the browser controlled by the agent
    await web_surfer_agent.close()


asyncio.run(main())

# import asyncio
# from autogen_agentchat.ui import Console
# from autogen_agentchat.teams import RoundRobinGroupChat
# from autogen_ext.models.openai import OpenAIChatCompletionClient
# from autogen_ext.agents.web_surfer import MultimodalWebSurfer
# from autogen_agentchat.agents import AssistantAgent

# import yaml 

# with open("config.yaml", "r") as file:
#     config = yaml.safe_load(file)

# model_client = OpenAIChatCompletionClient(**config["model_config"])

# async def main() -> None:
#     # Define an agent
#     web_surfer_agent = MultimodalWebSurfer(
#         name="MultimodalWebSurfer",
#         model_client=model_client,
#         headless=False,
#         description="You are web researcher who is great in fetching text contents from the websites. Don't take images. If you can't find the information, just say 'I don't know'.",
#     )

#     summarizer_agent = AssistantAgent(
#         name="summarizer_agent",
#         model_client=model_client,
#         description="You are a summarizer who is great in summarizing text contents as short points. If Web_surfer_agent can't find the answer, just say 'I don't know'.",
#     )
#     # Define a team
#     agent_team = RoundRobinGroupChat([web_surfer_agent, summarizer_agent], max_turns=2)

#     # Run the team and stream messages to the console
#     stream = agent_team.run_stream(
#         task="""Search for [Myanmar earthquake 2025] in wikipedia and summarize it.""")
#     await Console(stream)
#     # Close the browser controlled by the agent
#     await web_surfer_agent.close()

# asyncio.run(main())

