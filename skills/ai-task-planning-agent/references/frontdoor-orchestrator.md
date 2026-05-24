# Frontdoor / Orchestrator

## 职责

识别请求类型、模式、目标下游 AI、当前状态、下一状态和恢复动作。

## 输入

- 用户请求
- 已存在的 task pack，如果有
- 对话摘要
- 校验结果

## 输出

- 请求类型
- 模式：light、standard 或 deep
- 当前状态
- 下一状态
- 恢复动作
- Manifest 更新项

## 硬失败

- 把 coding-agent task 错误路由成通用 PRD task。
- Evaluator 已失败，但 pack 仍被标记为 delivery-ready。
- 缺少 `package-manifest.json`，且没有记录 light-mode exception。
