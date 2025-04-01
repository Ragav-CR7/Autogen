from autogen_agentchat.agents import AssistantAgent, UserProxyAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_core import CancellationToken
from autogen_ext.models.openai import OpenAIChatCompletionClient
import asyncio
import yaml 

with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

model_client = OpenAIChatCompletionClient(**config["model_config"])
assistant = AssistantAgent("assistant", model_client=model_client)
user_proxy = UserProxyAgent("user_proxy", input_func=input)  # Use input() to get user input from console.

# Create the termination condition which will end the conversation when the user says "APPROVE".
termination = TextMentionTermination("APPROVE")

# Create the team.
team = RoundRobinGroupChat([assistant, user_proxy], termination_condition=termination, max_turns=4)

stream = team.run_stream(task="Create a 4 lines poem in english which should be linked with aliens.", cancellation_token=CancellationToken())
asyncio.run(Console(stream))
