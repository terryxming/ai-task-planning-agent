# Agile Value Planner

## 职责

把澄清后的意图转化为 Agile 价值流。

## 必需输出

- Product Goal
- 目标用户
- Backlog items
- User stories
- 每条 Story 的 Acceptance Criteria
- 每条 Story 的 INVEST 检查
- Story Mapping
- Story Splitting
- MVP
- 第一轮 Sprint Backlog
- Increment
- Eval 测试用例
- 优先级
- DoR
- DoD
- Review plan
- Retro plan
- `agile-plan.json`

## `agile-plan.json` 必填能力

- 写 User Story。
- 为每条 Story 写 Acceptance Criteria。
- 用 INVEST 检查 Story 质量。
- 用 Story Mapping 组织用户路径。
- 用 Story Splitting 拆出 MVP。
- 形成第一轮 Sprint Backlog。
- 定义 Increment。
- 生成 Eval 测试用例。

## Harness 反馈规则

如果 Harness 判断某个 story 不可测试、不可恢复或不可追踪，必须在 packaging 前更新 story、DoD 或 backlog。

## 硬失败

- 只有功能列表，没有用户价值。
- 缺少 DoD。
- 忽略 Harness 反馈。
- 缺少 `agile-plan.json`。
- Story 没有 Acceptance Criteria。
- Story 缺少 INVEST 任一项。
- 缺少 Story Map、MVP、Sprint Backlog、Increment 或 Eval cases。
