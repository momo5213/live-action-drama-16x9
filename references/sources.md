# 研究依据与采用边界

检索与阅读日期：2026-09-10。近期指本次能够核实的2026年公开项目，另保留与任务相关的2025年研究与案例。没有以GitHub星数代替质量评估，没有本地运行外部项目，没有逐镜观看所列影片。本文件区分官方事实、项目自述和本skill的设计判断。

第二轮已进一步检查实际入口、测试范围、发行信息及工作流矛盾：[项目可用性复核](repository-audit.md)。以下首次阅读记录不代表项目已可用于生产；可用性结论以复核记录为准。

## 近期作品：用于建立观察方向

### Runway AIF 2026

[官方获奖名单及简介](https://aif.runwayml.com/)

已核实：Grand Prix为Robert Gaudette的《A Face Only A Mother Could Love》；Honoree包含《Costa Verde》与Dave Clark的《TAIRELL ISN'T REAL》。官方简介分别涉及孤独与相遇、家庭夏日记忆、人物身份危机。

本skill的取舍：这些题材适合把观察方向放在人物目标、日常动作、主观体验和状态变化。本次仅阅读官方简介与获奖信息，不能据此评价具体焦段、微表情质量、完整工作流或断言全部为纯AI真人剧。未将动画获奖片直接当作真人表演标杆。

### Reply AI Film Festival 2025

[官方获奖公告，2025-09-05](https://www.reply.com/en/newsroom/news/love-at-first-sight-by-jacopo-reale-is-the-winning-short-film-of-the-reply-ai-film-festival-the-international-competition-that-bridges-cinema-and-ai)

已核实：Jacopo Reale的《Love at First Sight》获该届冠军。公告强调原创性、制作质量与AI在整体创作流程中的使用。

本skill的取舍：将叙事、情绪与整体完成度纳入审核，避免单独按清晰度评判。本次没有核验逐镜生成记录，不能把制作天数或使用模型等二手报道当作已验证生产参数。2025年案例不是2026年最新获奖结论。

## GitHub与研究项目：借鉴结构，不直接移植

### showlab/MovieAgent

[仓库](https://github.com/showlab/MovieAgent) · [实际提示词文件](https://github.com/showlab/MovieAgent/blob/main/movie_agent/system_prompts.py)

已阅读README、目录及提示词文件的编剧、场景规划和监督相关部分。README介绍剧本与角色库驱动的分层电影规划；实际文件将剧本、人物关系、场景情绪、道具和摄影信息分开组织，并包含监督反馈角色。

采用：场景—节拍—镜头分层、角色资料、原剧本追溯与修订环节。不采用：固定场景数量/最低字数、要求输出内部思维过程、旧模型安装步骤。README更新日期本身存在2024/2025顺序不一致，不用于证明最新活跃度。未运行或验证生成质量。

### XucroYuri/take

[仓库](https://github.com/XucroYuri/take) · [镜头语言文件](https://github.com/XucroYuri/take/blob/main/skills/take/references/shot-language.md) · [输出契约](https://github.com/XucroYuri/take/blob/main/skills/take/references/output-contract.md)

已读实际skill、镜头词表和输出契约。项目把节拍、镜头、图像提示词与文件校验联系起来。

采用：稳定ID、节拍映射、设置与提示词分离、先检查结构再生产。本skill自行设计格式，不宣称兼容take导入。

不采用：2—3秒短镜头默认值、固定供应商路由、未经官方核对的型号优劣与可用性断言；过肩构图和摄影机高度角在本skill中分开。公开文档可借鉴，不据此宣称软件或电影质量已实测。

### LudwigKienle/ai-video-production-editor

[仓库与README](https://github.com/LudwigKienle/ai-video-production-editor)

已读README，页面标有September 2026更新内容，描述了从剧本、分镜、拍摄到剪辑调色的生产界面及连续性审查。

采用：完整镜头制作卡、图像/视频阶段分开、连续性复查与修订回路。仅阅读文档，未安装、未审计代码、未验证各供应商集成。其列举的型号不复制为本skill官方能力表。

### FilmAgent

[作者项目页](https://filmagent.github.io/) · [论文摘要](https://arxiv.org/abs/2501.12909)

研究对象为虚拟3D空间中的电影自动化，组织编剧、演员与摄影等职责。

采用：以不同制作职责检查同一方案。默认由当前助手顺序完成，不自动派生代理；虚拟空间的可控性不能直接推断为生成式真人视频的表现保证。

## 生成模型官方指南

- [Runway Gen-4](https://help.runwayml.com/hc/en-us/articles/39789879462419-Gen-4-Video-Prompting-Guide)：简洁、动作导向、正向表述、逐项调整。
- [Runway图生视频](https://help.runwayml.com/hc/en-us/articles/48324313115155-Image-to-Video-Prompting-Guide)：图片与文字分工。
- [Veo提示指南](https://deepmind.google/models/veo/prompt-guide/)：场面、人物、动作、摄影与音频描述。

具体适配见[model-adapters.md](model-adapters.md)，不把某模型的写法当作所有模型的规律。

## 本用户已有经验如何纳入

采用本任务对话中已明确的约束：16:9、真人质感、4—15秒整数、短动作按连续性合并、首尾气口、长文本可复制、人物与道具连续性、图生与文生区别、最终审查。

对话中没有提供实际剧本或生成视频，因此没有“用户既有成片效果已验证”的结论。前次给出的固定/运动镜头比例只作为练习起点，本skill不把它固化为精品标准。

所有工作流、示例、审查门槛与脚本均为本次面向需求重新编写；外部资料只做方法参考，不复制项目实现，不引入其依赖或操作指令。

## 更新方式

用户再次要求近期参考或指定新模型时，核对官方发布、仓库实际文件和适用版本；记录验证日期、来源类型及采用/不采用的理由。新来源必须改善镜头决策或生产质量，不因“最新”自动替换已适用规则。
