"""EvaluatorAgent: Evaluates code against TaskSpec using structured output."""
import json

from pydantic import BaseModel

from agents.base import BaseAgent


class EvaluationResult(BaseModel):
    """Structured evaluation result for code against a TaskSpec.
    
    Attributes:
        quality_score: Overall quality score between 0.0 and 1.0.
        functionality: Assessment of whether the code fulfills the task.
        code_quality: Assessment of code quality (readability, structure, etc.).
        feedback: Constructive feedback for improvement.
        passed: Whether the code meets the acceptance criteria.
    """
    
    quality_score: float
    functionality: float
    code_quality: float
    feedback: str
    passed: bool


class EvaluatorAgent(BaseAgent):
    """Agent that evaluates code against a TaskSpec specification.
    
    The EvaluatorAgent takes generated code and a TaskSpec, then uses
    structured output (Pydantic model) to return a detailed evaluation.
    """
    
    def __init__(self):
        """Initialize the EvaluatorAgent."""
        super().__init__()
        self.system_prompt = (
            "You are a code evaluation agent. Your job is to assess generated code "
            "against a task specification and provide detailed feedback.\n\n"
            "Evaluate the code on:\n"
            "1. Functionality - Does it fulfill the task requirements?\n"
            "2. Code Quality - Is it clean, readable, and well-structured?\n"
            "3. Completeness - Does it meet all acceptance criteria?\n\n"
            "IMPORTANT: You must respond with valid JSON only. The JSON must include:\n"
            "- quality_score: A float between 0.0 and 1.0\n"
            "- functionality: A float between 0.0 and 1.0\n"
            "- code_quality: A float between 0.0 and 1.0\n"
            "- feedback: A string with constructive feedback\n"
            "- passed: A boolean indicating if the code meets criteria\n\n"
            "Respond with JSON only."
        )
    
    def evaluate(self, code: str, spec: dict) -> EvaluationResult:
        """Evaluate code against a TaskSpec.
        
        Args:
            code: The generated code to evaluate.
            spec: The TaskSpec dictionary to evaluate against.
            
        Returns:
            An EvaluationResult instance with structured evaluation data.
        """
        spec_str = str(spec)
        
        prompt = (
            f"TaskSpec:\n{spec_str}\n\n"
            f"Code to evaluate:\n```\n{code}\n```\n\n"
            "Evaluate this code against the TaskSpec and respond with JSON."
        )
        
        messages = [{"role": "user", "content": prompt}]
        response = self.call_llm(system=self.system_prompt, messages=messages)
        
        # Parse JSON response
        try:
            result_dict = json.loads(response)
        except json.JSONDecodeError:
            # Try to extract JSON from the text
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end != 0:
                result_dict = json.loads(response[json_start:json_end])
            else:
                # Return a failure result if we can't parse
                return EvaluationResult(
                    quality_score=0.0,
                    functionality=0.0,
                    code_quality=0.0,
                    feedback=f"Could not parse response: {response[:200]}",
                    passed=False
                )
        
        return EvaluationResult(**result_dict)
