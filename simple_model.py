from autogen_core.models import UserMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
import asyncio
import yaml 

# model_client = OpenAIChatCompletionClient(
#     model="gemma3:1b",
#     base_url="http://127.0.0.1:11434/v1/", 
#     api_key="key",  
#     model_info={
#         "vision": False,
#         "function_calling": False,
#         "json_output": False,
#         "family": "gemma",
#     },
# )

with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

model_client = OpenAIChatCompletionClient(**config["model_config"])

response = asyncio.run(model_client.create([UserMessage(content="What is the capital of Tamil Nadu?", source="user")]))
print(response)