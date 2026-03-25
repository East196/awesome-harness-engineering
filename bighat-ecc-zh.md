---
url: https://www.bighatgroup.com/blog/everything-claude-code-ai-agent-harness-guide/
title: "Everything Claude Code：你的团队缺失的 Agent Harness"
author: "Big Hat Group"
translated_from: "en"
captured_at: "2026-03-25T15:16:13.821Z"
---

# Everything Claude Code：你的团队缺失的 Agent Harness

大多数开发者只使用了 Claude Code、Codex 或 Cursor 约 30% 的能力——基本的基于聊天的代码生成和默认设置。Everything Claude Code（ECC）是一个开源配置系统，它将这些工具视为完整的 AI Agent 编排平台，而非聊天机器人。它拥有 84,000+ GitHub stars、108+ skills、25+ 专业 agents，以及一个在会话间不断变聪明的持续学习系统。

如果你的团队正在投资 AI 辅助开发，但尚未评估 ECC 的架构，那么你正在错失重要的能力。

## 从黑客马拉松胜利到 84k Stars

Everything Claude Code 始于一场赌注。2025 年 9 月，Affaan Mustafa 和队友 @DRodriguezFX 参加了在纽约市举办的 Anthropic × Forum Ventures 黑客马拉松。在 100 多个竞争团队中，他们仅使用 Claude Code 在八小时内构建了 zenith.chat——一个完整的 AI 产品。他们赢得了第一名和 15,000 美元的 Anthropic API 积分奖励。

优势并非来自新颖的算法，而是 Affaan 通过日常生产使用积累的 10 个月 Claude Code 配置优化。获胜后，他将整个系统开源。

Affaan 的背景很重要。他是 Itô（一个预测市场聚合器）的联合创始人，elizaOS（Web3 中最广泛使用的 AI Agent 框架，17k+ stars）的核心贡献者，之前还构建了达到 70k 并发观众和 3800 万美元峰值 FDV 的自主交易代理。这家伙懂 Agent 系统。

该仓库于 2026 年 1 月 17 日发布，包含 9 个 agents、14 个命令和 11 个 skills。到 1 月底已有 50,000 stars。到 2026 年 3 月：84,000+ stars、30+ 贡献者、五种语言的翻译，以及 997 个通过的测试。它是 GitHub 历史上增长最快的开发者工具仓库之一。

## 四层架构

ECC 不是一堆技巧的杂烩。它是一个结构化系统，有四个不同的层次，每一层都建立在下一层之上。理解这个架构是理解 Everything Claude Code 为何有效的关键。

### 第一层：用户交互——命令和规则

57+ 斜杠命令作为结构化工作流的入口点：

- **核心工作流：** /plan、/tdd、/e2e 用于任务规划、测试驱动开发和端到端测试
- **代码质量：** /code-review、/build-fix、/refactor-clean 用于审查和修复
- **多 Agent：** /multi-plan、/multi-execute、/orchestrate 用于协调并行 Agent 工作
- **学习：** /learn-eval、/evolve 用于模式提取和技能进化

规则是按语言组织的始终加载的指南——通用约定加上 TypeScript、Python、Go、Swift、PHP 等的语言特定集合。这些涵盖编码风格、git 工作流、测试要求（默认 80% TDD 覆盖率）、性能模式和安全实践。

### 第二层：智能——Agents 和 Skills

这是 Claude Code 配置变得有趣的地方。ECC 定义了 25+ 个专业 agents，具有明确的责任边界和受限的工具权限：

- **编排器**（Planner、Architect）获得广泛的工具访问权限，可以委托给其他 agents
- **质量 agents**（Code Reviewer、Security Reviewer、Database Reviewer）以只读方式运行
- **构建器**（TDD Guide、Build Error Resolver、E2E Runner）处理实现
- **语言专家**（Go Reviewer、Python Reviewer）提供有针对性的分析

108+ Claude Code skills 是按需加载的领域知识模块——在被调用之前不消耗上下文 tokens。Skills 涵盖后端模式、前端模式、数据库迁移、API 设计、Docker、部署、安全扫描，以及 Django、Laravel、Spring Boot、Swift、C++ 和 Perl 的框架特定工作流。

Agent/skill 分离很清晰：agents 定义谁做工作以及他们有什么权限；skills 定义领域知识和程序。

### 第三层：自动化——Hooks 和 Scripts

事件驱动的 hooks 在生命周期阶段触发——PreToolUse、PostToolUse、SessionStart、SessionEnd、PreCompact 和 Stop。这些是跨平台的 Node.js 脚本（早期版本使用脆弱的 bash 单行命令），具有运行时控制：

```
ECC_HOOK_PROFILE=minimal|standard|strict
ECC_DISABLED_HOOKS=hook1,hook2
```

这意味着质量门在工具执行前自动运行，结果在执行后验证，上下文在会话开始时加载，模式在会话结束时提取——无需人工干预。

### 第四层：学习——新颖的部分

这是将 Everything Claude Code 与组织良好的 dotfiles 仓库区分开来的地方。

## 持续学习系统

ECC 通过两代实现跨会话知识积累：

**版本 1（基于 skill）** 通过会话结束时的 Stop hooks 提取编码模式，并存储在 ~/.claude/skills/learned/ 中。它覆盖了大约 50-80% 的可学习模式。

**版本 2（基于 instinct）** 更具野心。它通过 PreToolUse 和 PostToolUse hooks 观察每个工具交互，实现 100% 覆盖。每个学习单元是一个"Instinct"——一个置信度分数范围为 0.3 到 0.9 的微观模式。当系统积累 3+ 相关 instincts 时，/evolve 命令将它们聚合为可重用的 Skill 模块。

实际效果：你的 Claude Code 设置随着使用次数的增加而显著改善。有效的模式得到强化。失败的模式被降权。团队可以导入和导出 instinct 库，这意味着一个开发者辛苦获得的模式可以转移到整个团队。

这是对 AI 编码助手设置空间的真正新颖贡献。大多数配置系统是静态的——你设置一次并手动维护。ECC 的学习层是动态和自我改进的。

## 为什么企业团队应该关注

### 跨 Harness 兼容性

虽然为 Claude Code 而生，ECC 现在可以跨 Claude Code、Codex (OpenAI)、Cursor、OpenCode、Cowork 和 Antigravity 工作。相同的 skills、agents 和模式可以跨工具转移。对于评估多个 AI 编码助手或对冲供应商锁定风险的团队来说，这很重要——你的 AI Agent Harness 投资不绑定到单一平台。

### 安全：AgentShield

AgentShield 集成（/security-scan）提供 1,282 个测试和 102 条专门为 AI Agent 系统设计的规则。这不是通用的 SAST——它针对 Agentic AI 独特的新兴攻击面：提示注入、工具滥用、通过 Agent 委托的权限提升，以及通过上下文窗口的数据外泄。

AgentShield 在 Cerebral Valley × Anthropic 活动中亮相，解决了一个真正的空白。随着 AI Agents 进入生产环境，访问文件系统、API 和数据库，专门构建的安全扫描变得至关重要。

### 生产验证

ECC 不是理论性的。它通过以下方式验证：

- 赢得 Anthropic 黑客马拉松——在 8 小时内构建完整产品
- 10+ 个月的日常生产使用构建真实产品
- 997 个内部测试覆盖 agents、skills、hooks 和打包
- 84,000+ stars 和 30+ 贡献者提供持续反馈
- 两份病毒式指南（速记和长文）拥有 300 万+ 跟踪浏览量和估计 1000 万+ 跨平台触达

## 入门指南

ECC 通过 npm 安装，支持跨平台：

- 克隆仓库或通过 ecc-universal（npm 包）安装
- 选择 hook 配置文件——minimal 用于低开销，standard 用于大多数团队，strict 用于最大质量门
- 从核心命令开始：/plan 用于任务分解，/tdd 用于测试驱动开发，/code-review 用于自动审查
- 让持续学习系统（v2 instincts）随着时间的推移建立你团队的模式库
- 在将任何具有 Agent 访问权限的内容发布到生产系统之前，通过 AgentShield 运行 /security-scan

该仓库通过 GitHub Marketplace 应用提供 Claude Code 插件，有免费、专业和企业层。贡献模板存在于 agents、skills、commands、rules、hooks 和翻译中。

Affaan 撰写的两份指南——速记指南（设置和理念）和长文指南（token 优化、内存持久化、evals、并行化）——是深入定制之前必读的。

## 我们的观点

在 Big Hat Group，我们与通过 OpenClaw 和类似平台部署 AI Agents 的企业团队合作。ECC 的架构直接映射到我们每天使用的模式——OpenClaw 已经运行类似的 skills 系统，许多 ECC skills 直接兼容。

四层模型（交互 → 智能 → 自动化 → 学习）是我们见过的最清晰的心智框架，用于将 Agent Harness 工程视为一门学科。在 ECC 之前，配置 AI 编码助手是临时性的——分散的技巧、个人配置文件、论坛帖子。ECC 将其形式化为结构化和可转移的东西。

如果你的团队正在使用 Claude Code、Codex 或任何类似的 AI 编码助手，评估 Everything Claude Code 的模式。你不需要采用整个系统——即使挑选 Agent 委托模型或持续学习架构也会改善你的 AI 辅助开发工作流。

该仓库采用 MIT 许可，积极维护：[github.com/affaan-m/everything-claude-code](https://github.com/affaan-m/everything-claude-code)

---

**参考文档：**
- 原文：https://www.bighatgroup.com/blog/everything-claude-code-ai-agent-harness-guide/
- ECC 仓库：https://github.com/affaan-m/everything-claude-code
