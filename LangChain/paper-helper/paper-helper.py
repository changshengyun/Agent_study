from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage,SystemMessage,AIMessage
import os
from dotenv import load_dotenv

# load env
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
agent = create_agent(model = model)

# build message
system_prompt = """
你是一个AI领域的论文分析助手，辅助用户阅读论文。

要求：
1. 所有内容用中文回答
2. 对于第一次出现的专业名词，要有他的英文名称对照，并且在文本最后有对应附加解释。
3.依据用户提供的论文标题和摘要进行分析，使用论文正文、外部知识或模型记忆补充信息必须标注并且说明来源。
4.无法确认的信息必须明确标记为不确定。

约束：
1.专业术语处理规则：
（1）主动识别文中影响理解的 AI、机器学习和自然语言处理专业术语，不要只解释缩写。
（2）每个专业术语第一次出现时，统一写为：中文名称（English Term，缩写）
（3）至少识别并解释摘要中的核心术语，包括但不限于：
- 方法或模型名称；
- 任务类型；
- 模型架构；
- 评价与实验相关概念。
（4）正文分析结束后，必须增加“专业术语解释”章节
（5）术语解释统一使用以下格式：
中文名称（English Term，缩写）：结合当前摘要语境，用 1～3 句话解释其含义及在本文中的作用。
（6）只解释当前输入中实际出现的术语，不得为了补充术语表而引入摘要之外的技术。如果必须引入，需要附加对应专业术语的解释。
""".strip()
# 多行输入，空行结束
def input_multiline(prompt: str) -> str:
    print(prompt)
    lines = []

    while True:
        line = input()
        if not line:
            break
        lines.append(line)

    return "\n".join(lines)

paper_title = input_multiline("请输入论文名称，输入空行结束：")
paper_context = input_multiline("请输入论文摘要，输入空行结束：")

human_prompt = f"""
分析这篇论文的摘要部分：
论文名称：{paper_title}
论文摘要：{paper_context}

输出顺序：
1. 摘要总结，核心内容
2. 按照学术摘要的结构划分段都，逐段落分析
3. 专业术语解释
4. 不确定信息
""".strip()

message = [
    HumanMessage(human_prompt),
]

response = agent.stream(
    {'messages':message},
    system_prompt = system_prompt,
    stream_mode="messages",
)

for chunk,matedata in response:
    if chunk.content:
        print(chunk.content, end="", flush=True)
    # print(matedata)
