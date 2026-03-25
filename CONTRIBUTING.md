# 贡献指南

> 感谢你对 Awesome Harness Engineering 的兴趣！

---

## 如何贡献

### 1. 报告问题

发现 bug 或有改进建议？请提交 [Issue](https://github.com/East196/awesome-harness-engineering/issues)：

- 使用清晰的标题
- 描述问题复现步骤
- 提供环境信息（OS、Python 版本等）
- 如有错误日志，请附上

### 2. 提交代码

#### 步骤

```bash
# 1. Fork 仓库
# 点击 GitHub 页面的 Fork 按钮

# 2. 克隆你的 Fork
git clone https://github.com/YOUR_USERNAME/awesome-harness-engineering.git
cd awesome-harness-engineering

# 3. 创建分支
git checkout -b feature/your-feature-name

# 4. 提交更改
git add .
git commit -m "Add: 你的更改描述"

# 5. 推送到 GitHub
git push origin feature/your-feature-name

# 6. 创建 Pull Request
# 在 GitHub 上点击 "Compare & pull request"
```

#### 代码规范

- **Python**: 遵循 PEP 8，使用 Black 格式化
- **Markdown**: 使用标准 Markdown，代码块标注语言
- **提交信息**: 使用清晰的提交信息格式

```
Add: 新功能
Fix: 修复 bug
Update: 更新文档
Refactor: 重构代码
```

### 3. 完善文档

- 修正拼写错误
- 改进表述清晰度
- 添加更多示例
- 翻译其他语言

---

## 内容贡献

### 文章投稿

欢迎投稿关于 AI Agent Harness 的技术文章：

- 架构设计经验
- 实战案例分享
- 性能优化技巧
- 工具链整合方案

投稿方式：
1. 在 `articles/` 目录创建 Markdown 文件
2. 遵循现有文章格式
3. 提交 PR

### 示例代码

贡献新的 Harness 示例：

```
examples/
├── your-example/
│   ├── README.md      # 说明文档
│   ├── harness.py     # 核心实现
│   ├── config.yaml    # 配置文件
│   └── example.py     # 使用示例
```

### 架构图

贡献新的图解：

- 使用 SVG 格式
- 保持风格一致
- 添加中英文说明

---

## 开发环境

### 本地开发

```bash
# 安装依赖
pip install -r requirements.txt
pip install -r requirements-dev.txt

# 运行测试
pytest

# 代码格式化
black .
isort .

# 类型检查
mypy .
```

### 文档预览

```bash
# 本地预览 Docsify 站点
docsify serve

# 访问 http://localhost:3000
```

---

## 审核流程

1. **自动检查**: CI 运行测试和代码规范检查
2. **人工审核**: 维护者审核代码质量和内容准确性
3. **合并**: 通过后合并到 main 分支

---

## 行为准则

- 尊重他人，友善交流
- 接受建设性批评
- 关注社区最佳利益
- 禁止骚扰和歧视

---

## 联系方式

- GitHub Issues: [提交问题](https://github.com/East196/awesome-harness-engineering/issues)
- 邮件: flybear16@outlook.com

---

再次感谢你的贡献！🎉
