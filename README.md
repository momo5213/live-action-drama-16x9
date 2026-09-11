# 16:9 真人精品短剧 Skill

将剧本转为可执行的真人质感AI短剧镜头包：剧本节拍、分镜、运镜、光影、人物状态与细微表演、首帧和视频提示词，以及连续性与实片审查。

**当前计划格式：schema_version 2。** 本技能提供制作方法与结构检查，不包含视频生成引擎，也不依赖参考资料中的GitHub项目运行。

## 能做什么

- 根据人物目标、信息变化和情绪转折设计镜头，保持重要剧情事实与对白。
- 明确景别、构图、摄影机运动起止、焦点与世界光源位置。
- 将人物状态转换为与景别匹配的可见表情、呼吸和动作。
- 按4—15秒整数规划生成单元；只有动作与时空连续、机位可容纳并留有气口时才合并短动作。
- 分开提供制作卡、首帧提示词、视频提示词和声音安排。
- 检查裁剪切点、道具状态、时长和转场；记录修订及待验证项目。

## 安装与使用

下载整个仓库，将包含`SKILL.md`、`agents`、`references`和`scripts`的目录命名为`live-action-drama-16x9`，放入目标助手支持的技能目录。不要只复制`SKILL.md`，它会按需读取参考文件。

在Codex个人技能目录中，目录结构应为：

```text
~/.codex/skills/live-action-drama-16x9/
├── SKILL.md
├── agents/openai.yaml
├── references/
└── scripts/validate_plan.py
```

调用示例：

```text
使用 $live-action-drama-16x9 处理下面的剧本。
按16:9真人精品短剧标准，输出合理分镜、运镜、光影、人物状态与细微表演，以及可直接使用的逐镜视频提示词。
生成单元限定4—15秒整数，符合连续性要求时才合并短动作，保留前后气口。
交付前审查并修订问题，明确文本预审结果与待实片验证项。
视频工具及版本：未指定时使用平台中立版。
剧本：[粘贴剧本]
```

## 文件导航

| 文件 | 用途 |
| --- | --- |
| [SKILL.md](SKILL.md) | 技能入口与完整流程 |
| [导演决策参考](references/directing.md) | 摄影、光影、表演与连续性 |
| [输出规范](references/output-contract.md) | 镜头卡与JSON字段 |
| [模型适配](references/model-adapters.md) | 平台能力核对与提示词适配 |
| [审查规范](references/review.md) | 硬门槛、修订与最终结论 |
| [完整示例](references/worked-example.md) | 三镜头、20秒的原创演示 |
| [示例计划](references/example-plan.json) | 可运行的结构检查样本 |
| [研究来源](references/sources.md) | 方法来源及采用边界 |
| [项目可用性复核](references/repository-audit.md) | GitHub参考项目证据分级 |
| [发布审查记录](docs/review-report.md) | 已完成检查与验证限制 |

## 本地检查

结构检查器仅使用Python标准库，建议Python 3.10或更新版本。从仓库根目录运行：

```bash
python scripts/validate_plan.py references/example-plan.json
python tests/check_plan.py
```

`PASS_MECHANICAL_ONLY`表示可机器检查的结构约束通过。回归检查包含24个案例；不会调用外部模型、产生视频费用或修改示例文件。

## 验证范围

文本预审和实片审查分别进行。没有实际视频与音轨时，不能确认人物稳定、微表情、光影、物理接触、口型或剪辑节奏，也不能承诺“绝对完美”。

GitHub项目用于方法参考，未被整体安装或作端到端真实生成验证。模型参数随入口和版本变化，实际生成前需核对当前官方能力。

本仓库仅包含技能、原创示例、校验代码与审查资料，不包含用户账号凭据、私人剧本或本机依赖目录。
