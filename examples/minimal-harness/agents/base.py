"""BaseAgent class with common LLM calling functionality."""
import os
from typing import Optional
from anthropic import Anthropic


class BaseAgent:
    """Base class for all agents with common LLM calling functionality.
    
    Attributes:
        model: The LLM model to use for completions.
        client: The Anthropic client instance.
    """
    
    def __init__(self, model: str = "claude-sonnet-4-20250514"):
        """Initialize the BaseAgent.
        
        Args:
            model: The model identifier for the LLM. Defaults to claude-sonnet-4-20250514.
        """
        self.model = model
        self.client = Anthropic(api_key=os.environ.get("ANTHROPIC_API_KEY"))
    
    def call_llm(
        self,
        messages: list[dict[str, str]],
        system: Optional[str] = None,
        max_tokens: int = 4096,
    ) -> str:
        """Call the LLM with the given messages.
        
        Args:
            system: Optional system prompt.
            messages: List of message dicts with 'role' and 'content' keys.
            max_tokens: Maximum tokens to generate.
            
        Returns:
            The text content of the LLM response.
        """
        response = self.client.messages.create(
            model=self.model,
            system=system,
            max_tokens=max_tokens,
            messages=messages,
        )
        return response.content[0].text
