from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain.agents import create_agent
from langchain_core.messages import ServerToolCall,HumanMessage
import os
import base64
import mimetypes
from pathlib import Path

load_dotenv()
base_url = os.getenv("AGENTSTUDIO_URL")
api_key = os.getenv("DASHSCOPE_API_KEY")

# def model
model = init_chat_model(
    model="qwen3.7-plus",
    model_provider='openai',
    base_url = base_url,
    api_key = api_key,
)

# def agent
agent = create_agent(model=model)

#def message
# url
# message = HumanMessage(
#     content = [
#         {
#             "type": "image_url",
#             "image_url": {
#                 "url": "https://tse1.mm.bing.net/th/id/OIP.kktBSaGQkQC4wGQNgGMjewHaEo?r=0&rs=1&pid=ImgDetMain&o=7&rm=3"
#             },
#         },
#         {"type": "text", "text": "描述一下这张图片"},
# ])

# 本地base64

image_path = Path(r"C:\Users\Legion\Pictures\96780c858ee2bd9cc03983bab4dcd4aa.jpg")
mime_type, _ = mimetypes.guess_type(image_path)
mime_type = mime_type or "image/jpeg"

img_b64 = base64.b64encode(image_path.read_bytes()).decode("utf-8")

message = HumanMessage([
    {"type": "text", "text": "Describe the content of this image."},
    {
            "type": "image",
            "base64": img_b64,
            "mime_type": "image/jpeg",
    },
])

# print(type(message))
# 调用agent
# respone = agent.invoke({"messages":[message]})
# print(respone)
##多模态
response = agent.stream(
    {'messages':[message]},
    stream_mode='messages',
)

for chunk,matedate in response:
    if chunk.content:
        print(chunk.content,end="",flush=True)
# output
## url
######################################################
# (agent-study) PS D:\DevEnv\Agent_study> & d:\DevEnv\Agent_study\.venv\Scripts\python.exe d:/DevEnv/Agent_study/LangChain/Message/messages.py
# 这张图片展示了一个年轻男性的半身肖像，从外貌特征来看，非常像中国艺人**蔡徐坤**（或者是以他为原型制作的AI生成/3D渲染图像）。

# 以下是具体的画面描述：

# 1.  **人物外貌**：
#     *   **发型**：留着标志性的银灰色中分短发，头发看起来比较蓬松。
#     *   **面部**：五官比较立体，但皮肤质感非常光滑，甚至有一种“塑料感”或3D建模的质感，不太像真实的皮肤。眼睛很大，眼神看起来略带惊讶或呆滞。
# 2.  **穿着打扮**：
#     *   他穿着一件浅灰色的西装外套（看起来像是细格纹材质）。
#     *   内搭一件黑色的高领毛衣/打底衫。
#     *   脖子上似乎戴着一条银色的细项链。
# 3.  **表情神态**：
#     *   他的嘴巴微微张开，似乎正在说话，或者处于一种惊讶、错愕的状态。
# 4.  **背景**：
#     *   背景比较简洁，主要是灰白色的墙面，左侧有一点模糊的蓝色色块。

# **总结**：这张图看起来很有可能是基于蔡徐坤形象生成的AI图或3D恶搞图（这类图在网络文化中常被称为“AI坤”或相关的梗图），因为人物的神态和质感带有一种明显的非真实感（类似“恐怖谷”效应）。

## base64
###################################################
# (agent-study) PS D:\DevEnv\Agent_study> & d:\DevEnv\Agent_study\.venv\Scripts\python.exe d:/DevEnv/Agent_study/LangChain/Message/messages.py
# This image shows a top-down view of a white bowl filled with a thick, beige dipping sauce—likely sesame paste, which is a staple for Chinese hot pot. The sauce has been playfully decorated to resemble a smiley face:

# *   **Nose:** A cluster of white sesame seeds sits in the center.
# *   **Left Eye:** A small dollop of green sauce (likely chive flower sauce) is placed on the left.
# *   **Right Eye:** A dollop of dark sauce (likely soy sauce or vinegar) is placed on the right.
# *   **Mouth:** A curved line of reddish-pink sauce (likely chili oil or fermented bean curd) forms a wide smile at the bottom.

# The bowl has a logo and Chinese characters printed on the inner rim that read "南门涮肉" (Nanmen Shuanrou), a famous hot pot restaurant chain. 
# To the right of the bowl, there is a pair of wooden chopsticks and a decorative tray with a brown and white geometric lattice pattern. The items are resting on a grey, marble-patterned table.
