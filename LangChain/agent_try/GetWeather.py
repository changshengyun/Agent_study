# how to develop agent?

# 1.加载环境变量
## don't need os to load .env file, just use load_dotenv() from dotenv
## because langchain will use os.environ to get the env variables
from dotenv import load_dotenv
load_dotenv()

# 2.def tools
from langchain.tools import tool

@tool
def getweather(location: str) -> str:
    """Get the weather of a location."""
    return f"Current weather in {location} is sunny."

# 3.def agent
from langchain.agents import create_agent

agent = create_agent(
    # model name
    "deepseek-chat",
    tools=[getweather],
)

# 3.调用 agent
print("正在调用大模型")
response = agent.invoke({
    "messages" : [
        {"role": "user", "content": "What's the weather in Beijing,today?"},
    ]
})

# print(response)
for message in response["messages"]:
    print(message.model_dump_json(indent=2))
    print("--------------------------------------------------")

# output:
# (agent-study) PS D:\DevEnv\Agent_study> & d:\DevEnv\Agent_study\.venv\Scripts\python.exe d:/DevEnv/Agent_study/LangChain/search.py
# 正在调用大模型
# {
#   "content": "What's the weather in Beijing,today?",
#   "additional_kwargs": {},
#   "response_metadata": {},
#   "type": "human",
#   "name": null,
#   "id": "9c9cff38-7b79-4067-804e-84e8895ff625"
# }
# --------------------------------------------------
# {
#   "content": "Let me check the weather in Beijing for you.",
#   "additional_kwargs": {
#     "refusal": null
#   },
#   "response_metadata": {
#     "token_usage": {
#       "completion_tokens": 53,
#       "prompt_tokens": 281,
#       "total_tokens": 334,
#       "completion_tokens_details": null,
#       "prompt_tokens_details": {
#         "audio_tokens": null,
#         "cache_write_tokens": null,
#         "cached_tokens": 256
#       },
#       "prompt_cache_hit_tokens": 256,
#       "prompt_cache_miss_tokens": 25
#     },
#     "model_provider": "deepseek",
#     "model_name": "deepseek-v4-flash",
#     "system_fingerprint": "fp_8b330d02d0_prod0820_fp8_kvcache_20260402",
#     "id": "936ff399-2842-4b98-8289-6655ee971a4e",
#     "finish_reason": "tool_calls",
#     "logprobs": null
#   },
#   "type": "ai",
#   "name": null,
#   "id": "lc_run--019f5f88-3345-7e00-b846-811e3d82d31a-0",
#   "tool_calls": [
#     {
#       "name": "getweather",
#       "args": {
#         "location": "Beijing"
#       },
#       "id": "call_00_2DHBIJmx2c3YHEhBSWfB4099",
#       "type": "tool_call"
#     }
#   ],
#   "invalid_tool_calls": [],
#   "usage_metadata": {
#     "input_tokens": 281,
#     "output_tokens": 53,
#     "total_tokens": 334,
#     "input_token_details": {
#       "cache_read": 256
#     },
#     "output_token_details": {}
#   }
# }
# --------------------------------------------------
# {
#   "content": "Current weather in Beijing is sunny.",
#   "additional_kwargs": {},
#   "response_metadata": {},
#   "type": "tool",
#   "name": "getweather",
#   "id": "90f23b51-cce6-42a9-84fe-6d0bb5324130",
#   "tool_call_id": "call_00_2DHBIJmx2c3YHEhBSWfB4099",
#   "artifact": null,
#   "status": "success"
# }
# --------------------------------------------------
# {
#   "content": "The current weather in Beijing today is **☀️ sunny**! \n\nIf you need more details like temperature or wind condittions, feel free to ask!",
#   "additional_kwargs": {
#     "refusal": null
#   },
#   "response_metadata": {
#     "token_usage": {
#       "completion_tokens": 31,
#       "prompt_tokens": 351,
#       "total_tokens": 382,
#       "completion_tokens_details": null,
#       "prompt_tokens_details": {
#         "audio_tokens": null,
#         "cache_write_tokens": null,
#         "cached_tokens": 256
#       },
#       "prompt_cache_hit_tokens": 256,
#       "prompt_cache_miss_tokens": 95
#     },
#     "model_provider": "deepseek",
#     "model_name": "deepseek-v4-flash",
#     "system_fingerprint": "fp_8b330d02d0_prod0820_fp8_kvcache_20260402",
#     "id": "164f271c-35de-4275-b9dc-2ddc756cf130",
#     "finish_reason": "stop",
#     "logprobs": null
#   },
#   "type": "ai",
#   "name": null,
#   "id": "lc_run--019f5f88-37aa-7dc0-89d2-82e575c10ebf-0",
#   "tool_calls": [],
#   "invalid_tool_calls": [],
#   "usage_metadata": {
#     "input_tokens": 351,
#     "output_tokens": 31,
#     "total_tokens": 382,
#     "input_token_details": {
#       "cache_read": 256
#     },
#     "output_token_details": {}
#   }
# }
# --------------------------------------------------