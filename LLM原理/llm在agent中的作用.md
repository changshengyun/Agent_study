# Agent 认知文档：LLM 与 Transformer 的工程化理解

> 学习主题：LLM、Transformer、模型 API、推理性能、幻觉、模型边界，以及 LLM 在 Agent 系统中的位置
> 当前状态：LLM 整体流程基本掌握，Transformer 内部机制与推理工程正在巩固

---

## 1. 本阶段学习目标

本阶段不是以“大模型算法研究员”为目标，不要求从零训练大模型，也不要求完整推导 Transformer 的数学公式。

学习目标是建立面向 **Agent 工程开发** 的 LLM 认知：

1. 理解 LLM 从文本输入到文本输出的完整流程；
2. 理解 Transformer 内部主要模块分别负责什么；
3. 理解模型 API 参数作用于生成流程的哪个阶段；
4. 理解上下文长度、输出长度、KV Cache 与推理性能的关系；
5. 理解模型为什么会产生幻觉；
6. 理解模型能力边界的工程意义；
7. 明确 LLM、Agent Runtime、Tools、Memory 和 Validator 的职责边界。

---

# 2. 基础术语校正

## 2.1 LLM 与 Llama

需要区分两个概念：

* **LLM**：Large Language Model，大语言模型，是一类模型；
* **Llama**：Meta 推出的一个具体大语言模型家族。

关系类似：

```text
LLM
├── GPT
├── Claude
├── Gemini
├── Qwen
├── DeepSeek
└── Llama
```

本知识文档讨论的是 **LLM 与 Transformer 的通用工程机制**，而不只针对 Llama。

---

# 3. LLM 应用体系的七层结构

## 3.1 基础模型层

这一层提供不同类型的模型能力。

| 模型类型                   | 主要作用          |
| ---------------------- | ------------- |
| LLM                    | 文本理解、生成、推理和规划 |
| VLM                    | 图像与文本联合理解     |
| Embedding Model        | 将文本或图片转换为语义向量 |
| Reranker               | 对检索结果重新排序     |
| ASR Model              | 语音转文字         |
| TTS Model              | 文字转语音         |
| Image Generation Model | 文本生成图片        |

需要特别区分：

```text
LLM 内部的 Token Embedding
≠
用于 RAG 的独立 Embedding Model
```

---

## 3.2 模型训练、对齐与适配层

这一层负责形成或修改模型参数。

主要包括：

1. 数据采集；
2. 数据清洗、去重和标注；
3. 预训练 Pre-training；
4. 监督式指令微调 SFT；
5. 偏好对齐，例如 RLHF、DPO；
6. 领域 Fine-tuning；
7. LoRA 等参数高效微调；
8. 模型评测。

需要注意：

> Fine-tuning 是一个上位概念，SFT、领域微调和 LoRA 都可以属于 Fine-tuning。

---

## 3.3 模型调用与推理层

这一层负责把模型能力提供给应用程序。

主要内容包括：

* API 调用；
* Token 与 Tokenizer；
* Context Window；
* Sampling；
* Temperature；
* Top-p、Top-k；
* Structured Output；
* Streaming；
* Token 成本；
* 延迟；
* Rate Limit。

---

## 3.4 上下文增强层

这一层通常不修改模型参数，而是改善模型当前获得的信息条件。

包括：

* Prompt Engineering；
* Context Engineering；
* RAG；
* Memory；
* 对话历史管理；
* 上下文压缩；
* 工具结果管理。

### Prompt Engineering

关注：

> 当前任务指令应该怎么写。

例如：

* 任务目标；
* 角色；
* 输出格式；
* 限制条件；
* 示例；
* 验收标准。

### Context Engineering

关注：

> 在有限的 Context Window 中，模型当前应该看到什么信息。

它的范围更大：

```text
Context Engineering
├── Prompt Engineering
├── 对话历史
├── RAG 检索结果
├── Memory
├── 工具描述
├── 工具返回结果
├── 当前任务状态
└── 上下文压缩
```

---

## 3.5 工具与执行层

这一层负责让系统读取或改变外部环境。

包括：

* Function Calling；
* MCP；
* 外部 API；
* 数据库；
* 文件系统；
* 浏览器；
* 代码执行。

需要明确：

```text
LLM 生成工具调用请求
≠
工具已经执行
```

完整流程是：

```text
LLM 提出工具名和参数
→ Agent Runtime 解析
→ 参数校验
→ 权限校验
→ 工具真实执行
→ 返回执行结果
→ 再交给 LLM 分析
```

---

## 3.6 Agent 控制与编排层

这一层不只是“多 Agent”，单 Agent 也需要。

包括：

* Planning；
* Routing；
* State Management；
* Agent Loop；
* Retry；
* Timeout；
* Error Recovery；
* Termination Condition；
* Human-in-the-loop；
* Multi-Agent Coordination。

Agent 的基本闭环是：

```text
目标
→ 观察当前状态
→ 选择动作
→ 执行动作
→ 获取反馈
→ 更新状态
→ 判断是否完成
```

---

## 3.7 工程治理层

这一层负责系统的安全性、可靠性和可验证性。

包括：

* 权限控制；
* 日志与审计；
* 安全策略；
* 并发控制；
* 成本控制；
* 监控；
* 评测；
* 结果验证；
* 故障恢复；
* 数据一致性。

---

# 4. LLM 从输入到输出的完整流程

完整链路如下：

```text
原始文本
↓
Tokenizer
↓
Token
↓
Token ID
↓
查询 Embedding Matrix
↓
Token Embedding
+ 位置信息
↓
多层 Transformer
↓
Hidden State
↓
LM Head
↓
整个词表的 Logits
↓
Temperature 等参数调整
↓
Softmax 概率分布
↓
Top-k / Top-p 等采样
↓
选择下一个 Token ID
↓
追加到已有序列
↓
重复自回归生成
↓
满足停止条件
↓
Detokenization
↓
输出文本
```

---

# 5. Token、Token ID 与 Embedding

## 5.1 Token

Token 是 Tokenizer 根据词表和编码规则，对文本切分后得到的离散单位。

Token 不一定等于一个完整单词，它可能是：

* 一个汉字；
* 多个汉字；
* 一个英文单词；
* 英文单词的一部分；
* 标点；
* 空格与单词的组合；
* 特殊控制符号。

---

## 5.2 Token ID

每个 Token 在模型词表中都有一个整数编号。

例如：

```text
"我"      → 105
"喜欢"    → 872
"Agent"   → 31025
```

模型不能直接计算字符串，因此需要先转换为 Token ID。

Token ID 的本质是：

> Token 在词表中的整数索引。

---

## 5.3 Token Embedding

模型内部存在一个 Embedding Matrix。

Token ID 用于查询这个矩阵中的某一行：

```text
Token ID
→ 查询 Embedding Matrix
→ 得到 Token Embedding
```

Token Embedding 是 Transformer 可以进行矩阵运算的向量表示。

需要区分：

```text
Token Embedding：
单个 Token 在 LLM 内部的隐藏向量

Embedding Model：
将一段完整文本转换为用于检索的语义向量
```

---

# 6. Context Window 与 Memory

## 6.1 Context Window

Context Window 是模型一次请求能够处理的输入和输出 Token 总容量。

其中可能包括：

```text
System Prompt
+ 用户输入
+ 历史消息
+ RAG 内容
+ Memory 检索结果
+ 工具定义
+ 工具返回结果
+ 模型输出
```

Context Window 不是永久存储系统。

---

## 6.2 Memory

LLM 通常是无状态的，不会天然记住上一轮对话。

真正的过程是：

```text
应用保存历史信息
→ 下一次请求时选取部分信息
→ 重新放入 Context Window
→ 模型重新读取
```

因此：

```text
Context Window = 当前工作台
Memory / Database = 外部仓库
```

Agent 的 Memory 不只是保存历史，还包括：

* 写入什么；
* 什么时候写入；
* 如何压缩；
* 如何检索；
* 如何处理冲突；
* 什么时候遗忘。

---

# 7. Transformer 内部工作机制

现代 GPT、Llama 等通常采用 Decoder-only Transformer。

一个 Transformer Block 可以简化为：

```text
输入 Hidden State
→ Norm
→ Causal Self-Attention
→ Residual Connection
→ Norm
→ MLP
→ Residual Connection
→ 下一层
```

---

## 7.1 Self-Attention

Self-Attention 的作用是：

> 让当前 Token 根据任务需要，从其他 Token 中动态读取相关信息。

模型会将输入映射成：

```text
Q：Query
K：Key
V：Value
```

可以用工程直觉理解：

* **Query**：当前 Token 想寻找什么信息；
* **Key**：其他 Token 用什么特征说明自己可能相关；
* **Value**：如果被关注，它实际提供什么信息。

例如：

```text
小红把书给了小明，因为她已经看完了。
```

在处理“她”时，模型会计算“她”与“小红”“小明”“书”等 Token 的相关性，然后将相关 Token 的信息聚合进“她”的新表示。

需要注意：

> Attention 是一种上下文信息聚合机制，不等于人类理解，也不能保证事实正确。

---

## 7.2 Causal Mask

自回归模型预测当前位置时，不能看到未来 Token。

例如预测：

```text
今天天气很____
```

模型不能提前看到正确答案“好”。

Causal Mask 保证：

```text
第 i 个位置
只能关注自己和前面的 Token
不能关注未来 Token
```

这也是为什么：

* 训练时可以并行计算多个位置；
* 推理时通常必须逐 Token 串行生成。

---

## 7.3 位置信息与 RoPE

Attention 本身不能天然理解顺序。

例如：

```text
狗咬人
人咬狗
```

Token 类似，但含义完全不同。

因此模型需要加入位置信息。

现代 Llama 类模型常使用 RoPE。工程层面需要理解：

1. 它帮助 Attention 感知 Token 的位置和相对距离；
2. 长上下文能力与位置编码有关；
3. 支持更长 Context Window，不代表所有位置的信息都能被同样可靠地使用。

---

## 7.4 Multi-Head Attention

单个 Attention Head 只在一套投影空间中计算关系。

Multi-Head Attention 允许模型同时从多种关系维度处理上下文，例如：

* 局部语法；
* 长距离指代；
* 结构边界；
* 代码依赖；
* 主题关系。

不同 Head 的具体功能通常不是完全固定、可直接解释的。

---

## 7.5 MLP

Transformer Block 不只有 Attention。

可以建立以下工程直觉：

```text
Attention：
负责不同 Token 之间的信息交换

MLP：
负责对每个位置得到的信息进行非线性加工
```

知识和能力并不只存储在某个单独模块中，而是分布在整个网络参数及其交互过程中。

---

## 7.6 Residual 与 Norm

### Residual Connection

概念上：

```text
输出 = 原输入 + 子层计算结果
```

作用包括：

* 保留原始信息；
* 改善梯度传播；
* 让深层网络更容易训练；
* 允许每层学习增量修正。

### LayerNorm / RMSNorm

用于稳定隐藏状态的数值尺度。

Llama 类模型通常使用 RMSNorm。

---

## 7.7 Hidden State、LM Head 与 Logits

需要严格区分：

| 概念              | 作用                     |
| --------------- | ---------------------- |
| Token Embedding | Transformer 输入前的初始向量   |
| Hidden State    | Transformer 处理后的上下文表示  |
| LM Head         | 将 Hidden State 映射到词表维度 |
| Logits          | 每个候选 Token 的原始分数       |

完整过程：

```text
最后一个位置的 Hidden State
→ LM Head
→ 整个词表的 Logits
→ Softmax
→ 概率分布
```

---

# 8. 自回归生成

模型通常一次只选择一个新 Token。

原因是后一个 Token 的概率依赖前面实际生成了什么。

例如：

```text
输入：人工智能正在

第 1 次预测：改变
第 2 次预测：世界
第 3 次预测：。
```

完整循环：

```text
已有 Token 序列
→ 预测下一个 Token
→ 选择 Token
→ 加入序列
→ 再次预测
```

这就是自回归生成。

---

# 9. API 参数在生成流程中的作用

## 9.1 `model`

决定：

* 使用哪个模型；
* Tokenizer；
* 参数规模；
* Context Window；
* 工具能力；
* 多模态能力；
* 速度；
* 成本。

---

## 9.2 `messages`、`system`

消息通常先经过 Chat Template，转换为模型能识别的特殊 Token 序列。

System Prompt 的作用是：

* 规定角色；
* 设定行为原则；
* 设定输出要求；
* 约束工具使用。

但 System Prompt 不是绝对安全边界，模型仍可能忽略或误解。

---

## 9.3 `max_output_tokens`

控制最大输出 Token 数量。

作用：

* 控制成本；
* 控制最大延迟；
* 防止输出无限增长。

如果达到上限，回答可能被截断。

---

## 9.4 `temperature`

Temperature 调整概率分布的尖锐程度。

低 Temperature：

* 高概率 Token 更突出；
* 输出通常更稳定；
* 随机性更低。

高 Temperature：

* 概率分布更平坦；
* 低概率 Token 更容易被选中；
* 输出更多样。

需要注意：

```text
低 Temperature
≠
事实一定正确
```

模型可能稳定地输出一个错误答案。

---

## 9.5 `top_p`

Top-p 使用累计概率选择候选集合。

例如：

```text
A：0.45
B：0.30
C：0.15
D：0.07
```

当 `top_p = 0.8` 时：

```text
A + B = 0.75
A + B + C = 0.90
```

候选集合是 A、B、C，然后再从中采样。

Top-p 不是“单个 Token 概率必须超过 80%”。

---

## 9.6 `top_k`

Top-k 只保留概率最高的前 k 个候选 Token。

区别：

| 参数    | 机制              |
| ----- | --------------- |
| Top-k | 固定候选数量          |
| Top-p | 固定累计概率，候选数量动态变化 |

---

## 9.7 `stop`

控制生成终止条件。

常见停止原因：

* EOS Token；
* 最大输出长度；
* Stop Sequence；
* 工具调用；
* 请求超时；
* 用户取消。

---

## 9.8 `stream`

`stream=true` 不改变模型的生成机制，只改变返回方式。

```text
非流式：
全部生成完后一次返回

流式：
生成一部分就立即返回一部分
```

流式可以降低用户感知到的首字延迟，但不会显著减少总计算量。

---

## 9.9 Structured Output

Structured Output 要求模型按固定结构输出，例如 JSON Schema。

它能提高：

* 可解析性；
* 字段完整性；
* 类型稳定性。

但不能保证：

* 内容真实；
* 参数合理；
* 事实正确；
* 任务已经完成。

```text
结构正确
≠
语义正确
≠
事实正确
```

---

## 9.10 `tools` 与 Function Calling

工具 Schema 会被放入模型上下文。

模型根据上下文生成：

```json
{
  "name": "search_paper",
  "arguments": {
    "query": "Agent memory"
  }
}
```

但模型只是在提出动作请求。

真正执行者是：

```text
Agent Runtime
+ Tool Executor
```

---

## 9.11 Runtime 参数

以下参数通常不属于 Transformer：

* Timeout；
* Retry；
* 并发；
* Rate Limit；
* 连接池；
* 请求队列；
* 熔断；
* 失败降级。

这些属于应用程序和 Agent Runtime。

---

# 10. 推理工程与性能机制

## 10.1 Prefill

Prefill 一次性处理全部输入上下文：

* System Prompt；
* 用户输入；
* 历史对话；
* RAG 内容；
* 工具定义；
* 工具结果。

长输入主要增加：

* TTFT；
* 输入 Token 成本；
* 显存占用；
* Attention 计算量。

---

## 10.2 Decode

Decode 逐 Token 生成输出。

每生成一个新 Token，都需要经过全部 Transformer 层。

长输出主要增加：

* 总响应时间；
* 输出费用；
* 后续上下文长度。

---

## 10.3 KV Cache

历史 Token 的 Key 和 Value 会被保存。

下一轮生成时：

```text
逻辑上：
新 Token 仍然依赖全部历史

计算上：
不需要重新计算全部历史 K/V
```

KV Cache 可以加快 Decode，但会占用显存。

KV Cache 随以下因素增长：

* Context 长度；
* 并发请求数；
* 模型层数；
* KV Head 数量；
* 数值精度。

---

## 10.4 性能指标

| 指标                  | 含义                    |
| ------------------- | --------------------- |
| TTFT                | 从发送请求到收到第一个 Token 的时间 |
| TPS                 | 每秒生成多少 Token          |
| Inter-token Latency | 相邻输出 Token 的时间间隔      |
| Total Latency       | 完整回答生成完所需时间           |

Agent 总延迟还包括：

```text
模型调用
+ 工具调用
+ 网络
+ 重试
+ 多轮 Agent Loop
```

---

## 10.5 Agent 中的上下文膨胀

Agent 在运行过程中会不断增加：

* 计划；
* 工具参数；
* 工具结果；
* 错误日志；
* 重试记录；
* RAG 资料；
* 中间结论。

如果全部塞入 Context：

* Prefill 变慢；
* 成本上升；
* KV Cache 变大；
* 重要信息被噪声淹没；
* 模型更容易混淆。

因此 Context Engineering 的目标是：

> 提供完成当前决策所需的最小充分信息，而不是尽量塞满上下文。

---

# 11. 幻觉

## 11.1 幻觉是什么

幻觉是指：

> 模型生成了语言上合理、结构完整，但事实、逻辑或执行状态错误的内容。

根本原因是模型主要优化：

```text
生成上下文中概率较高的 Token
```

而用户真正需要的是：

```text
输出是否符合现实事实
```

两者不是同一个目标。

---

## 11.2 幻觉的类型

### 知识幻觉

* 编造论文；
* 编造 API；
* 记错日期；
* 混淆人物和事件。

### 上下文幻觉

资料已经提供，但模型：

* 忽略关键内容；
* 错读数字；
* 混淆多个文档；
* 使用了错误片段。

### 推理幻觉

事实正确，但推理过程或结论错误。

### 检索幻觉

RAG 检索到：

* 错误资料；
* 过期资料；
* 不相关片段；
* 缺失上下文的片段。

### 工具幻觉

模型可能：

* 调用不存在的工具；
* 生成错误参数；
* 错误理解工具结果；
* 声称工具已执行。

### 行动幻觉

模型说：

```text
文件已经保存。
```

但实际上文件没有创建，或者创建失败。

---

## 11.3 Temperature 不能消灭幻觉

低 Temperature 只能降低采样随机性。

假设模型认为：

```text
错误答案：80%
正确答案：15%
不知道：5%
```

降低 Temperature 后，模型会更稳定地选择错误答案。

因此：

```text
低 Temperature
= 更稳定

低 Temperature
≠ 更真实
```

---

## 11.4 RAG 不能消灭幻觉

RAG 链路中仍可能发生：

```text
查询理解错误
→ 检索错误
→ 排序错误
→ 文档切片错误
→ 上下文构建错误
→ 模型解释错误
```

RAG 的准确定位是：

> 为模型提供外部证据，降低只依赖模型参数知识回答的风险。

---

# 12. 为什么要引入“模型边界”

模型边界不是 Transformer 中的一个技术模块，而是：

> 用来划分 LLM 在系统中的责任范围。

它主要解决三个工程问题：

```text
系统设计
风险控制
故障定位
```

---

## 12.1 系统设计

模型边界帮助判断：

* 哪些任务可以直接交给 LLM；
* 哪些任务需要搜索；
* 哪些任务需要数据库；
* 哪些任务需要工具；
* 哪些任务必须人工审批。

---

## 12.2 风险控制

LLM 是概率性组件，可能：

* 误解用户意图；
* 生成错误工具参数；
* 误判任务完成；
* 受到 Prompt Injection；
* 执行危险动作。

因此不能让 LLM 拥有无限权限。

---

## 12.3 故障定位

当结果错误时，需要区分：

* 模型知识错误；
* Prompt 错误；
* Context 错误；
* RAG 错误；
* 工具错误；
* Runtime 错误；
* 验证机制缺失。

不能遇到问题就简单归结为：

```text
模型不够聪明，换一个更大模型。
```

---

# 13. 模型能力边界的六种类型

## 13.1 知识边界

模型知识可能：

* 不完整；
* 过时；
* 错误；
* 被不同信息混合。

需要搜索、数据库、RAG 或官方资料补充。

---

## 13.2 上下文边界

模型只能使用当前 Context 中看到的信息。

即使模型支持长上下文，也可能：

* 忽略中间信息；
* 混淆多个来源；
* 被噪声干扰；
* 遗漏关键约束。

---

## 13.3 观察边界

模型不能直接观察真实环境。

它不知道：

* 文件是否存在；
* 数据库当前状态；
* 邮件是否送达；
* 服务是否启动；
* 代码是否运行成功。

必须由工具读取真实状态，再返回给模型。

---

## 13.4 行动边界

LLM 的输出本质上只是 Token。

```text
模型输出“删除文件”
≠
文件已经删除
```

真实动作必须由 Runtime 和 Tool 执行。

---

## 13.5 记忆边界

LLM 通常没有天然、可靠的永久记忆。

长期状态需要：

* 数据库；
* Memory Store；
* 文件；
* 缓存；
* 向量库；
* State Store。

---

## 13.6 自我验证边界

模型可以检查自己的回答，但不能仅凭自我评价证明正确。

例如：

```text
模型说代码正确
≠
代码已经编译和测试通过
```

真实验证需要：

* 单元测试；
* 代码执行；
* 数据库回查；
* API 状态查询；
* 规则验证；
* 人工审核。

---

# 14. LLM 与 Agent 的关系

LLM 不是完整 Agent。

可以抽象为：

```text
Agent
=
LLM
+ Context
+ State
+ Memory
+ Tools
+ Runtime
+ Control Loop
+ Guardrails
+ Validator
```

LLM 主要负责：

* 理解目标；
* 生成内容；
* 生成计划；
* 选择候选动作；
* 分析工具结果；
* 提出下一步建议。

Agent Runtime 负责：

* 构建上下文；
* 维护状态；
* 控制循环；
* 解析工具调用；
* 权限校验；
* 重试和超时；
* 终止任务；
* 错误恢复。

Tools 负责：

* 真实读取环境；
* 改变外部状态。

Validator 负责：

* 判断动作是否执行成功；
* 判断用户目标是否真正完成。

---

# 15. 核心工程原则

## 15.1 概率性与确定性分工

```text
LLM 负责开放性认知
代码负责确定性控制
工具负责真实执行
验证器负责证明结果
```

---

## 15.2 三个不能画等号的关系

```text
LLM 输出工具调用
≠
工具已经执行
```

```text
工具返回成功
≠
外部状态一定正确
```

```text
外部状态改变
≠
用户目标一定完成
```

---

## 15.3 Structured Output 的边界

```text
JSON 正确
≠
事实正确
≠
业务正确
≠
执行成功
```

Structured Output 主要解决“程序能不能解析”，而不是“内容是否可信”。

---

# 16. 当前认知盲区

## 盲区一：容易混淆不同层级

需要继续严格区分：

* 模型训练；
* 模型推理；
* Prompt；
* RAG；
* Tool Calling；
* Runtime；
* Agent 编排；
* 工程治理。

---

## 盲区二：容易把模型提出动作理解成模型执行动作

模型只生成动作建议。

真正执行必须经过：

```text
解析
→ 校验
→ 权限判断
→ 工具执行
→ 状态回查
```

---

## 盲区三：容易把流畅性理解成正确性

模型可以生成非常专业、完整、确定的错误答案。

必须分别评价：

* 语言质量；
* 事实质量；
* 推理质量；
* 执行质量；
* 任务完成质量。

---

# 17. 关键补充认识

## 17.1 LLM 可以看成一种 Policy

在 Agent 中，可以将 LLM 理解为：

```text
当前状态
→ LLM / Policy
→ 候选动作
```

它更像一个概率性策略组件，而不是拥有绝对控制权的“大脑”。

---

## 17.2 Agent 的核心是显式状态

没有状态管理，Agent 容易：

* 重复执行；
* 忘记已完成步骤；
* 丢失工具结果；
* 无法恢复错误；
* 无法判断任务结束。

---

## 17.3 模型能力边界不是固定清单

边界取决于：

```text
模型能力
+ 当前上下文
+ 工具条件
+ 任务风险
+ 验证机制
```

同一个任务，在不同系统条件下，可靠程度不同。

---

# 18. 当前掌握状态

| 知识模块                    | 当前状态   |
| ----------------------- | ------ |
| LLM 与 Llama 区分          | 已掌握    |
| LLM 应用分层                | 基本掌握   |
| Token 生成流程              | 基本掌握   |
| Context 与 Memory 区别     | 基本掌握   |
| API 参数作用                | 正在巩固   |
| Transformer Block       | 正在学习   |
| Prefill、Decode、KV Cache | 初步理解   |
| 幻觉机制                    | 初步理解   |
| 模型能力边界                  | 基本形成框架 |
| LLM 与 Agent 责任边界        | 基本掌握   |

当前节点建议标记为：

```text
🟡 LLM 与 Transformer 工程化理解：基本合格，等待费曼验收
```

---

# 19. 费曼自测题

回答时不要直接复制文档内容，必须使用自己的语言，并尽量举例。

## 第一组：基础流程

### 1. Token、Token ID 和 Token Embedding 分别是什么？

要求说明：

* 三者如何转换；
* 模型为什么不能直接处理文本字符串；
* Token Embedding 与独立 Embedding Model 的区别。

### 2. 完整解释一次 LLM 从用户输入到输出文本的过程。

必须包含：

```text
Tokenizer
Token ID
Embedding
Transformer
Hidden State
LM Head
Logits
Softmax
Sampling
自回归
Detokenization
```

### 3. 为什么 LLM 推理时通常要逐 Token 生成，而训练时可以并行处理多个位置？

---

## 第二组：Transformer

### 4. 用“小红、小明和她”的例子解释 Q、K、V 和 Self-Attention。

要求回答：

* Query 在寻找什么；
* Key 的作用是什么；
* Value 提供什么；
* Attention 最终怎样改变当前 Token 的 Hidden State。

### 5. Causal Mask 为什么是自回归模型必须存在的机制？

### 6. Attention 和 MLP 在 Transformer Block 中分别负责什么？

---

## 第三组：API 参数

### 7. Temperature 和 Top-p 有什么区别？

进一步回答：

* 为什么 Temperature 低不代表答案一定正确？
* 为什么 Top-p 不是“概率超过某个阈值的 Token 才能选择”？

### 8. Structured Output 能保证什么，不能保证什么？

请分析以下输出：

```json
{
  "email_sent": true
}
```

为什么 JSON 合法仍然不能证明邮件已经发送？

### 9. `stream=true` 改变了模型内部的生成机制吗？它主要改变什么体验？

---

## 第四组：推理性能

### 10. Prefill 和 Decode 分别处理什么？

要求说明：

* 长输入主要影响哪个阶段；
* 长输出主要影响哪个阶段；
* TTFT 和总延迟分别受什么影响。

### 11. KV Cache 保存了什么？为什么它能加快生成？为什么它又会占用大量显存？

---

## 第五组：幻觉与模型边界

### 12. 为什么模型可以生成语言非常专业、但事实完全错误的答案？

### 13. 为什么即使设置 `temperature = 0`，模型仍然可能产生幻觉？

### 14. 为什么 RAG 不能彻底消除幻觉？

至少列出三个可能出错的环节。

### 15. 什么是模型边界？为什么 Agent 开发必须引入这个概念？

要求从三个方面回答：

```text
系统设计
风险控制
故障定位
```

### 16. 模型的知识边界、观察边界、行动边界和验证边界分别是什么？

每一种边界至少举一个例子。

---

## 第六组：Agent 工程场景

### 17. 用户要求：“找到三篇最新的 Agent 论文，总结后发给导师。”

请把任务拆给以下组件：

* LLM；
* 搜索工具；
* Agent Runtime；
* 邮件工具；
* Validator；
* 用户审批。

### 18. 为什么下面三个表达不能画等号？

```text
模型说完成
工具执行成功
用户目标完成
```

### 19. 一个 Agent 不断重复调用同一个工具，可能是哪一层的问题？

至少从以下角度分析：

* LLM；
* Prompt；
* State；
* Runtime；
* Termination Condition；
* Tool Result。

### 20. 用一句话解释可靠 Agent 的核心工程原则。

参考方向：

```text
LLM 负责什么
代码负责什么
工具负责什么
验证器负责什么
```

---

# 20. 费曼验收标准

完成自测时，不以术语数量为判断标准，而以以下能力为标准：

1. 能够使用自己的语言解释；
2. 能够举出真实例子；
3. 能够区分相近概念；
4. 能够说明适用范围和边界；
5. 能够解释错误发生在哪一层；
6. 能够把底层机制映射到 Agent 工程问题。

当以上问题能够独立回答，并且关键概念没有明显混淆时，可以将该节点标记为：

```text
🟢 LLM 与 Transformer 工程化理解：已掌握
```
