"""GeneratorAgent: Generates code from TaskSpec."""
from typing import Optional

from agents.base import BaseAgent


class GeneratorAgent(BaseAgent):
    """Agent that generates code from a TaskSpec specification.
    
    The GeneratorAgent takes a TaskSpec dictionary (and optional feedback)
    and generates code that fulfills the specification.
    """
    
    def __init__(self):
        """Initialize the GeneratorAgent."""
        super().__init__()
        self.system_prompt = (
            "You are a code generation agent. Your job is to write code "
            "that fulfills the given task specification.\n\n"
            "Given a TaskSpec JSON object, generate clean, well-documented code "
            "that meets all the requirements. Output only the code, no explanations."
        )
    
    def generate(self, spec: dict, feedback: Optional[str] = None) -> str:
        """Generate code from a TaskSpec.
        
        Args:
            spec: A TaskSpec dictionary containing task details.
            feedback: Optional feedback from previous evaluation attempts.
            
        Returns:
            A string containing the generated code.
        """
        spec_str = str(spec)
        
        if feedback:
            prompt = (
                f"TaskSpec: {spec_str}\n\n"
                f"Previous feedback to address:\n{feedback}\n\n"
                "Generate improved code based on the feedback."
            )
        else:
            prompt = f"TaskSpec: {spec_str}\n\nGenerate the code for this task."
        
        messages = [{"role": "user", "content": prompt}]
        response = self.call_llm(system=self.system_prompt, messages=messages)
        return response
