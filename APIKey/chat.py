import os

from dotenv import load_dotenv
from openai import OpenAI


def create_client() -> OpenAI:
    """创建并返回 DeepSeek API 客户端。"""
    load_dotenv()

    api_key = os.getenv("API_KEY")
    if not api_key:
        raise RuntimeError(
            "未读取到 DEEPSEEK_API_KEY，请检查 .env 文件。"
        )

    return OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com",
    )


def main() -> None:
    client = create_client()

    messages: list[dict[str, str]] = [
        {
            "role": "system",
            "content": (
                "You are a helpful assistant. "
                "Answer factual questions clearly and concisely."
            ),
        },
        {
            "role": "user",
            "content": "What's the highest mountain in the world?",
        },
    ]

    # 第一轮对话
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

    first_answer = response.choices[0].message.content
    if first_answer is None:
        raise RuntimeError("第一轮模型返回内容为空。")

    print("第一轮回答：")
    print(first_answer)

    messages.append(
        {
            "role": "assistant",
            "content": first_answer,
        }
    )

    # 第二轮用户输入
    messages.append(
        {
            "role": "user",
            "content": "What is the second?",
        }
    )

    # 第二轮对话
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

    second_answer = response.choices[0].message.content
    if second_answer is None:
        raise RuntimeError("第二轮模型返回内容为空。")

    print("\n第二轮回答：")
    print(second_answer)

    # 查看停止原因
    print("\n停止原因：")
    print(response.choices[0].finish_reason)

    # 查看 Token 消耗
    if response.usage:
        print("\nToken Usage：")
        print(f"输入 Token：{response.usage.prompt_tokens}")
        print(f"输出 Token：{response.usage.completion_tokens}")
        print(f"总 Token：{response.usage.total_tokens}")


if __name__ == "__main__":
    main()