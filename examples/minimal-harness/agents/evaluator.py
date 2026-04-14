"""EvaluatorAgent: Evaluates code against TaskSpec using structured output."""
import json
import os
from typing import Optional

from pydantic import BaseModel

from agents.base import BaseAgent

# Outlines is optional - graceful degradation if not available
try:
    import outlines
    from openai import OpenAI
    OUTLINES_AVAILABLE = True
except ImportError:
    OUTLINES_AVAILABLE = False


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
    
    Supports two modes:
    - use_outlines=True (default): Uses Outlines for guaranteed valid JSON output
    - use_outlines=False: Uses basic LLM call with JSON parsing fallback
    """
    
    def __init__(self, use_outlines: bool = True):
        """Initialize the EvaluatorAgent.
        
        Args:
            use_outlines: Whether to use Outlines for structured JSON output.
                         Defaults to True. If Outlines is not available, falls back
                         to basic LLM call regardless of this setting.
        """
        super().__init__()
        self.use_outlines = use_outlines and OUTLINES_AVAILABLE
        self._outlines_client: Optional[OpenAI] = None
        self._outlines_model: Optional[str] = None
        
        if self.use_outlines:
            self._setup_outlines()
        
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
    
    def _setup_outlines(self) -> None:
        """Configure Outlines for structured JSON generation.
        
        Sets up an OpenAI-compatible client using environment variables:
        - OPENAI_API_KEY: API key for the OpenAI-compatible endpoint
        - OPENAI_BASE_URL: Base URL for the OpenAI-compatible endpoint
        """
        if not OUTLINES_AVAILABLE:
            return
        
        api_key = os.environ.get("OPENAI_API_KEY")
        base_url = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
        
        if not api_key:
            print("Warning: OPENAI_API_KEY not set, Outlines will not be used")
            self.use_outlines = False
            return
        
        try:
            self._outlines_client = OpenAI(api_key=api_key, base_url=base_url)
            # Use a capable model for structured output
            self._outlines_model = os.environ.get("OUTLINES_MODEL", "gpt-4o")
        except Exception as e:
            print(f"Warning: Failed to setup Outlines client: {e}")
            self.use_outlines = False
    
    def evaluate(self, code: str, spec: dict) -> EvaluationResult:
        """Evaluate code against a TaskSpec.
        
        Args:
            code: The generated code to evaluate.
            spec: The TaskSpec dictionary to evaluate against.
            
        Returns:
            An EvaluationResult instance with structured evaluation data.
            
        Note:
            When use_outlines=True (default), this method uses Outlines for
            guaranteed valid JSON output. If Outlines fails or is not available,
            falls back to basic LLM call with JSON parsing.
        """
        spec_str = str(spec)
        
        prompt = (
            f"TaskSpec:\n{spec_str}\n\n"
            f"Code to evaluate:\n```\n{code}\n```\n\n"
            "Evaluate this code against the TaskSpec and respond with JSON."
        )
        
        # Try Outlines first for guaranteed valid JSON
        if self.use_outlines and self._outlines_client:
            try:
                return self._evaluate_with_outlines(prompt)
            except Exception as e:
                print(f"Warning: Outlines evaluation failed, falling back to basic LLM: {e}")
        
        # Fall back to basic LLM call with JSON parsing
        return self._evaluate_with_basic_llm(prompt)
    
    def _evaluate_with_outlines(self, prompt: str) -> EvaluationResult:
        """Evaluate using Outlines for guaranteed valid JSON output.
        
        Args:
            prompt: The evaluation prompt.
            
        Returns:
            An EvaluationResult instance with structured evaluation data.
        """
        if not self._outlines_client or not self._outlines_model:
            raise RuntimeError("Outlines client not initialized")
        
        # Create a generator that produces JSON conforming to EvaluationResult
        generator = outlines.generate.json(
            self._outlines_client,
            EvaluationResult,
            model=self._outlines_model
        )
        
        # Generate the response with Outlines
        response = generator(prompt)
        
        return EvaluationResult(**response)
    
    def _evaluate_with_basic_llm(self, prompt: str) -> EvaluationResult:
        """Evaluate using basic LLM call with JSON parsing fallback.
        
        Args:
            prompt: The evaluation prompt.
            
        Returns:
            An EvaluationResult instance with structured evaluation data.
        """
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
