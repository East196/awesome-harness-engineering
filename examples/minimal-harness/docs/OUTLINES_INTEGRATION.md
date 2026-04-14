# Outlines 结构化输出集成

本项目使用 [Outlines](https://github.com/outlines-dev/outlines) 保证 Evaluator 输出 100% 有效的 JSON。

## 为什么用 Outlines？

传统 LLM JSON 输出依赖后处理解析：
1. LLM 生成文本
2. 尝试 `JSON.parse()`
3. 失败则重试（浪费 token、不可靠）

Outlines 的 grammar-based generation：
1. 定义 JSON Schema → 转换为有限状态机（FSM）
2. 生成时在 logit 层过滤无效 token
3. **无效输出在物理上不可能**

## 在 Evaluator 中的使用

```python
from agents.evaluator import EvaluatorAgent, EvaluationResult

# 启用 Outlines（默认）
evaluator = EvaluatorAgent(use_outlines=True)
result = evaluator.evaluate(code, spec)
# result 是 EvaluationResult Pydantic 实例
# 100% 有效保证

# 禁用 Outlines（回退到 JSON 解析）
evaluator = EvaluatorAgent(use_outlines=False)
```

## Outlines 支持的模型

| 模型类型 | 支持情况 |
|----------|----------|
| OpenAI (api.openai.com) | ✅ 完整支持 |
| Anthropic (通过兼容层) | ⚠️ 需要 OpenAI 兼容包装 |
| Local (llama.cpp, vLLM) | ✅ 完整支持 |
| Hugging Face Transformers | ✅ 完整支持 |
| Azure OpenAI | ✅ 完整支持 |

## 配置

### OpenAI 兼容 API

```bash
# 使用代理（推荐）
export OPENAI_API_KEY="sk-..."
export OPENAI_BASE_URL="https://api.openai-proxy.org/v1"

# 或直接使用 OpenAI
export OPENAI_API_KEY="sk-..."
```

### 本地模型 (vLLM)

```python
from agents.evaluator import EvaluatorAgent

evaluator = EvaluatorAgent(use_outlines=True)

# 配置 outlines 使用 vLLM
evaluator._setup_outlines = lambda: outlines.generate.json(
    outlines.models.vllm("meta-llama/Llama-3.1-8B-Instruct"),
    EvaluationResult
)
```

### llama.cpp

```python
evaluator._setup_outlines = lambda: outlines.generate.json(
    outlines.models.llamacpp("./models/llama-3.1-8b.Q4_K_M.gguf"),
    EvaluationResult
)
```

## 扩展到其他 Agent

Planner 和 Generator 也可以用 Outlines：

```python
from pydantic import BaseModel
import outlines

class TaskSpecOutput(BaseModel):
    title: str
    description: str
    features: list[str]
    tech_stack: dict[str, str]
    acceptance_criteria: list[str]

# 配置 Outlines 生成器
model = outlines.models.openai("gpt-4o-mini", api_key=os.getenv("OPENAI_API_KEY"))
generator = outlines.generate.json(model, TaskSpecOutput)

# 生成结构化输出
spec = generator("创建一个待办事项应用")
```

## API 参考

### `EvaluatorAgent(use_outlines=True)`

- **use_outlines**: `bool` — 是否使用 Outlines（默认 `True`）
- 当 `OPENAI_API_KEY` 未设置时，自动回退到基础 LLM
- 当 Outlines 调用失败时，自动回退到基础 LLM

### Outlines 生成器类型

| 类型 | 函数 | 用途 |
|------|------|------|
| JSON | `outlines.generate.json(model, schema)` | 结构化 JSON |
| Choice | `outlines.generate.choice(model, options)` | 单选 |
| Regex | `outlines.generate.regex(model, pattern)` | 正则匹配 |
| Integer | `outlines.generate.integer(model)` | 整数 |
| Float | `outlines.generate.float(model)` | 浮点数 |

## 故障排除

### "OPENAI_API_KEY not set, Outlines will not be used"

这是正常的回退行为。设置环境变量即可启用：
```bash
export OPENAI_API_KEY="sk-..."
```

### Outlines 生成失败

EvaluatorAgent 会自动回退到基础 LLM + JSON 解析，不影响功能。

### 模型不支持 Outlines

某些模型（如某些本地模型）可能不完全兼容 Outlines。在这种情况下，EvaluatorAgent 会自动使用回退方案。

## 资源

- [Outlines 文档](https://outlines-dev.github.io/outlines)
- [Outlines GitHub](https://github.com/outlines-dev/outlines) (8k+ stars)
- [Outlines Discord](https://discord.gg/R9DSu34mGd)
