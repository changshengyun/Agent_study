from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
from langchain_core.messages import SystemMessage,HumanMessage
import os
load_dotenv()

base_url = os.getenv("AGENTSTUDIO_URL")
api_key = os.getenv("DASHSCOPE_API_KEY")

# create model
model = init_chat_model(
    model = "qwen3.7-plus",
    model_provider = "openai",
    base_url = base_url,
    api_key = api_key,
)

# create agent
agent = create_agent(
    model = model,
)

# build messages
## prompt




