1. 相关概念
- context window:
- q:
上下文窗口有限，
发送太多会影响模型判断，
输入多成本高，


# context
- 保存context
- 选择
1. 静态：Agent.md,Systemprompt。开发规则，配置信息，遵循的一些规则
2. 动态：skills，tools，每次运行时按需选择
- 压缩context
context = 读取的fils，写入的文件内容，模型思考内容，prompt，历史输入输出...
最占空间的data：模型输出文本，tools执行结果

- 隔离context
用于Multi-Agent


