import os

from dotenv import load_dotenv
from openai import OpenAI

# 配置apikey
load_dotenv()

# 初始化客户端
client = OpenAI(
    api_key=os.getenv("API_KEY"),
    base_url="https://api.deepseek.com")

messages=[
        {"role": "system", "content": "You are a helpful assistant"},
        {"role": "user", "content": "Hello"},
    ]

# 发送请求
response = client.chat.completions.create(
        model="deepseek-v4-pro",
        messages=messages,
        stream=False,
        reasoning_effort="high",
        extra_body={
            "thinking": {
                "type": "enabled",
            }
        },
    )

# 输出结果
print(response.choices[0].message.content)