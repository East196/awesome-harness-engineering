"""PlannerAgent: Converts user prompt to TaskSpec JSON."""
import json

from agents.base import BaseAgent


class PlannerAgent(BaseAgent):
    """Agent that converts user prompts into structured TaskSpec JSON.
    
    The PlannerAgent takes a natural language description of a task and
    generates a JSON specification that defines the task structure,
    requirements, and expected behavior.
    """
    
    def __init__(self):
        """Initialize the PlannerAgent."""
        super().__init__()
        self.system_prompt = (
            "You are a task planning agent. Your job is to analyze user requests "
            "and convert them into structured JSON task specifications.\n\n"
            "IMPORTANT: You must respond with JSON only - no other text, explanations, "
            "or formatting. The JSON must include:\n"
            "- task: A brief name for the task\n"
            "- description: A detailed description of what the task should do\n"
            "- requirements: List of specific requirements\n"
            "- acceptance_criteria: How to verify the task is complete\n\n"
            "Respond with valid JSON only."
        )
    
    def plan(self, prompt: str) -> dict:
        """Convert a user prompt into a TaskSpec dictionary.
        
        Args:
            prompt: The user's natural language description of the task.
            
        Returns:
            A dictionary representing the TaskSpec.
        """
        messages = [{"role": "user", "content": prompt}]
        response = self.call_llm(system=self.system_prompt, messages=messages)
        
        # Parse JSON response
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            # If response isn't valid JSON, try to extract JSON from the text
            json_start = response.find('{')
            json_end = response.rfind('}') + 1
            if json_start != -1 and json_end != 0:
                return json.loads(response[json_start:json_end])
            raise ValueError(f"Could not parse JSON from response: {response}")
