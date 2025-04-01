import asyncio
from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_ext.teams.magentic_one import MagenticOne
from autogen_agentchat.ui import Console
import yaml

with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

client = OpenAIChatCompletionClient(**config["model_config"])

async def example_usage():
    # client = OpenAIChatCompletionClient(model="gpt-4o")
    m1 = MagenticOne(client=client)
    task = "Browse for myanmar earthquake 2025 in wikipedia and summarize it."
    result = await Console(m1.run_stream(task=task))
    print(result)

asyncio.run(example_usage())
