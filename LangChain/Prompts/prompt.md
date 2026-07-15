1. System Prompts
设定模型的角色和聊天背景
2. System Prompts添加方法
(1)message里添加SystemMessage()
{'messages' = [
        SystemMessage(),
        HumanMessage(),]}
(2)agent/model里添加system_prompt参数
system_prompt = " input your prompts "
3. System Prompts includes：
identity：         描述ai职责、沟通风格和总体目标
instructions：     知道模型如何生成所需的响应。do/not do
ex--improtant：    提供可能的输入实例，以及模型期望的输出
context（背景信息）：Rag、Data

- 推荐用.md格式
- xml标签可以帮助明确区分一段内容
- json
（1）json对象,dict
{
    "name":"Tim",
}
(2)json数组，dict_list
[
    {...},
    {...},
    ...
]
(3)
json.dumps(),py->json
json.loads(),json->py

-设置角色和指令
system_prompt = """
# 身份
- 你是一个论文阅读助手，帮助用户阅读英文论文。
# 指令
- 请用markdown格式分点输出
# 实例
user：总结下他的摘要部分
assistant：...
"""

4. 结构化输出
（1）提供结构化示例
（2）定义一个类，在agent的response_format参数设置结构化输出格式
response_format = 类名

5. Prompt Engineering
是通过优化prompt使model的output更符合业务需求的‘过程’。
：编写、优化的一个过程。

6. Zero-shot

7. Few-shot
8. Prompt 版本管理
Prompt 不是写完一次就结束，而应像代码一样维护版本。
每次修改要记录：

修改了什么；
为什么修改；
使用哪个模型；
在哪些测试论文上效果更好；
是否导致旧任务退化。
OpenAI 和 Anthropic 的提示工程文档都把 Prompt 设计视为一个需要反复测试和迭代的过程，而不是一次性措辞工作。

9. 目标、约束、边界和成功标准，这四个概念需要分清
- 目标：最终要完成什么。
ex:生成一份结构化论文阅读报告。

- 约束：执行过程中必须遵守什么。
ex:只能使用提供的论文内容；
总字数不超过 2000 字。

- 边界（在执行过程中不需要做什么）：哪些事情不在模型责任范围内。
ex:不能判断未提供的实验数据；
不能声称论文结论已经被后续研究证实。

- 成功标准：怎样判断输出合格。
研究问题、方法、实验、结果、局限五部分完整；
所有主要结论能够对应原文证据。
 - 正例
告诉模型什么样的输出符合要求。

 - 反例
告诉模型哪些常见输出是不合格的。

- 边界示例
告诉模型遇到信息不足或模糊情况时怎么处理。

- Prompt A/B 测试
在模型、输入数据和参数尽量相同的情况下，对比两个 Prompt 的实际效果。
-- 评估指标：
完整性；
事实准确率；
输出格式稳定性；
是否识别局限；
Token 消耗；
响应时间。

- Prompt 回归测试
回归测试解决的是：
修改 Prompt 后，新版本会不会修好一个问题，却破坏原来正常的能力。

例如，V2 增加“必须简洁”后：输出长度减少了；但论文方法细节也被删掉了。

因此需要维护固定测试集：
5 篇方法型论文
5 篇综述论文
3 篇实验型论文
2 篇证据不完整论文

每次修改 Prompt，都重新运行测试。