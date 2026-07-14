# 1.create agent
# 2.调用agent
# agent调用时必须传入一个dict对象，里面必须包含一个messages字段，包含role和content两个dict
# agent的response比model多一些字段，
# （1）invoke模式下，返回的是一个完整的response对象
# （2）stream模式下，返回的是一个迭代器，可以边接收边处理

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain_core.messages import SystemMessage,HumanMessage,AIMessage

load_dotenv()

# 调用agent:传统dict/面向对象
# langchain里面，它会把消息做封装，调用简洁，调试方便

# def models
model = init_chat_model(model="deepseek-chat")

# def tools
from langchain.tools import tool
@tool
def getweather(location: str) -> str:
    """Get the weather of a location."""
    return f"Current weather in {location} is sunny."

# def agent

agent = create_agent(
    model=model,
    tools=[getweather],
)


# (1)invoke

# response = agent.invoke({
#     "messages" :[
#         SystemMessage("你是一个热心的ai助手"),
#         HumanMessage("你好我是Tim"),
#         AIMessage("你好，Tim"),
#         HumanMessage("北京天气如何？"),
#     ]
# })
# # print(response)
# for message in response['messages']:
#     message.pretty_print()

# (2)stream

messages = [
        SystemMessage("你是一个热心的ai助手"),
        HumanMessage("你好我是Tim"),
        AIMessage("你好，Tim"),
        HumanMessage("北京天气如何？"),
]

for chunk,metadata in agent.stream({'messages':messages},stream_mode="messages"):
    # print(chunk.content, end="",flush=True)
    print("\n节点：", metadata.get("langgraph_node"))
    print("类型：", type(chunk).__name__)
    print("内容：", chunk.content)
    print("工具片段：", getattr(chunk, "tool_call_chunks", None))