# 1.引入依赖
from dotenv import load_dotenv
load_dotenv()
from langchain.chat_models import init_chat_model
# 2.配置环境API_KEY

## 3. init models
# model用来指定模型名字，langchain会自动获取base_url和api_key
model = init_chat_model(model="deepseek-chat")
# 如果使用langchain不支持的model。比如qwen-max，
### (1)自定义模型参数来访问
# import os
# base_url = os.getenv("DEEPSEEK_BASE_URL")
# api_key = os.getenv("DASHSCOPE_API_KEY")
# model = init_chat_model(
#     model="qwen-max",
#     model_provider='openai',
#     base_url=base_url,
#     api_key=api_key,
# )
### (2)使用langchain-community提供的模型适配器来访问
# from langchain_community.chat_models.tongyi import ChatTongyi
# model = ChatTongyi(model="qween-max")

## 4.调用模型：invoke(阻塞式)/stream(流式)方法可以直接调用模型，传入messages参数即可
### （1）invoke模式下，返回的是一个完整的response对象
# response = model.invoke("hello, how are you?")
# print(response.content)

### （2）stream模式下，返回的是一个迭代器，可以边接收边处理
response = model.stream("hello, how are you?")
for chunk in response:
    print(chunk.content)

