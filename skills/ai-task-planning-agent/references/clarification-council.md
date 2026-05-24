# Clarification Council Loop

## 职责

在 Clarification Engine 之后、Requirement Discovery & Modeling Engine 之前，使用“追问 + 挑刺”双轨机制，把模糊想法变成可确认的需求理解。

## 每轮追问

每轮必须输出五问，字段固定为：

| 序号 | 问题 | 为什么这么问 | 不会会怎样 | 建议回答 |
|---:|---|---|---|---|

`建议回答` 只是示例，不能自动写入事实源。

## 每轮挑刺

用户回答后，不得直接进入下一轮。必须先挑刺并输出：

- 问题点
- 影响
- 涉及字段
- 是否阻塞
- 建议修正

挑刺重点包括逻辑矛盾、隐含假设、用户缺失、场景缺失、目标不可测试、成功标准模糊、范围膨胀、非目标缺失、工具或权限风险、后续执行返工点。

## 角色参与

每轮角色都要参与，但必须结构化、短输出：

- `role`
- `statement`
- `challenge`
- `supplement`
- `field_updates`
- `blocking`

角色没有绑定受影响字段时，该轮无效。

## 用户确认

每轮挑刺后，必须整理 `revised_understanding` 给用户确认。用户未确认时，不得进入下一轮，不得生成交付包 ready 结论。

## 阶段 Brief

每三轮必须输出一次阶段性 brief，请用户确认。少于三轮但准备进入建模前，也要保留至少一个 brief 或说明本阶段确认结果。

## 必需输出

- `clarification-session.json`
- 必要时输出人工阅读版 clarification brief

## 硬失败

- 任一轮不是五问。
- 问题缺少“为什么这么问”“不会会怎样”或“建议回答”。
- 用户回答后未挑刺。
- 挑刺没有映射字段。
- 角色没有 statement、challenge、supplement 或 field_updates。
- 用户未确认就进入下一阶段。
- Blocking questions 非空。
