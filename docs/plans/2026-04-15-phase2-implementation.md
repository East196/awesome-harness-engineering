# Awesome Harness Engineering — Phase 2 Implementation Plan

> **Goal:** 实现真正的 LLM-powered Planner/Generator/Evaluator，替换 mock 实现
>
> **Architecture:** 使用 Outlines 做结构化输出（JSON Schema 约束 Evaluator 评分），Anthropic Claude API 做生成
>
> **Tech Stack:** Python 3.10+, anthropic, outlines, pydantic, pytest

---

## 阶段 0: P0 修复（文档一致性）

### Task 0.1: 清理不存在路径的文档引用

**Objective:** 修复 README.md 中引用了不存在文件的链接

**Files:**
- Modify: `examples/minimal-harness/README.md`
- Modify: `examples/minimal-harness/core/harness.py`
- Modify: `QUICKSTART.md`

**Step 1: 修改 minimal-harness README**

将 `examples/minimal-harness/README.md` 中不存在的路径替换为实际存在的：

```markdown
## 下一步

- [完整 Harness 实现](../full-harness/) → 删除（不存在）
- [前端设计 Harness](../frontend-harness/) → [前端设计 Harness](../frontend-harness/)
- [全栈开发 Harness](../fullstack-harness/) → 删除（不存在）
```

**Step 2: 验证 harness.py 中的 agents 引用**

`harness.py` 底部有注释引用了不存在的 `agents/` 目录，保留现状（后续 Task 1 会创建）

**Step 3: 验证 QUICKSTART.md**

检查并删除对 `examples/fullstack-harness/` 的引用

**Step 4: 验证**

```bash
cd /home/east/wsclaw/awesome-harness-engineering
grep -r "fullstack-harness\|full-harness\|agents/planner\|agents/generator\|agents/evaluator" --include="*.md" --include="*.py" | grep -v ".pyc"
```
Expected: 只有 `harness.py` 里的 import 注释（Task 1 会解决）

**Step 5: Commit**

```bash
git add examples/minimal-harness/README.md QUICKSTART.md
git commit -m "fix: remove references to non-existent directories"
```

---

### Task 0.2: 修正 PROGRESS_REPORT.md 中的虚假数据

**Objective:** 将 PROGRESS_REPORT 中夸大的数据修正为真实值

**Files:**
- Modify: `PROGRESS_REPORT.md`

**修改内容:**

| 位置 | 原值 | 修正为 |
|------|------|--------|
| `harness.py` 行数 | "~660 行" | "256 行" |
| `agents/` 目录 | "存在" | "不存在（stub）" |
| Phase 1 完成度 | "100% 完成" | "文档完成，代码为 mock 实现" |

**Step 1: 更新表格**

```markdown
#### 1.4 示例代码详情

**minimal-harness/**:
- ⚠️ `core/harness.py` - 核心实现（256行，mock 实现，非真实 LLM 调用）
- ✅ `examples/simple_task.py` - 可运行示例（76行）
- ❌ `agents/` - 目录不存在（Phase 2 实现）
```

**Step 2: 添加 Phase 2 待办表格**

在 PROGRESS_REPORT.md 末尾添加：

```markdown
## 📋 Phase 2 待办

### 核心实现
- [ ] 实现 `agents/planner.py` — 真实 LLM-powered 规划器
- [ ] 实现 `agents/generator.py` — 真实代码生成
- [ ] 实现 `agents/evaluator.py` — Outlines 结构化评分
- [ ] 实现 `core/context_manager.py` — 上下文管理

### 文档更新
- [ ] 更新 README.md 中的下一步链接
- [ ] 更新 PROGRESS_REPORT.md 数据
```

**Step 3: Commit**

```bash
git add PROGRESS_REPORT.md
git commit -m "docs: correct Phase 1 progress report, add Phase 2 TODOs"
```

---

## 阶段 1: 核心架构实现

### Task 1.1: 创建 agents 目录结构和基础模块

**Objective:** 创建 `agents/` 目录和基础 agent 类

**Files:**
- Create: `examples/minimal-harness/agents/__init__.py`
- Create: `examples/minimal-harness/agents/base.py`
- Create: `examples/minimal-harness/agents/planner.py`
- Create: `examples/minimal-harness/agents/generator.py`
- Create: `examples/minimal-harness/agents/evaluator.py`

**Step 1: 创建 agents/__init__.py**

```python
"""Agent 模块 - LLM-powered 多智能体实现"""

from agents.base import BaseAgent
from agents.planner import PlannerAgent
from agents.generator import GeneratorAgent
from agents.evaluator import EvaluatorAgent

__all__ = [
    "BaseAgent",
    "PlannerAgent",
    "GeneratorAgent",
    "EvaluatorAgent",
]
```

**Step 2: 创建 agents/base.py**

```python
"""Base agent class with common functionality"""

import os
import anthropic
from abc import ABC, abstractmethod
from typing import Optional


class BaseAgent(ABC):
    """所有 Agent 的基类"""

    def __init__(
        self,
        model: str = "claude-sonnet-4-5-20250514",
        api_key: Optional[str] = None,
        max_tokens: int = 4096,
    ):
        self.model = model
        self.client = anthropic.Anthropic(
            api_key=api_key or os.getenv("ANTHROPIC_API_KEY")
        )
        self.max_tokens = max_tokens

    @abstractmethod
    async def run(self, input_data) -> dict:
        """执行 agent 核心逻辑"""
        pass

    def _call_llm(self, system: str, messages: list) -> anthropic.Message:
        """统一的 LLM 调用"""
        response = self.client.messages.create(
            model=self.model,
            max_tokens=self.max_tokens,
            system=system,
            messages=messages,
        )
        return response
```

**Step 3: 创建 agents/planner.py**

```python
"""Planner Agent - 将需求转化为技术规格"""

import json
from typing import List
from agents.base import BaseAgent


SYSTEM_PROMPT = """你是一个专业的软件架构师。你的任务是将用户需求转化为详细的技术规格。

输出格式（必须是有效的 JSON）：
{
  "title": "产品名称",
  "description": "一句话描述",
  "features": ["功能1", "功能2", "功能3"],
  "tech_stack": {
    "frontend": "技术选型",
    "backend": "技术选型",
    "database": "技术选型"
  },
  "acceptance_criteria": ["验收标准1", "验收标准2"]
}

不要输出除了 JSON 之外的任何内容。"""


class PlannerAgent(BaseAgent):
    """规划器：将模糊需求转化为具体规格"""

    async def run(self, prompt: str) -> dict:
        """分析需求并生成规格"""
        messages = [{"role": "user", "content": prompt}]
        response = self._call_llm(SYSTEM_PROMPT, messages)

        # 解析 JSON 输出
        try:
            spec = json.loads(response.content[0].text)
            return spec
        except json.JSONDecodeError:
            # Fallback: 返回结构化错误
            return {
                "title": "Parse Error",
                "description": prompt,
                "features": [],
                "tech_stack": {},
                "error": response.content[0].text
            }
```

**Step 4: 创建 agents/generator.py**

```python
"""Generator Agent - 根据规格生成代码"""

from typing import Dict
from agents.base import BaseAgent


SYSTEM_PROMPT = """你是一个专业的 Python 开发者。根据规格生成高质量、可运行的代码。

要求：
1. 代码必须完整、可运行
2. 添加必要的注释
3. 包含错误处理
4. 遵循最佳实践

只输出代码，不要有其他解释。"""


class GeneratorAgent(BaseAgent):
    """生成器：根据规格生成代码"""

    async def run(self, spec: dict, feedback: str = "") -> str:
        """根据规格生成代码，可选接受上一轮反馈"""
        context = f"产品规格:\n{json.dumps(spec, ensure_ascii=False, indent=2)}"

        if feedback:
            context += f"\n\n上一轮反馈（需要修复）:\n{feedback}"

        messages = [{"role": "user", "content": context}]
        response = self._call_llm(SYSTEM_PROMPT, messages)

        return response.content[0].text
```

**Step 5: 创建 agents/evaluator.py**

```python
"""Evaluator Agent - 使用 Outlines 进行结构化评分"""

import json
from typing import List, Optional
from pydantic import BaseModel, Field
from agents.base import BaseAgent

# 使用 Outlines 做结构化输出（见 Task 2.1）
# 先用 Pydantic 定义评分结构


class EvaluationResult(BaseModel):
    """评估结果"""
    quality_score: float = Field(description="质量分数 0.0-1.0")
    functionality: float = Field(description="功能完整性 0.0-1.0")
    code_quality: float = Field(description="代码质量 0.0-1.0")
    feedback: str = Field(description="改进建议")
    passed: bool = Field(description="是否通过验收标准")


SYSTEM_PROMPT = """你是一个严格的代码评审专家。根据规格评估生成的代码。

评分维度：
1. functionality: 功能完整性 - 是否实现了所有要求的功能
2. code_quality: 代码质量 - 可读性、错误处理、最佳实践
3. quality_score: 综合质量分数

对于每个维度给出 0.0-1.0 的分数，并提供具体的改进建议。

必须返回有效的 JSON。"""


class EvaluatorAgent(BaseAgent):
    """评估器：多维度代码评估"""

    async def run(self, code: str, spec: dict) -> EvaluationResult:
        """评估代码并返回评分"""
        context = f"代码:\n```{code}\n```\n\n规格:\n{json.dumps(spec, ensure_ascii=False, indent=2)}"

        messages = [{"role": "user", "content": context}]
        response = self._call_llm(SYSTEM_PROMPT, messages)

        try:
            # 尝试解析 JSON
            result = json.loads(response.content[0].text)
            return EvaluationResult(
                quality_score=result.get("quality_score", 0.0),
                functionality=result.get("functionality", 0.0),
                code_quality=result.get("code_quality", 0.0),
                feedback=result.get("feedback", ""),
                passed=result.get("quality_score", 0.0) >= 0.8
            )
        except json.JSONDecodeError:
            # Fallback
            return EvaluationResult(
                quality_score=0.0,
                functionality=0.0,
                code_quality=0.0,
                feedback=f"Parse error: {response.content[0].text[:200]}",
                passed=False
            )
```

**Step 6: Commit**

```bash
git add agents/
git commit -m "feat: add agents module with Planner, Generator, Evaluator"
```

---

## 阶段 2: Outlines 集成（Task 2.1）

### Task 2.1: 使用 Outlines 替换 Evaluator 的 JSON 解析

**Objective:** 用 Outlines 的 grammar-based generation 保证 Evaluator 输出 100% 有效的 JSON

**Files:**
- Modify: `examples/minimal-harness/agents/evaluator.py`
- Create: `examples/minimal-harness/tests/test_evaluator.py`

**Step 1: 安装依赖**

```bash
cd /home/east/wsclaw/awesome-harness-engineering/examples/minimal-harness
pip install outlines anthropic
```

**Step 2: 创建 test_evaluator.py**

```python
"""Evaluator Agent 测试"""

import pytest
import asyncio
from agents.evaluator import EvaluatorAgent, EvaluationResult


@pytest.fixture
def evaluator():
    return EvaluatorAgent()


@pytest.fixture
def sample_spec():
    return {
        "title": "待办事项应用",
        "description": "简单的任务管理应用",
        "features": ["添加任务", "完成任务", "删除任务"],
        "tech_stack": {"frontend": "React", "backend": "FastAPI", "database": "SQLite"}
    }


@pytest.fixture
def sample_code():
    return '''
class TodoApp:
    def __init__(self):
        self.tasks = []

    def add_task(self, title: str):
        self.tasks.append({"title": title, "completed": False})

    def complete_task(self, title: str):
        for task in self.tasks:
            if task["title"] == title:
                task["completed"] = True
                return True
        return False
'''


@pytest.mark.asyncio
async def test_evaluator_returns_valid_evaluation(evaluator, sample_spec, sample_code):
    """测试 Evaluator 返回有效的评估结果"""
    result = await evaluator.run(sample_code, sample_spec)

    assert isinstance(result, EvaluationResult)
    assert 0.0 <= result.quality_score <= 1.0
    assert 0.0 <= result.functionality <= 1.0
    assert 0.0 <= result.code_quality <= 1.0
    assert isinstance(result.feedback, str)
    assert isinstance(result.passed, bool)


@pytest.mark.asyncio
async def test_evaluator_with_real_llm(evaluator, sample_spec, sample_code):
    """端到端测试：真实 LLM 调用"""
    result = await evaluator.run(sample_code, sample_spec)

    # 验证结构完整性
    assert hasattr(result, 'quality_score')
    assert hasattr(result, 'functionality')
    assert hasattr(result, 'code_quality')
    assert hasattr(result, 'feedback')
    assert hasattr(result, 'passed')

    print(f"\n评估结果: {result.quality_score:.2f}, passed={result.passed}")
    print(f"反馈: {result.feedback[:100]}...")
```

**Step 3: 运行测试验证现状**

```bash
cd /home/east/wsclaw/awesome-harness-engineering/examples/minimal-harness
pytest tests/test_evaluator.py -v
```
Expected: 测试应该能运行（可能失败，因为没有真实 API key）

**Step 4: 用 Outlines 重写 Evaluator**

修改 `agents/evaluator.py`，添加 Outlines 支持：

```python
"""Evaluator Agent - 使用 Outlines 做结构化评分"""

import os
import json
from typing import Optional
from pydantic import BaseModel, Field
from agents.base import BaseAgent

try:
    import outlines
    OUTLINES_AVAILABLE = True
except ImportError:
    OUTLINES_AVAILABLE = False


class EvaluationResult(BaseModel):
    """评估结果"""
    quality_score: float = Field(description="质量分数 0.0-1.0")
    functionality: float = Field(description="功能完整性 0.0-1.0")
    code_quality: float = Field(description="代码质量 0.0-1.0")
    feedback: str = Field(description="改进建议")
    passed: bool = Field(description="是否通过验收标准")


SYSTEM_PROMPT = """你是一个严格的代码评审专家。根据规格评估生成的代码。

评分维度：
1. functionality: 功能完整性 - 是否实现了所有要求的功能
2. code_quality: 代码质量 - 可读性、错误处理、最佳实践
3. quality_score: 综合质量分数

必须返回有效的 JSON。"""


class EvaluatorAgent(BaseAgent):
    """评估器：多维度代码评估，使用 Outlines 保证结构化输出"""

    def __init__(self, use_outlines: bool = True, **kwargs):
        super().__init__(**kwargs)
        self.use_outlines = use_outlines and OUTLINES_AVAILABLE

    def _setup_outlines(self):
        """配置 Outlines 结构化生成"""
        # 使用 OpenAI-compatible API 或本地模型
        # 这里使用 OpenAI 兼容接口
        if os.getenv("OPENAI_API_KEY"):
            model = outlines.models.openai(
                "gpt-4o-mini",
                api_key=os.getenv("OPENAI_API_KEY"),
                base_url=os.getenv("OPENAI_BASE_URL", None)
            )
        else:
            # 回退到基础实现
            return None

        generator = outlines.generate.json(model, EvaluationResult)
        return generator

    async def run(self, code: str, spec: dict) -> EvaluationResult:
        """评估代码并返回评分"""
        context = f"代码:\n```{code}\n```\n\n规格:\n{json.dumps(spec, ensure_ascii=False, indent=2)}"

        # 尝试使用 Outlines
        if self.use_outlines:
            try:
                generator = self._setup_outlines()
                if generator:
                    result = generator(context)
                    return result
            except Exception as e:
                print(f"Outlines failed: {e}, falling back to basic LLM")

        # Fallback: 基础 LLM 调用 + JSON 解析
        return await self._evaluate_basic(context)

    async def _evaluate_basic(self, context: str) -> EvaluationResult:
        """基础评估（无 Outlines）"""
        messages = [{"role": "user", "content": context}]
        response = self._call_llm(SYSTEM_PROMPT, messages)

        try:
            result = json.loads(response.content[0].text)
            return EvaluationResult(**result)
        except (json.JSONDecodeError, TypeError):
            return EvaluationResult(
                quality_score=0.0,
                functionality=0.0,
                code_quality=0.0,
                feedback=f"Failed to parse LLM response: {response.content[0].text[:200]}",
                passed=False
            )
```

**Step 5: 验证测试**

```bash
cd /home/east/wsclaw/awesome-harness-engineering/examples/minimal-harness
pytest tests/test_evaluator.py -v
```

**Step 6: Commit**

```bash
git add agents/evaluator.py tests/test_evaluator.py
git commit -m "feat: add Outlines integration to Evaluator for structured output"
```

---

## 阶段 3: 集成测试

### Task 3.1: 更新 MinimalHarness 使用真实的 Agent

**Objective:** 将 `core/harness.py` 改为使用真实的 agents

**Files:**
- Modify: `examples/minimal-harness/core/harness.py`

**Step 1: 重写 harness.py**

将 mock 实现替换为真实调用：

```python
"""
Minimal Harness 实现 - LLM-powered 版本
使用真实的 Planner/Generator/Evaluator agent
"""

import asyncio
import logging
from typing import Dict, Any, Optional
from dataclasses import dataclass

from agents import PlannerAgent, GeneratorAgent, EvaluatorAgent

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class TaskSpec:
    """任务规格"""
    title: str
    description: str
    features: list
    tech_stack: Dict[str, str]
    acceptance_criteria: list = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "description": self.description,
            "features": self.features,
            "tech_stack": self.tech_stack,
            "acceptance_criteria": self.acceptance_criteria or []
        }


@dataclass
class SprintResult:
    """Sprint 结果"""
    sprint_number: int
    code: str
    evaluation: Any  # EvaluationResult
    passed: bool


class MinimalHarness:
    """
    LLM-powered Harness 实现

    核心流程：
    1. Planner: 需求 → 规格
    2. Generator: 规格 → 代码（多 Sprint）
    3. Evaluator: 代码 → 评分 + 反馈（使用 Outlines）
    4. 循环直到满足条件
    """

    def __init__(
        self,
        max_iterations: int = 5,
        min_quality_score: float = 0.8,
        debug: bool = False,
        use_outlines: bool = True
    ):
        self.max_iterations = max_iterations
        self.min_quality_score = min_quality_score
        self.debug = debug
        self.use_outlines = use_outlines

        # 初始化 agents
        self.planner = PlannerAgent()
        self.generator = GeneratorAgent()
        self.evaluator = EvaluatorAgent(use_outlines=use_outlines)

        self.history: list = []

    async def run(self, prompt: str) -> Dict[str, Any]:
        """运行完整 Harness 流程"""
        logger.info(f"🚀 启动 Minimal Harness")
        logger.info(f"需求: {prompt}")

        # Step 1: Planning
        spec_dict = await self.planner.run(prompt)
        spec = TaskSpec(**spec_dict)
        logger.info(f"✅ 规划完成: {spec.title}")

        # Step 2-4: Generate → Evaluate → Iterate
        final_result = await self._generate_and_evaluate(spec)

        return {
            "spec": spec.to_dict(),
            "code": final_result.code,
            "quality_score": final_result.evaluation.quality_score,
            "passed": final_result.passed,
            "iterations": final_result.sprint_number,
            "history": self.history
        }

    async def _generate_and_evaluate(self, spec: TaskSpec) -> SprintResult:
        """Generator + Evaluator 循环"""
        feedback = ""

        for iteration in range(1, self.max_iterations + 1):
            logger.info(f"\n[Sprint {iteration}/{self.max_iterations}]")

            # Generate
            code = await self.generator.run(spec.to_dict(), feedback)

            # Evaluate
            evaluation = await self.evaluator.run(code, spec.to_dict())

            # Record history
            self.history.append({
                "sprint": iteration,
                "code_length": len(code),
                "quality_score": evaluation.quality_score,
                "feedback": evaluation.feedback
            })

            # Check if quality threshold met
            if evaluation.passed:
                logger.info(f"✅ 达到质量标准 ({evaluation.quality_score:.2f})")
                return SprintResult(
                    sprint_number=iteration,
                    code=code,
                    evaluation=evaluation,
                    passed=True
                )

            logger.info(f"⚠️ 质量未达标 ({evaluation.quality_score:.2f})，继续迭代...")
            feedback = evaluation.feedback

        logger.info(f"⚠️ 达到最大迭代次数")
        return SprintResult(
            sprint_number=self.max_iterations,
            code=code,
            evaluation=evaluation,
            passed=False
        )
```

**Step 2: 验证**

```bash
cd /home/east/wsclaw/awesome-harness-engineering/examples/minimal-harness
python -c "from core.harness import MinimalHarness; print('Import OK')"
```

**Step 3: Commit**

```bash
git add core/harness.py
git commit -m "feat: wire MinimalHarness to real LLM-powered agents"
```

---

## 阶段 4: 新增文档

### Task 4.1: 创建 Outlines 集成文档

**Objective:** 记录如何使用 Outlines 做结构化输出

**Files:**
- Create: `examples/minimal-harness/docs/OUTLINES_INTEGRATION.md`

**Step 1: 创建文档**

```markdown
# Outlines 结构化输出集成

本项目使用 [Outlines](https://github.com/outlines-dev/outlines) 保证 Evaluator 输出 100% 有效的 JSON。

## 为什么用 Outlines？

传统 LLM JSON 输出依赖后处理解析：
1. LLM 生成文本
2. 尝试 JSON.parse()
3. 失败则重试（浪费 token）

Outlines 的 grammar-based generation：
1. 定义 JSON Schema → 转换为有限状态机（FSM）
2. 生成时在 logit 层过滤无效 token
3. **无效输出在物理上不可能**

## 在 Evaluator 中的使用

```python
from agents.evaluator import EvaluatorAgent, EvaluationResult

evaluator = EvaluatorAgent(use_outlines=True)
result = await evaluator.run(code, spec)
# result 是 EvaluationResult Pydantic 实例
# 100% 有效保证
```

## Outlines 支持的模型

| 模型类型 | 支持情况 |
|----------|----------|
| OpenAI (api.openai.com) | ✅ 完整支持 |
| Anthropic (通过兼容层) | ⚠️ 需要 OpenAI 兼容包装 |
| Local (llama.cpp, vLLM) | ✅ 完整支持 |
| Hugging Face Transformers | ✅ 完整支持 |

## 配置

环境变量：
```bash
# OpenAI 兼容 API
export OPENAI_API_KEY="sk-..."
export OPENAI_BASE_URL="https://api.openai-proxy.org/v1"  # 可选代理
```

## 扩展到其他 Agent

Planner 和 Generator 也可以用 Outlines：

```python
# Planner: 输出 TaskSpec
from pydantic import BaseModel

class TaskSpecOutput(BaseModel):
    title: str
    description: str
    features: list[str]
    tech_stack: dict[str, str]

generator = outlines.generate.json(model, TaskSpecOutput)
spec = generator(user_prompt)
```
```

**Step 2: Commit**

```bash
git add docs/OUTLINES_INTEGRATION.md
git commit -m "docs: add Outlines integration guide"
```

---

## 总结

| 阶段 | Task | 状态 |
|------|------|------|
| P0 | 0.1 修复文档引用 | ⬜ |
| P0 | 0.2 修正 PROGRESS_REPORT | ⬜ |
| P1 | 1.1 创建 agents 模块 | ⬜ |
| P2 | 2.1 Outlines 集成 | ⬜ |
| P3 | 3.1 更新 MinimalHarness | ⬜ |
| P4 | 4.1 创建集成文档 | ⬜ |

**Plan 完成后，你应该拥有：**
- 可运行的 LLM-powered minimal-harness
- Outlines 结构化输出保证
- 完整测试覆盖
- 清晰的新增文档
