# SKILL.md Governance

## 职责

治理 `SKILL.md` 入口文件，使它保持清晰、可触发、可执行、可验证。

## 入口文件边界

`SKILL.md` 只保留：

- 触发边界
- 主流程
- 必读 references
- 必跑 scripts
- 硬失败条件

详细需求方法、敏捷方法、模板和案例必须放入 `references/`、`schemas/`、`fixtures/` 或 `tests/`。

## 必需规则

- frontmatter 只允许 `name` 和 `description`。
- `name` 必须为 `ai-task-planning-agent`。
- `description` 必须默认中文，并保留产品触发边界。
- `SKILL.md` 必须列出 v0.4 必需 references。
- `SKILL.md` 必须列出 v0.4 必跑 scripts。
- `SKILL.md` 必须列出必需机器事实源的硬失败。
- `SKILL.md` 不得承载完整领域方法论。

## 必跑验证

```bash
python scripts/validate_skill_entry.py ../SKILL.md
```

## 硬失败

- 缺少必需 reference。
- 缺少必需 script。
- 缺少 `clarification-session.json`、`requirement-model.json` 或 `agile-plan.json` 硬失败。
- 入口文件过长，说明领域知识没有外置。
