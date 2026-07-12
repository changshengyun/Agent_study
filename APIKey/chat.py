import os
from openai import OpenAI
from dotenv import load_dotenv
## 配置APIKEY
# 1.加载 .env 文件
load_dotenv()
api_key = os.getenv("API_KEY")
# 2.环境变量
# api_key=os.environ.get('DEEPSEEK_API_KEY'),

## 初始化客户端
client = OpenAI(
    api_key=api_key,
    base_url="https://api.deepseek.com")

## 访问模型
messages = [{"role": "user", "content": "What's the highest mountain in the world?"}]
response = client.chat.completions.create(
    model="deepseek-v4-pro",
    messages=messages,
    stream=False,
    reasoning_effort="high",
    extra_body={"thinking": {"type": "enabled"}},
    # temperature=1.5,
)
messages.append(response.choices[0].message)
# print(f"Messages Round 1: {messages}")
print(response.choices[0].message.content)

# 多轮对话
messages.append({"role": "user", "content": "What is the second?"})
response = client.chat.completions.create(
    model="deepseek-v4-pro",
    messages=messages,
)

# print(response.model_dump_json)
print(response.choices[0].message.content)

# messages.append(response.choices[0].message)
# print(f"Messages Round 2: {messages}")

# output：
# The highest mountain in the world is **Mount Everest**, with an elevation of 8,848.86 meters (29,031.7 feet) above sea level. It is located in the Himalayas on the border between Nepal and the Tibet Autonomous Region of China.  
# The second highest mountain in the world is **K2**, with an elevation of 8,611 meters (28,251 feet) above sea level. It is located in the Karakoram range, on the border between Pakistan and China.