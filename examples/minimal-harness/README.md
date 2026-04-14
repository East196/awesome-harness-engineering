# 最小可运行的 Harness 示例

> 一个最简化的多智能体 Harness 实现，帮助你快速理解核心概念。

## 项目结构

```
minimal-harness/
├── README.md
├── requirements.txt
├── config.yaml
├── agents/
│   ├── __init__.py
│   ├── planner.py
│   ├── generator.py
│   └── evaluator.py
├── core/
│   ├── __init__.py
│   ├── harness.py
│   └── context_manager.py
└── examples/
    └── simple_task.py
```

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
export ANTHROPIC_API_KEY="your-api-key"
```

### 3. 运行示例

```bash
python examples/simple_task.py
```

## 核心概念演示

### Planner（规划器）

```python
from agents.planner import PlannerAgent

planner = PlannerAgent()
spec = planner.plan("创建一个待办事项应用")
print(spec)
```

### Generator（生成器）

```python
from agents.generator import GeneratorAgent

generator = GeneratorAgent()
code = generator.generate(spec)
print(code)
```

### Evaluator（评估器）

```python
from agents.evaluator import EvaluatorAgent

evaluator = EvaluatorAgent()
feedback = evaluator.evaluate(code, spec)
print(feedback)
```

## 完整工作流

```python
from core.harness import MinimalHarness

harness = MinimalHarness()
result = harness.run(
    prompt="创建一个待办事项应用",
    max_iterations=5
)
```

## 输出示例

```
🚀 启动 Minimal Harness

[Planner] 分析需求...
✅ 生成产品规格（3个功能点）

[Generator] Sprint 1/3...
✅ 实现功能：创建任务
✅ 实现功能：标记完成
✅ 实现功能：删除任务

[Evaluator] 评估中...
✅ 功能完整性：通过
✅ 代码质量：通过
⚠️  用户体验：建议优化

[Generator] Sprint 2/3...
✅ 优化：添加任务优先级
✅ 优化：添加截止日期

[Evaluator] 评估中...
✅ 所有标准通过！

✨ 完成！总耗时：2.3分钟
📁 输出目录：./output/todo-app
```

## 配置说明

### config.yaml

```yaml
# 模型配置
model:
  planner: claude-3-opus-20240229
  generator: claude-3-sonnet-20240229
  evaluator: claude-3-haiku-20240307

# 迭代配置
iteration:
  max_iterations: 5
  min_quality_score: 0.8

# 上下文配置
context:
  max_tokens: 4000
  reset_threshold: 0.8
```

## 进阶用法

### 自定义评估标准

```python
from agents.evaluator import EvaluatorAgent

custom_criteria = {
    "code_quality": 0.3,
    "performance": 0.2,
    "security": 0.3,
    "maintainability": 0.2
}

evaluator = EvaluatorAgent(criteria=custom_criteria)
```

### 上下文重置

```python
from core.context_manager import ContextManager

manager = ContextManager()
manager.reset_context()  # 清除上下文，保留关键状态
```

## 调试模式

```python
import logging

logging.basicConfig(level=logging.DEBUG)

harness = MinimalHarness(debug=True)
```

## 常见问题

**Q: 为什么需要 Planner？**  
A: Planner 将模糊的需求转化为具体可执行的任务列表，避免生成器盲目编码。

**Q: Evaluator 如何评分？**  
A: 基于预定义的标准（功能完整性、代码质量等），使用 LLM 进行多维度评估。

**Q: 上下文重置会丢失什么？**  
A: 只重置对话历史，保留关键状态（如已生成的代码、评估结果）在结构化产物中。

## 下一步

- [前端设计 Harness](../frontend-harness/) — 规划中
- 其他示例 — 后续阶段实现
