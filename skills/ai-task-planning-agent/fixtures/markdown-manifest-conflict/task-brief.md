# 任务简报

## 目标

为下游 coding agent 创建一个 `Task Execution Pack`。

## 非目标

- 不执行用户业务代码。
- 不连接生产环境。
- 不替代 Jira 或 Linear。

## 已知事实

- Agent 会为下游 coding agent 创建 `Task Execution Pack` artifacts。
- 机器可读 JSON 文件是事实源。
- Agent 不得执行用户业务代码。

MANIFEST_CONFLICT: 本文件声称 Markdown 是事实源，这与 manifest 中“机器可读 JSON 文件是事实源”的已知事实冲突。

## 成功标准

- 必需 JSON 文件存在。
- Blocking questions 为空，或已被结构化 waiver 覆盖。
- Recovery paths 和 trace requirements 非空。
