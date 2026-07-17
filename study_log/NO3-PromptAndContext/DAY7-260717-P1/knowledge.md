# 1.Prompt Engineering 深入学习
## 1.1 总结
- Prompt Engineering 定义
- Prompt Version Management
- Few-shot 
- Structured Output
- Prompt Evaluation
## 1.2 Prompt 的结构化设计
- 身份、目标、指令、示例、约束、边界、输出限制、检测、评估
## 1.3 Prompt Template
- prompt = 固定部分 + 动态内容
- Prompt Template 接收变量，并生成最终发送给模型的 Prompt。
模板：

template = """
你是一名{role}

任务：
{task}

输入：
{input}
"""

运行：

template.format(
 role="论文助手",
 task="总结论文",
 input="Transformer论文"
)

生成：
你是一名论文助手

任务：
总结论文

输入：
Transformer论文

# 2. Context Engineering 深入学习
## 2.1 总结
- Context Engineering 的核心是：给 Agent 提供完成任务所需的正确信息和工具，并以正确格式组织。存储、选择、压缩、隔离
- Context 组成：系统prompt、messages、tools、tool result、memory、rag、user input、state
- Context Ranking：组成元素按优先级排序（提升token命中率、提高输出质量）
- Context Window Management：
成本
Token 越多：
费用越高。
延迟
输入越长：
Prefill 越慢。
质量
信息过多：
注意力分散。
- Memory Management：Short / Long
- Task State
State 用于：
多节点间传递数据；
保存中间结果；
控制执行分支；
记录重试次数；
支持暂停和恢复；
保存当前任务进度。
## 2.2 Context Injection
## 2.3 context builder
-Context Builder 负责决定：
哪些信息需要进入本轮模型调用？
以什么顺序放进去？
使用原文还是摘要？
保留多少历史 Message？
调用哪些 Memory？
是否加入工具结果？

- 例如完整 State 是：
state = {
    "messages": [...],
    "paper_id": "paper-001",
    "method_text": "...",
    "experiment_text": "...",
    "retry_count": 2,
    "current_node": "evaluate",
    "debug_log": "...",
    "user_permission": "read_only"
}
Context Builder 可能只选择：
System Instruction
+ 最近 4 条 Messages
+ method_text
+ experiment_text

- Context Builder 最后会形成一个类似这样的请求：
model_input = [
    SystemMessage(
        content="你是论文实验评审助手。所有判断必须引用证据。"
    ),
    HumanMessage(
        content="判断这篇论文的实验是否充分验证了方法。"
    ),
    HumanMessage(
        content=f"""
方法部分：
{state["method_text"]}

实验部分：
{state["experiment_text"]}

用户偏好：
- 必须区分作者结论和模型推断
- 必须检查消融实验
"""
    )
]

result = model.invoke(model_input)
这里模型看到的是 model_input，而不是整个 state。

# 3. 安全部分
## 3.1 Prompt Injection
- Direct Injection / Indirect Injection
## 3.2 Tool Security
## 3.3 Least Privilege

# 4. 成本工程
## 4.1 Token Cost
- Prompt压缩、Context过滤
## 4.2 Model Routing
- 不同任务使用不同模型
## 4.3 KV Cache
稳定 Prompt 前缀
## 4.4 Tool Cost Control

# 5. py基础
## 5.1 f-string
- Python 会在创建字符串时，把变量值填进去。f-string 就是“格式化字符串”，允许在字符串中用 {表达式} 插入变量。

# 6. langchain基础
## 6.1 agent.stream()函数
- stream_mode="messages" 下，每次返回一个二元组：(AIMessageChunk, metadata字典)
- chunk 序列化后的大致结构
{
<!-- 当前流式返回的文字片段； -->
  "content": "论文",
  "additional_kwargs": {},
  <!-- 模型 Provider 返回的信息 -->
  "response_metadata": {},
  "type": "AIMessageChunk",
  "name": null,
  "id": "run-xxx",
  "tool_calls": [],
  "invalid_tool_calls": [],
  <!-- Token 使用量，通常不一定每个 chunk 都有 -->
  "usage_metadata": null,
  <!-- 工具调用参数片段 -->
  "tool_call_chunks": [],
  <!-- 最后一个分块时可能是 "last" -->
  "chunk_position": null
}
- metadata 大致结构
- {
  "langgraph_step": 1,
  "langgraph_node": "model",
  "langgraph_triggers": ["branch:to:model"],
  "langgraph_path": ["__pregel_pull", "model"],
  "langgraph_checkpoint_ns": "model:xxx",
  "checkpoint_ns": "model:xxx"
}
- 不同 LangChain、LangGraph 版本和 Agent 结构，字段可能不同。最常用的是：metadata["langgraph_node"]
它表示这个 chunk 来自哪个节点，例如 model。
