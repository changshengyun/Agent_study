1.为什么要分别创建model和agent？

-模型对象负责和大模型 API 通信、生成回答、决定是否调用工具；
-智能体对象负责维护消息状态、执行工具、把工具结果交回模型，并循环运行直到任务完成。
-LangChain 官方把模型称为 Agent 的“推理引擎”，而 create_agent() 创建的是围绕模型运行的 Agent harness，也就是模型之外的工具循环、提示词、状态、记忆和中间件等执行结构。

2.model和之前api调用中的客户端client的区别
LangChain model：
≈ API 客户端
+ 具体模型配置
+ LangChain 适配层

3.client，model，agent这三者的区别？
底层 SDK Client
负责连接 API、认证和发送 HTTP 请求
        ↓
LangChain Model
封装 SDK Client，并绑定模型名称、模型参数和消息格式
        ↓
LangChain Agent
使用 Model 进行推理，并负责工具执行、状态维护和循环控制