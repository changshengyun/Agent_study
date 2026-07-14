1. langchain中，发送给模型的消息和返回的消息都统一封装为BaseMessage，
并且准备了多个BaseMessage的子类对应不同角色类型的消息
消息的类型，大概四种：
role:system   SystemMessage
role:user     HumanMessage
role:assistant  AIMessage
role:tool     ToolMessage

2. 多模态消息
(1)找支持该多模态消息的model
(2)根据官网格式，构造message