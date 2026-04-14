"""
Minimal Harness 实现 - LLM-powered 版本
使用真实的 Planner/Generator/Evaluator Agent
"""

import asyncio
import logging
from typing import Dict, Any, Optional
from dataclasses import dataclass, field

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
    acceptance_criteria: list = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "description": self.description,
            "features": self.features,
            "tech_stack": self.tech_stack,
            "acceptance_criteria": self.acceptance_criteria
        }


class MinimalHarness:
    """
    LLM-powered Harness 实现

    核心流程：
    1. Planner: 需求 → 规格（调用 PlannerAgent）
    2. Generator: 规格 → 代码（调用 GeneratorAgent）
    3. Evaluator: 代码 → 评分（调用 EvaluatorAgent）
    4. 循环直到满足条件或达到最大迭代次数
    """

    def __init__(
        self,
        max_iterations: int = 5,
        min_quality_score: float = 0.8,
        debug: bool = False,
        use_outlines: bool = True
    ):
        """初始化 Harness。

        Args:
            max_iterations: 最大迭代次数
            min_quality_score: 通过质量分数阈值
            debug: 是否开启调试日志
            use_outlines: Evaluator 是否使用 Outlines（结构化输出）
        """
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
        """运行完整 Harness 流程。

        Args:
            prompt: 用户输入的需求描述

        Returns:
            包含最终代码、评估结果、历史记录的字典
        """
        logger.info(f"🚀 启动 Minimal Harness")
        logger.info(f"需求: {prompt}")

        # Step 1: Planning
        spec_dict = self.planner.plan(prompt)
        spec = TaskSpec(**spec_dict)
        logger.info(f"✅ 规划完成: {spec.title}")

        # Step 2-4: Generate → Evaluate → Iterate
        final_result = self._generate_and_evaluate(spec)

        return {
            "spec": spec.to_dict(),
            "code": final_result["code"],
            "quality_score": final_result["evaluation"].quality_score,
            "passed": final_result["evaluation"].passed,
            "iterations": final_result["iterations"],
            "history": self.history
        }

    async def _plan(self, prompt: str) -> dict:
        """Planner: 将需求转化为规格"""
        logger.info("[Planner] 分析需求...")

        spec_dict = await self.planner.plan(prompt)

        await asyncio.sleep(0.1)  # 小延迟避免日志混乱
        return spec_dict

    def _generate_and_evaluate(self, spec: TaskSpec) -> dict:
        """Generator + Evaluator 循环"""
        feedback = ""

        for iteration in range(1, self.max_iterations + 1):
            logger.info(f"\n[Sprint {iteration}/{self.max_iterations}]")

            # Generate
            code = await self._generate(spec, feedback)

            # Evaluate
            evaluation = await self._evaluate(code, spec)

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
                return {
                    "code": code,
                    "evaluation": evaluation,
                    "iterations": iteration
                }

            logger.info(f"⚠️ 质量未达标 ({evaluation.quality_score:.2f})，继续迭代...")
            feedback = evaluation.feedback

        logger.info(f"⚠️ 达到最大迭代次数")
        return {
            "code": code,
            "evaluation": evaluation,
            "iterations": self.max_iterations
        }

    def _generate(self, spec: TaskSpec, feedback: str) -> str:
        """Generator: 生成代码"""
        logger.info(f"[Generator] 生成代码...")

        code = self.generator.generate(spec.to_dict(), feedback)

        logger.info(f"✅ 代码生成完成 ({len(code)} 字符)")
        return code

    def _evaluate(self, code: str, spec: TaskSpec) -> Any:
        """Evaluator: 评估代码质量"""
        logger.info(f"[Evaluator] 评估代码...")

        evaluation = self.evaluator.evaluate(code, spec.to_dict())

        logger.info(f"✅ 评估完成: {evaluation.quality_score:.2f}")
        if self.debug:
            logger.debug(f"反馈: {evaluation.feedback}")

        return evaluation


# 使用示例
async def main():
    """运行示例"""
    harness = MinimalHarness(
        max_iterations=5,
        min_quality_score=0.8,
        debug=True,
        use_outlines=True
    )

    result = await harness.run("创建一个待办事项应用")

    print("\n" + "="*50)
    print("🎉 Harness 执行完成!")
    print("="*50)
    print(f"📋 规格: {result['spec']['title']}")
    print(f"⭐ 质量分数: {result['quality_score']:.2f}")
    print(f"🔄 迭代次数: {result['iterations']}")
    print(f"📝 代码长度: {len(result['code'])} 字符")
    print("="*50)


if __name__ == "__main__":
    asyncio.run(main())
