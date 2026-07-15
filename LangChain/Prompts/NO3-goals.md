N03：Prompt Engineering 与 Context Engineering
节点目标

不仅学习“怎么写提示词”，还要学习应用在运行时如何选择、组织和控制上下文。

需要掌握：

System、User 和示例的职责；
目标、约束、边界和成功标准；
Zero-shot 与 Few-shot；
- 组装messages
正例、反例和边界示例；
Prompt 模板和版本管理；
--------------------------------------------------
上下文选择、排序和压缩；
Token 预算；
历史会话管理；
长上下文位置偏差；
上下文冲突与污染；
Prompt Injection 基础；
Prompt A/B 测试与回归测试；
Prompt 缓存。
任务系统

你需要能把 Prompt 从“自然语言要求”升级成完整任务规范：

角色
目标
输入说明
执行规则
禁止行为
证据要求
输出结构
失败处理
质量标准

同时能够设计 Context Builder，决定：

哪些历史消息保留；
哪些论文片段进入上下文；
哪些用户笔记优先；
超过 Token 上限时如何压缩；
不可信论文文本如何隔离。
课程

主课 A 中的提示词工程章节；主课 B 中的 Prompt 和 RAG 前置部分。

理论补充可以参考李宏毅关于 Context Engineering 的相关讲解入口，但最终实现以你的项目实验为准。

验收系统

理解题覆盖：

Prompt 组成；
Few-shot；
上下文预算；
长上下文问题；
Prompt 与 Context 的区别。

面试题覆盖：

Prompt 版本治理；
上下文装配器；
Prompt Injection；
A/B 测试；
Prompt 缓存与成本。

综合实践 1：论文总结 Prompt 基准

准备 15 篇不同类型论文，对比三套 Prompt：

简单 Prompt；
结构化任务 Prompt；
带 Few-shot 和检查规则的 Prompt。

评价：

完整性；
事实准确；
格式稳定；
局限识别；
术语解释质量。

综合实践 2：Context Builder

输入：

系统指令
对话历史
论文证据
个人笔记
当前问题
Token 上限

输出最终模型上下文，并记录每段内容为何被保留或删除。

组会助手接入

增加：

固定论文综述标准；
不同类型论文模板；
术语解释；
证据不足标记；
Prompt 版本记录。

项目版本：V0.2 标准论文阅读报告