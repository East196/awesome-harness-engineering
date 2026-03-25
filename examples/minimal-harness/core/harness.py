"""
最小可运行的 Harness 实现
演示多智能体协作的核心逻辑
"""

import asyncio
import logging
from typing import Dict, Any, Optional
from dataclasses import dataclass

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@dataclass
class TaskSpec:
    """任务规格"""
    title: str
    description: str
    features: list
    tech_stack: Dict[str, str]
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "title": self.title,
            "description": self.description,
            "features": self.features,
            "tech_stack": self.tech_stack
        }


@dataclass
class SprintResult:
    """Sprint 结果"""
    sprint_number: int
    code: str
    tests_passed: bool
    quality_score: float
    feedback: str


class MinimalHarness:
    """
    最简化的 Harness 实现
    
    核心流程：
    1. Planner: 需求 → 规格
    2. Generator: 规格 → 代码（多 Sprint）
    3. Evaluator: 代码 → 评分 + 反馈
    4. 循环直到满足条件
    """
    
    def __init__(
        self,
        max_iterations: int = 5,
        min_quality_score: float = 0.8,
        debug: bool = False
    ):
        self.max_iterations = max_iterations
        self.min_quality_score = min_quality_score
        self.debug = debug
        self.history: list = []
        
    async def run(self, prompt: str) -> Dict[str, Any]:
        """
        运行完整 Harness 流程
        
        Args:
            prompt: 用户输入的需求描述
            
        Returns:
            包含最终代码、评估结果、历史记录的字典
        """
        logger.info(f"🚀 启动 Minimal Harness")
        logger.info(f"需求: {prompt}")
        
        # Step 1: Planning
        spec = await self._plan(prompt)
        logger.info(f"✅ 规划完成: {spec.title}")
        
        # Step 2-4: Generate → Evaluate → Iterate
        final_result = await self._generate_and_evaluate(spec)
        
        return {
            "spec": spec.to_dict(),
            "code": final_result.code,
            "quality_score": final_result.quality_score,
            "iterations": final_result.sprint_number,
            "history": self.history
        }
    
    async def _plan(self, prompt: str) -> TaskSpec:
        """Planner: 将需求转化为规格"""
        logger.info("[Planner] 分析需求...")
        
        # 模拟 Planner 的输出
        # 实际实现中，这里会调用 LLM
        spec = TaskSpec(
            title="待办事项应用",
            description=prompt,
            features=[
                "创建任务",
                "标记完成",
                "删除任务",
                "任务优先级"
            ],
            tech_stack={
                "frontend": "React",
                "backend": "FastAPI",
                "database": "SQLite"
            }
        )
        
        await asyncio.sleep(0.5)  # 模拟处理时间
        return spec
    
    async def _generate_and_evaluate(self, spec: TaskSpec) -> SprintResult:
        """Generator + Evaluator 循环"""
        
        for iteration in range(1, self.max_iterations + 1):
            logger.info(f"\n[Sprint {iteration}/{self.max_iterations}]")
            
            # Generate
            code = await self._generate(spec, iteration)
            
            # Evaluate
            result = await self._evaluate(code, spec, iteration)
            
            # Record history
            self.history.append({
                "sprint": iteration,
                "code_length": len(code),
                "quality_score": result.quality_score,
                "feedback": result.feedback
            })
            
            # Check if quality threshold met
            if result.quality_score >= self.min_quality_score:
                logger.info(f"✅ 达到质量标准 ({result.quality_score:.2f})")
                return result
            
            logger.info(f"⚠️  质量未达标 ({result.quality_score:.2f})，继续迭代...")
        
        logger.info(f"⚠️  达到最大迭代次数")
        return result
    
    async def _generate(self, spec: TaskSpec, sprint: int) -> str:
        """Generator: 生成代码"""
        logger.info(f"[Generator] 生成代码...")
        
        # 模拟代码生成
        # 实际实现中，这里会调用 LLM 生成真实代码
        code = f"""
# Sprint {sprint} 生成的代码
# {spec.title}

class TodoApp:
    def __init__(self):
        self.tasks = []
    
    def add_task(self, title: str, priority: str = "medium"):
        \"\"\"添加任务\"\"\"
        task = {{
            "id": len(self.tasks) + 1,
            "title": title,
            "priority": priority,
            "completed": False
        }}
        self.tasks.append(task)
        return task
    
    def complete_task(self, task_id: int):
        \"\"\"标记任务完成\"\"\"
        for task in self.tasks:
            if task["id"] == task_id:
                task["completed"] = True
                return task
        return None
    
    def delete_task(self, task_id: int):
        \"\"\"删除任务\"\"\"
        self.tasks = [t for t in self.tasks if t["id"] != task_id]

# 当前 Sprint: {sprint}
"""
        
        await asyncio.sleep(1.0)  # 模拟生成时间
        logger.info(f"✅ 代码生成完成 ({len(code)} 字符)")
        return code
    
    async def _evaluate(
        self,
        code: str,
        spec: TaskSpec,
        sprint: int
    ) -> SprintResult:
        """Evaluator: 评估代码质量"""
        logger.info(f"[Evaluator] 评估代码...")
        
        # 模拟评估逻辑
        # 实际实现中，这里会调用 LLM 进行多维度评估
        
        # 模拟质量分数随迭代提升
        base_score = 0.5
        improvement = sprint * 0.1
        quality_score = min(base_score + improvement, 0.95)
        
        # 模拟反馈
        if quality_score < self.min_quality_score:
            feedback = f"需要改进：\n" \
                      f"- 代码结构可以优化\n" \
                      f"- 缺少错误处理\n" \
                      f"- 建议添加更多功能"
        else:
            feedback = "代码质量良好，满足要求"
        
        await asyncio.sleep(0.5)  # 模拟评估时间
        
        result = SprintResult(
            sprint_number=sprint,
            code=code,
            tests_passed=quality_score > 0.7,
            quality_score=quality_score,
            feedback=feedback
        )
        
        logger.info(f"✅ 评估完成: {quality_score:.2f}")
        if self.debug:
            logger.debug(f"反馈: {feedback}")
        
        return result


# 使用示例
async def main():
    """运行示例"""
    harness = MinimalHarness(
        max_iterations=5,
        min_quality_score=0.8,
        debug=True
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
