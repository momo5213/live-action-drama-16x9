# GitHub项目可用性复核

复核日期：2026-09-10。没有安装这些项目、没有调用其付费视频服务。采用“方法参考／静态代码证据／上游自动测试／本地运行／真实生成”分层，不把前一层当作后一层。当前skill不导入这些仓库代码，也不需要它们才能分析剧本。

## MovieAgent：研究思路可参考，不适合直接作为本用户的生产底座

核对版本：`d84041bed8bc8be460664528d9e9924cdde384ba`，提交日期2025-03-26。

[运行入口](https://github.com/showlab/MovieAgent/blob/d84041bed8bc8be460664528d9e9924cdde384ba/movie_agent/run.py)中有两项直接不适配：
- 输出文件名用竖线拼接场景和镜头名称；竖线不能用作Windows普通文件名，需先修改命名策略。
- 生成调用传入1024×512尺寸，即2:1，而非本项目16:9；需要调整并验证后端能否正确支持。

[启动脚本](https://github.com/showlab/MovieAgent/blob/d84041bed8bc8be460664528d9e9924cdde384ba/movie_agent/script/run.sh)使用Shell环境变量、CUDA设备索引、特定模型与权重路径；不能当作本Windows环境即装即用。

[音频问题#9](https://github.com/showlab/MovieAgent/issues/9)与[权重/编译问题#10](https://github.com/showlab/MovieAgent/issues/10)反映用户报告的复现困难。问题帖不是独立复现证据，不据此断言所有环境均失败。

结论：保留分层场景规划的参考价值，不推荐原样部署；本次无本地端到端运行或真实生成通过记录。

## take：有工程测试证据，真实生成和真人质量仍未验证

核对版本：`47c17216b5ad74ee7dd376e8508266e29aefae2c`；发行标签0.1.0，发布时间2026-08-24。

[该版本CI运行成功](https://github.com/XucroYuri/take/actions/runs/32768410083)。[工作流](https://github.com/XucroYuri/take/blob/47c17216b5ad74ee7dd376e8508266e29aefae2c/.github/workflows/ci.yml)使用Ubuntu、Node20/22/24执行构建、类型、lint与测试。

[测试说明](https://github.com/XucroYuri/take/blob/47c17216b5ad74ee7dd376e8508266e29aefae2c/docs/testing.md)明确测试不访问外部网络，传输使用本地模拟服务器，CLI使用mock provider。故CI成功证明其所覆盖的工程检查通过，不证明供应商账号/接口、中文口型或视频成片质量。

[实际schema](https://github.com/XucroYuri/take/blob/47c17216b5ad74ee7dd376e8508266e29aefae2c/packages/core/src/schemas.ts)对durationSec只要求正数，不保证本用户4—15秒整数；也不能替代本skill的动作气口与切点连续性审查。

结论：可作轻量分镜数据组织的候选参考；上游测试通过、本地运行未测、真实视频未测。不能称为已验证的真人精品剧引擎。

## ai-video-production-editor：有发行包，但仓库规则存在冲突

本次默认分支提交：`2e47f42a86ccf30641c22be4662891f0a2ed8e7c`（2026-09-03）。

[v2.7.0发行页](https://github.com/LudwigKienle/ai-video-production-editor/releases/tag/v2.7.0)有Windows EXE及macOS DMG，发行日期2026-06-02。存在下载包不证明已经在用户机器安装可用，也不证明它覆盖README中9月列出的全部功能。

README与目录有应用源码和本地构建说明，但[Repository Guard](https://github.com/LudwigKienle/ai-video-production-editor/blob/2e47f42a86ccf30641c22be4662891f0a2ed8e7c/.github/workflows/repository-guard.yml)同时要求仓库仅供下载，并禁止src、electron、package.json等路径。对应[运行失败](https://github.com/LudwigKienle/ai-video-production-editor/actions/runs/33796938339)发生在该路径检查步骤。

这说明仓库治理配置与当前源码布局冲突；不是应用编译失败的实测证据，更不能直接推断发行包无法使用。

结论：只保留其工作流界面组织作为参考；当前证据不足以背书部署稳定性。本次未安装或验证真实模型集成。

## FilmAgent

仍是虚拟3D空间电影规划的研究方法参考，参见[作者项目页](https://filmagent.github.io/)。本次未安装或验证其工程运行，不作为真人视频生成后端。

## 对skill的影响

本skill的文本分析、镜头卡和Python结构检查均为独立编写。无需安装上述项目。外部项目的不适配之处没有作为依赖引入；其方案中的固定时长、模型路由、思维过程输出等没有沿用。

若今后用户明确要求接入某个项目，应针对选定提交先核对安装依赖、平台、实际模型入口，再做最小本地测试与真实生成测试。最终报告每一层的实测范围，不能只凭README、release或CI宣称生产可用。
