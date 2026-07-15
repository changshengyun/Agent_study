1. LangChain 的基本定位
LangChain 的作用：

LangChain 是位于业务应用和模型 API 之间的一层开发框架，用来封装模型调用、消息、Prompt、工具、Agent、输出解析和运行流程。
原始模型 API 调用链路是：

Python 程序
→ OpenAI SDK
→ 模型 API
→ 模型返回结果

使用 LangChain 后，调用链路变成：

Python 程序
→ LangChain 模型对象
→ 模型 Provider SDK/API
→ 模型服务

LangChain 并没有取代模型 API。

它主要是在模型 API 之上增加：

统一的模型对象；
统一的消息结构；
Prompt 模板；
输出处理；
工具封装；
Agent 控制；
链式组合能力。

2.model和agent输入输出formats的区别
Model：消息 → AIMessage
Agent：状态字典 → 更新后的状态字典

1）model
（1）Model 请求格式
-模型可以接收一个字符串
response = model.invoke("请解释什么是 Transformer")

-也可以接收消息列表：
messages = [
    {
        "role": "system",
        "content": "你是一名 AI 学习助手。"
    },
    {
        "role": "user",
        "content": "请解释什么是 Transformer。"
    }
]

response = model.invoke(messages)

-也可以使用 LangChain 的消息对象：
from langchain_core.messages import SystemMessage, HumanMessage

messages = [
    SystemMessage(content="你是一名 AI 学习助手。"),
    HumanMessage(content="请解释什么是 Transformer。"),
]

response = model.invoke(messages)
（2）Model 响应格式
-非流式情况下
response = model.invoke(messages)
type：AIMessage类
-它大致包含：
AIMessage(
    content="Transformer 是一种基于注意力机制的神经网络架构。",
    //模型调用工具
    tool_calls=[],
    //获取底层模型响应信息
    response_metadata={...},
    //获取 Token 使用情况
    usage_metadata={...},
    id="..."
)
print(response.content)

2）agent
（1）请求
result = agent.invoke({
    "messages": [
        {
            "role": "user",
            "content": "请查询论文的 Method 部分并总结。"
        }
    ]
})
（2）响应
{
    "messages": [...]
}
-ex：
{
    "messages": [
        HumanMessage(
            content="北京天气怎么样？"
        ),
        AIMessage(
            content="",
            tool_calls=[
                {
                    "name": "get_weather",
                    "args": {
                        "city": "北京"
                    },
                    "id": "call_001"
                }
            ]
        ),
        ToolMessage(
            content="北京今天晴，25 摄氏度。",
            tool_call_id="call_001"
        ),
        AIMessage(
            content="北京今天天气晴朗，气温约 25 摄氏度。"
        )
    ]
}
-因此获取最终答案时通常写：
final_message = result["messages"][-1]

print(final_message.content)