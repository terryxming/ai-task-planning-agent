# Harness Execution Planner

## 职责

为下游 coding agent 定义执行可靠性契约。

## 必需输出

- Context contracts
- Tool contracts
- Workflow steps
- Sandbox rules
- Test plan
- Eval cases
- Trace requirements
- Recovery paths
- Regression cases

## 硬失败

- 缺少 tool contract。
- 缺少 recovery path。
- 缺少 trace requirement。
- Eval cases 缺少 negative cases。
