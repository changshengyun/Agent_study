# N2 学习记录：大模型 API 基础调用与多轮会话

## 1. 今日学习目标

本阶段主要解决两个问题：

1. 应用程序如何通过 API 调用一个大语言模型；
2. 无状态模型 API 如何实现多轮对话。

今天已经完成：

* 认识模型 API 的基本组成；
* 使用 API Key 完成身份认证；
* 使用 cURL 调用 DeepSeek Chat Completions API；
* 使用 OpenAI Python SDK 调用 DeepSeek；
* 理解 `model`、`messages`、`stream` 等请求参数；
* 理解无状态 API 的多轮会话机制；
* 使用 Python 完成两轮连续对话。

---

# 2. 模型 API 是什么

模型 API 是应用程序与模型服务之间的一套调用契约。

它规定：

```text
请求发送到哪里
+ 如何认证
+ 请求中包含哪些字段
+ 模型返回什么结构
+ 如何处理流式输出
+ 如何报告 Token 消耗
+ 请求失败时返回什么错误
```

模型 API 通常建立在 HTTP 协议之上。

完整调用链路为：

```text
Python 程序或 Agent
→ 构造 HTTP 请求
→ 发送到模型 API Endpoint
→ 模型服务完成推理
→ 返回 HTTP 响应
→ 程序解析模型结果
```

---

# 3. 一次模型 API 请求的组成

一次 HTTP API 请求主要包含：

```text
HTTP Method
+ URL / Endpoint
+ Request Headers
+ Request Body
```

以 DeepSeek 为例：

```bash
curl https://api.deepseek.com/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${DEEPSEEK_API_KEY}" \
  -d '{
        "model": "deepseek-v4-pro",
        "messages": [
          {
            "role": "system",
            "content": "You are a helpful assistant."
          },
          {
            "role": "user",
            "content": "Hello!"
          }
        ],
        "thinking": {
          "type": "enabled"
        },
        "reasoning_effort": "high",
        "stream": false
      }'
```

---

## 3.1 HTTP Method

模型生成接口通常使用：

```text
POST
```

因为应用程序需要向服务器提交：

* 用户消息；
* 历史消息；
* 模型名称；
* 生成参数；
* 工具定义。

---

## 3.2 URL 与 Endpoint

本次使用的 Endpoint 是：

```text
https://api.deepseek.com/chat/completions
```

可以拆成：

```text
Base URL：
https://api.deepseek.com

API Path：
/chat/completions
```

Endpoint 表示：

> 当前请求具体要访问模型服务中的哪个功能接口。

DeepSeek 还提供 `/models` 等其他接口，因此 Base URL 相同，不同 Path 对应不同能力。

---

## 3.3 Request Headers

请求头负责携带认证和请求元数据。

本次使用了：

```http
Content-Type: application/json
Authorization: Bearer ${DEEPSEEK_API_KEY}
```

### `Content-Type`

表示请求体的数据格式是 JSON：

```http
Content-Type: application/json
```

### `Authorization`

表示使用 Bearer Token 进行认证：

```http
Authorization: Bearer API_KEY
```

API Key 通常放在 Header 中，而不是放在普通 Request Body 中。

---

## 3.4 Request Body

Request Body 包含模型真正需要处理的数据和生成参数。

本次主要字段包括：

| 参数                 | 作用             |
| ------------------ | -------------- |
| `model`            | 指定调用哪个模型       |
| `messages`         | 提供当前对话上下文      |
| `thinking`         | 开启或关闭思考模式      |
| `reasoning_effort` | 控制推理投入程度       |
| `stream`           | 决定响应是流式还是一次性返回 |

---

# 4. 核心请求参数

## 4.1 `model`

```python
model="deepseek-v4-pro"
```

用于指定实际调用的模型。

模型选择会影响：

* 推理能力；
* 响应速度；
* Token 价格；
* 上下文长度；
* 工具调用能力；
* 输出质量。

当前代码使用的是偏高质量推理场景的 `deepseek-v4-pro`。

---

## 4.2 `messages`

`messages` 表示当前模型能够看到的对话上下文。

基本格式：

```python
messages = [
    {
        "role": "system",
        "content": "You are a helpful assistant."
    },
    {
        "role": "user",
        "content": "Hello!"
    }
]
```

常见角色包括：

| Role        | 作用              |
| ----------- | --------------- |
| `system`    | 定义模型的角色、规则和行为要求 |
| `user`      | 用户输入            |
| `assistant` | 模型之前的回答         |
| `tool`      | 工具执行后的返回结果      |

消息顺序非常重要，因为模型会按顺序读取当前上下文。

---

## 4.3 `stream`

```python
stream=False
```

表示模型完成全部生成后，一次性返回完整响应。

如果设置：

```python
stream=True
```

服务器会在生成过程中不断返回响应片段。

需要区分：

```text
自回归生成：
模型内部逐 Token 生成

Streaming：
服务器如何将已生成的内容传给客户端
```

无论 `stream` 是 `True` 还是 `False`，模型内部通常仍然逐 Token 生成。

---

## 4.4 `thinking`

```python
extra_body={
    "thinking": {
        "type": "enabled"
    }
}
```

表示开启思考模式。

在使用 OpenAI SDK 调用 DeepSeek 时，DeepSeek 特有但 SDK 方法签名中没有直接定义的字段，可以通过 `extra_body` 传递。

例如：

```python
extra_body={
    "thinking": {
        "type": "disabled"
    }
}
```

可以关闭思考模式。

---

## 4.5 `reasoning_effort`

```python
reasoning_effort="high"
```

用于控制模型在推理任务上的计算投入。

当前 DeepSeek API 支持的主要级别包括：

```text
high
max
```

一般理解为：

```text
high：
常规高质量推理

max：
复杂 Agent、代码或高难度推理任务
```

推理投入更高通常可能带来：

* 更长的推理过程；
* 更高的 Token 消耗；
* 更高延迟；
* 在复杂任务上更好的结果。

它并不保证任何任务都一定得到正确答案。

---

## 4.6 `temperature`

代码中暂时注释了：

```python
# temperature=1.5
```

Temperature 用于调整 Token 概率分布。

```text
低 Temperature：
输出更稳定、更集中

高 Temperature：
输出更多样、更随机
```

对于事实问答、信息提取和工具参数生成，一般不建议使用过高的 Temperature。

`1.5` 对“世界最高山峰”这类事实问答没有明显必要，还可能增加回答波动。

---

# 5. API Key 的正确管理

代码使用：

```python
load_dotenv()
api_key = os.getenv("API_KEY")
```

表示从 `.env` 文件加载 API Key。

例如项目目录中的 `.env`：

```env
DEEPSEEK_API_KEY=你的真实密钥
```

推荐代码统一写成：

```python
api_key = os.getenv("DEEPSEEK_API_KEY")
```

不建议同时使用：

```text
API_KEY
DEEPSEEK_API_KEY
```

两个不同名称，否则容易出现环境变量读取错误。

推荐规范：

```text
OPENAI_API_KEY
DEEPSEEK_API_KEY
ANTHROPIC_API_KEY
GEMINI_API_KEY
```

这样可以清楚区分不同 Provider。

---

## 5.1 `.env` 文件注意事项

`.env` 中包含真实密钥，因此必须加入 `.gitignore`：

```gitignore
.env
```

可以额外提供一个不包含真实密钥的模板：

```text
.env.example
```

内容：

```env
DEEPSEEK_API_KEY=
```

代码中还应验证环境变量是否成功读取：

```python
if not api_key:
    raise RuntimeError(
        "未读取到 DEEPSEEK_API_KEY，请检查 .env 文件。"
    )
```

---

# 6. OpenAI SDK 为什么可以调用 DeepSeek

你的代码使用：

```python
from openai import OpenAI
```

但调用的是 DeepSeek，而不是 OpenAI。

这是因为 DeepSeek 提供了与 OpenAI Chat Completions 兼容的接口格式。

通过修改：

```python
base_url="https://api.deepseek.com"
```

OpenAI SDK 会把请求发送给 DeepSeek，而不是 OpenAI。

调用关系是：

```text
OpenAI Python SDK
→ 负责构造兼容格式的 HTTP 请求
→ DeepSeek Base URL
→ DeepSeek API
```

因此：

> OpenAI SDK 在这里是客户端工具，不代表实际调用的是 OpenAI 模型。

---

# 7. API 为什么是无状态的

DeepSeek Chat Completions API 是无状态 API。

无状态表示：

> 服务端不会因为你使用相同 API Key，就自动记住上一轮对话。

第一次调用：

```python
messages = [
    {
        "role": "user",
        "content": "What's the highest mountain in the world?"
    }
]
```

模型回答：

```text
The highest mountain is Mount Everest.
```

如果第二次只发送：

```python
messages = [
    {
        "role": "user",
        "content": "What is the second?"
    }
]
```

模型不知道：

```text
“the second”指的是什么。
```

因为上一轮内容没有传递。

---

# 8. 多轮对话的实现原理

要实现多轮对话，客户端必须维护历史消息。

完整流程：

```text
第一轮用户消息
→ 调用 API
→ 获得模型回答
→ 将回答添加到 messages

第二轮用户消息
→ 添加到 messages
→ 把完整 messages 再次发送给 API
```

最终第二轮请求实际携带：

```python
[
    {
        "role": "user",
        "content": "What's the highest mountain in the world?"
    },
    {
        "role": "assistant",
        "content": "The highest mountain in the world is Mount Everest."
    },
    {
        "role": "user",
        "content": "What is the second?"
    }
]
```

所以模型能够理解：

```text
“the second”
=
世界第二高峰
```

---

# 9. 当前多轮代码分析

你的代码：

```python
messages.append(response.choices[0].message)
```

这种写法是可行的，DeepSeek 官方多轮对话示例也采用了直接追加返回消息对象的方式。

不过为了让程序更容易调试、持久化和跨 SDK 使用，也可以显式转换为普通字典：

```python
assistant_message = {
    "role": "assistant",
    "content": response.choices[0].message.content,
}

messages.append(assistant_message)
```

两种方式区别如下：

| 写法                  | 优点              | 缺点         |
| ------------------- | --------------- | ---------- |
| 直接追加 SDK Message 对象 | 简洁，能保留更多字段      | 与 SDK 类型耦合 |
| 转换为字典               | 容易保存为 JSON，结构清楚 | 需要手动保留额外字段 |

普通文本多轮对话中，两种方式都可以。

---

# 10. 经过改进的完整代码

```python
import os

from dotenv import load_dotenv
from openai import OpenAI


def create_client() -> OpenAI:
    """创建并返回 DeepSeek API 客户端。"""
    load_dotenv()

    api_key = os.getenv("DEEPSEEK_API_KEY")
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
```

---

# 11. 原代码中需要改进的地方

## 11.1 环境变量名称需要统一

原代码中出现：

```text
DEEPSEEK_API_KEY
API_KEY
```

推荐统一为：

```text
DEEPSEEK_API_KEY
```

---

## 11.2 第二轮参数应保持一致

第一轮使用了：

```python
reasoning_effort="high"
extra_body={"thinking": {"type": "enabled"}}
```

第二轮没有写这些参数。

当前模型默认开启 Thinking，因此代码未必报错，但从代码可读性和实验控制角度看，建议两轮保持相同配置。

否则无法清楚判断：

> 两轮结果差异来自上下文，还是来自生成配置发生了变化。

---

## 11.3 应检查返回值是否为空

不应直接假定：

```python
response.choices[0].message.content
```

一定存在。

工具调用、拒绝、异常响应或特定模型行为下，`content` 可能为空。

因此应增加：

```python
if response.choices[0].message.content is None:
    raise RuntimeError("模型未返回文本内容。")
```

---

## 11.4 应读取 `finish_reason`

```python
response.choices[0].finish_reason
```

可以帮助判断生成为什么停止。

可能的情况包括：

* 正常停止；
* 达到最大长度；
* 产生工具调用；
* 内容过滤。

如果因为长度上限被截断，就不能把回答视为完整结果。

---

## 11.5 应读取 `usage`

```python
response.usage
```

可以查看本次请求的 Token 使用量。

这是以后实现以下功能的基础：

* 成本统计；
* 上下文长度监控；
* 模型选择；
* 用户预算；
* 网关限额；
* Agent 调用成本分析。

---

# 12. 多轮对话的工程问题

虽然把所有历史消息继续加入 `messages` 可以实现会话记忆，但它会产生上下文膨胀。

随着对话增加：

```text
第 1 轮：
用户 1 + 模型 1

第 10 轮：
用户 1 + 模型 1
+ 用户 2 + 模型 2
+ ...
+ 用户 10
```

每一次请求都需要重新发送历史记录，因此会带来：

* 输入 Token 增加；
* 费用增加；
* Prefill 延迟增加；
* Context Window 被占用；
* 无关信息增加；
* 模型混淆历史内容。

后续需要引入：

* 历史消息裁剪；
* 对话摘要；
* Sliding Window；
* 外部 Memory；
* 只检索与当前问题相关的历史；
* 对话状态结构化保存。

所以：

```text
messages 保存历史
=
最基础的短期会话记忆

不等于
=
完整的 Agent 长期记忆系统
```

---

# 13. 思考模式下的多轮对话注意事项

普通文本多轮对话中，将模型的 assistant 消息追加回 `messages` 即可。

但在 Thinking Mode 与 Tool Calling 结合时，需要额外注意 `reasoning_content` 的传递。DeepSeek 官方说明：发生工具调用的思考轮次中，后续请求需要完整传回相应的 `reasoning_content`；否则可能导致上下文或接口错误。

这属于后续 Function Calling 阶段的知识，目前只需要先记住：

```text
普通文本多轮：
保存 role 和 content

思考模式 + 工具调用：
还可能需要保存 reasoning_content、tool_calls 和 tool 结果
```

---

# 14. 当前形成的标准认知

模型 API 是应用程序与模型服务之间的调用契约。一次基本请求包括 HTTP Method、Endpoint、Headers 和 Request Body。API Key 通常通过 Authorization Header 传递，用于服务端认证。

`model` 决定调用哪个模型，`messages` 提供当前上下文，`stream` 决定响应传输方式，`thinking` 和 `reasoning_effort` 控制推理模式及推理投入。

Chat Completions API 通常是无状态的。服务端不会自动记住上一轮对话。多轮会话由客户端维护 `messages`，将历史用户消息和模型回答在下一次请求中重新发送。

因此：

```text
API 多轮会话
=
客户端保存历史
+ 每轮重传相关上下文
```

而不是模型服务端自动拥有永久记忆。

---

# 15. 当前知识盲区

## 盲区一：将 API Key 和 API 参数放在同一层理解

需要区分：

```text
API Key：
身份认证凭证

model、messages、stream：
业务请求参数
```

API Key 不是模型生成参数。

---

## 盲区二：将 messages 等同于永久记忆

`messages` 只是在当前请求中传给模型的上下文。

真正的长期记忆需要外部系统保存、筛选和检索。

---

## 盲区三：当前只读取了回答文本

生产级调用不能只读取：

```python
response.choices[0].message.content
```

还应观察：

* `finish_reason`；
* `usage`；
* `model`；
* Request ID；
* 工具调用；
* 错误类型；
* 延迟。

---

# 16. 三个关键补充

## 补充一：SDK 是调用工具，不是模型服务

```text
OpenAI SDK
≠ OpenAI 模型
```

SDK 只负责构建请求、发送请求和解析响应。

通过修改 `base_url`，它可以调用兼容 OpenAI 接口格式的其他 Provider。

---

## 补充二：多轮会话的成本会逐轮增加

由于每次都要重新发送历史消息：

```text
对话越长
→ 输入 Token 越多
→ Prefill 越慢
→ 成本越高
```

因此 Agent 必须管理 Context，而不是无限追加消息。

---

## 补充三：HTTP 调用成功不等于业务成功

完整成功至少包括：

```text
HTTP 调用成功
→ 模型有有效输出
→ 输出没有被截断
→ 格式符合要求
→ 内容满足当前任务
```

`HTTP 200` 只能证明请求在接口层成功，不能证明回答正确。

---
