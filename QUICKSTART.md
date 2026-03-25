# 快速开始

> 5 分钟上手 AI Agent Harness

---

## 方式一：Docker 一键部署（推荐）

```bash
# 克隆仓库
git clone https://github.com/East196/awesome-harness-engineering.git
cd awesome-harness-engineering

# 启动 Docsify 文档站点
docker run -it --rm -p 3000:3000 -v $(pwd):/docs docsify/docsify serve

# 访问 http://localhost:3000
```

---

## 方式二：本地开发环境

### 1. 安装依赖

```bash
# Python 3.10+
pip install anthropic openai pyyaml python-dotenv

# Playwright (用于前端测试)
pip install playwright
playwright install

# Node.js (用于 Docsify)
npm install -g docsify-cli
```

### 2. 配置 API 密钥

```bash
# 复制环境变量模板
cp examples/minimal-harness/.env.example .env

# 编辑 .env 文件，填入你的 API 密钥
vim .env
```

`.env` 文件内容：
```bash
ANTHROPIC_API_KEY=sk-ant-api03-your-key-here
LOG_LEVEL=INFO
```

### 3. 运行示例

```bash
# 最小 Harness 示例
cd examples/minimal-harness
python examples/simple_task.py

# 预期输出：
# 🚀 Minimal Harness 示例
# 📋 任务: 创建一个简单的待办事项应用
# ✅ 执行完成!
# ⭐ 质量分数: 0.85/1.0
```

---

## 方式三：GitHub Codespaces

[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://github.com/East196/awesome-harness-engineering/codespaces)

点击按钮直接在浏览器中启动完整开发环境。

---

## 第一个 Harness 项目

### 创建项目结构

```bash
mkdir my-harness-project
cd my-harness-project

# 创建基础文件
touch harness.py config.yaml .env
```

### 编写代码

```python
# harness.py
from anthropic import Anthropic
import yaml

class MyHarness:
    def __init__(self, config_path="config.yaml"):
        with open(config_path) as f:
            self.config = yaml.safe_load(f)
        self.client = Anthropic()
    
    def run(self, prompt: str):
        # 1. Planning
        spec = self._plan(prompt)
        
        # 2. Generation
        code = self._generate(spec)
        
        # 3. Evaluation
        score = self._evaluate(code)
        
        return {"code": code, "score": score}
    
    def _plan(self, prompt):
        response = self.client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1000,
            messages=[{
                "role": "user",
                "content": f"将以下需求转化为技术规格：\n{prompt}"
            }]
        )
        return response.content[0].text
    
    def _generate(self, spec):
        # 生成代码...
        pass
    
    def _evaluate(self, code):
        # 评估代码...
        pass

# 运行
if __name__ == "__main__":
    harness = MyHarness()
    result = harness.run("创建一个待办事项应用")
    print(result)
```

### 运行项目

```bash
python harness.py
```

---

## 下一步

- 📚 [阅读完整文档](https://east196.github.io/awesome-harness-engineering)
- 🔍 [查看示例代码](examples/)
- 🎨 [尝试前端设计 Harness](examples/frontend-harness/)
- 🏗️ [了解全栈开发 Harness](examples/fullstack-harness/)

---

## 常见问题

**Q: 需要什么 API 密钥？**  
A: 推荐使用 Anthropic API (Claude)，也支持 OpenAI API。

**Q: 免费额度够吗？**  
A: 最小示例运行成本约 $0.01-$0.1，完整 Harness 可能 $1-$10。

**Q: 支持哪些模型？**  
A: Claude 3 (Opus/Sonnet/Haiku)、GPT-4、GPT-3.5。

**Q: 可以商用吗？**  
A: 本项目 MIT 许可，可自由商用。

---

*遇到问题？提交 [Issue](https://github.com/East196/awesome-harness-engineering/issues)*
