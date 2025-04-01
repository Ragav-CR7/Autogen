import asyncio
import yaml

from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.conditions import TextMentionTermination
from autogen_agentchat.teams import RoundRobinGroupChat
from autogen_agentchat.ui import Console
from autogen_core import CancellationToken
from autogen_ext.models.openai import OpenAIChatCompletionClient


with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

model_client = OpenAIChatCompletionClient(**config["model_config"])

async def team():
    # Create the primary agent.
    primary_agent = AssistantAgent(
        "primary",
        model_client=model_client,
        system_message="You are an expert in dynamic programming who explains the concepts in detail.",
    )

    # Create the critic agent.
    critic_agent = AssistantAgent(
        "critic",
        model_client=model_client,
        system_message="Provide constructive feedback. Respond with 'APPROVE' to when your feedbacks are addressed.",
    )

    # Define a termination condition that stops the task if the critic approves.
    text_termination = TextMentionTermination("APPROVE")

    # Create a team with the primary and critic agents.
    team = RoundRobinGroupChat([primary_agent, critic_agent], termination_condition=text_termination, max_turns=2)


    result = team.run_stream(task="Explain how dynamic programming works with an example.", cancellation_token=CancellationToken())
    await Console(result)

# Run the async function
asyncio.run(team())