# Agile 计划

## Product Goal

帮助 AI Agent builder 生成经过校验的执行包，让下游 coding agent 不必重新澄清核心需求即可开始执行。

## Backlog

- 定义任务边界。
- 创建执行契约。
- 打包 artifacts。
- 运行 release gate evaluation。

## Definition of Ready

- 目标、非目标、目标下游 AI 和成功标准已存在。

## Definition of Done

- Evaluator 对该 pack 返回 `pass`。
- Negative fixtures 按预期 block release。

## Review and Retro

审阅 evaluator output，并为新发现的 hard failures 增加 regression fixtures。
