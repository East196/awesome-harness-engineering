# Awesome Harness Engineering

> AI Agent Harness 工程实践精选

[![GitHub stars](https://img.shields.io/github/stars/East196/awesome-harness-engineering?style=social)](https://github.com/East196/awesome-harness-engineering)
[![GitHub license](https://img.shields.io/github/license/East196/awesome-harness-engineering)](https://github.com/East196/awesome-harness-engineering/blob/main/LICENSE)

---

## 简介

本仓库收集和整理关于 **AI Agent Harness** 设计的最佳实践、架构模式和工程方法。

**什么是 Agent Harness？**

Agent Harness 是一种系统化的 AI 代理配置和编排框架，通过多智能体架构、持续学习系统和自动化工作流，让 AI 能够在长时间运行中保持高质量输出。

---

## 内容目录

### 📚 Anthropic 官方技术博客

- **[Harness 设计深度解析](article.md)** - 多智能体架构、生成器-评估器循环、前端设计四维标准
- **[英文原文](original-en.md)** - 原始英文版本（baoyu-url-to-markdown 抓取）
- **[中文翻译](original-zh.md)** - 完整中文翻译

### 🚀 Everything Claude Code

- **[ECC 架构指南](bighat-ecc-zh.md)** - 84k+ stars 的开源配置系统
- **[英文原文](bighat-ecc-en.md)** - Big Hat Group 技术分析

### 🎨 架构图解

| 图片 | 说明 |
|------|------|
| ![多智能体架构](diagram.png) | 多智能体 Harness 架构 — Planner、Generator、Evaluator 形成反馈循环 |
| ![上下文管理对比](context-comparison.png) | 上下文焦虑问题与上下文重置解决方案对比 |
| ![设计评估标准](design-criteria.png) | 前端设计评估四维标准：设计质量、原创性、工艺、功能性 |

---

## 核心概念

### 多智能体架构

```
┌─────────────────────────────────────────┐
│         多智能体 Harness 架构            │
├─────────────────────────────────────────┤
│                                         │
│   Planner ──→ Generator ──→ Evaluator   │
│   (规划器)      (生成器)      (评估器)    │
│       │           ↑            │        │
│       │           └────────────┘        │
│       │            (反馈循环)            │
│       └────────────────────────────────→  │
│                     (迭代优化)            │
│                                         │
└─────────────────────────────────────────┘
```

### 关键特性

| 特性 | 说明 |
|------|------|
 **生成器-评估器分离** | 将执行工作的代理与评判工作的代理分离，解决自我评估偏差 |
| **上下文重置** | 清除上下文窗口并启动新代理，解决上下文焦虑和失焦问题 |
| **可量化评估标准** | 将主观判断（如设计质量）转化为可评分的具体指标 |
| **持续学习系统** | 跨会话积累知识，模式随使用次数增加而改善 |

---

## 快速开始

### 本地预览

```bash
# 克隆仓库
git clone https://github.com/East196/awesome-harness-engineering.git
cd awesome-harness-engineering

# 使用 docsify 本地预览
npm i docsify-cli -g
docsify serve

# 或直接使用 Python
python3 -m http.server 3000
```

### GitHub Pages 部署

本仓库已配置 GitHub Pages，访问：
**https://east196.github.io/awesome-harness-engineering**

---

## 参考文档

- [Anthropic Engineering Blog](https://www.anthropic.com/engineering)
- [Claude Agent SDK](https://platform.claude.com/docs/en/agent-sdk/overview)
- [Everything Claude Code](https://github.com/affaan-m/everything-claude-code)
- [Big Hat Group Analysis](https://www.bighatgroup.com/blog/everything-claude-code-ai-agent-harness-guide/)

---

## 贡献

欢迎提交 PR 和 Issue！

---

## 许可

MIT License © 2026 flybear16
