"""Agents module for minimal-harness example.

This module provides agents for the harness engineering system:
- BaseAgent: Base class with LLM calling functionality
- PlannerAgent: Converts user prompts to TaskSpec JSON
- GeneratorAgent: Generates code from specifications
- EvaluatorAgent: Evaluates code against specifications
"""

from agents.base import BaseAgent
from agents.planner import PlannerAgent
from agents.generator import GeneratorAgent
from agents.evaluator import EvaluatorAgent, EvaluationResult

__all__ = [
    "BaseAgent",
    "PlannerAgent",
    "GeneratorAgent",
    "EvaluatorAgent",
    "EvaluationResult",
]
