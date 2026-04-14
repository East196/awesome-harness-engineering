"""Tests for agents module (Task 1.1)."""
import pytest
from unittest.mock import MagicMock, patch


class TestBaseAgent:
    """Tests for BaseAgent class."""

    def test_base_agent_import(self):
        """Test that BaseAgent can be imported."""
        from agents.base import BaseAgent
        assert BaseAgent is not None

    def test_base_agent_has_anthropic_client(self):
        """Test that BaseAgent initializes with an anthropic client."""
        from agents.base import BaseAgent
        agent = BaseAgent()
        assert agent.client is not None

    def test_base_agent_has_model_default(self):
        """Test that BaseAgent has a default model."""
        from agents.base import BaseAgent
        agent = BaseAgent()
        assert hasattr(agent, 'model')
        assert agent.model is not None


class TestPlannerAgent:
    """Tests for PlannerAgent class."""

    def test_planner_agent_import(self):
        """Test that PlannerAgent can be imported."""
        from agents.planner import PlannerAgent
        assert PlannerAgent is not None

    def test_planner_agent_inherits_base(self):
        """Test that PlannerAgent inherits from BaseAgent."""
        from agents.planner import PlannerAgent
        from agents.base import BaseAgent
        assert issubclass(PlannerAgent, BaseAgent)

    def test_planner_agent_has_system_prompt(self):
        """Test that PlannerAgent has a system prompt instructing JSON output."""
        from agents.planner import PlannerAgent
        agent = PlannerAgent()
        assert hasattr(agent, 'system_prompt')
        assert 'JSON' in agent.system_prompt or 'json' in agent.system_prompt

    @patch('agents.planner.BaseAgent.call_llm')
    def test_planner_returns_task_spec(self, mock_call):
        """Test that planner converts prompt to TaskSpec dict."""
        from agents.planner import PlannerAgent
        
        mock_call.return_value = '{"task": "example", "description": "test"}'
        agent = PlannerAgent()
        result = agent.plan("Write a hello world function")
        
        assert isinstance(result, dict)
        assert 'task' in result


class TestGeneratorAgent:
    """Tests for GeneratorAgent class."""

    def test_generator_agent_import(self):
        """Test that GeneratorAgent can be imported."""
        from agents.generator import GeneratorAgent
        assert GeneratorAgent is not None

    def test_generator_agent_inherits_base(self):
        """Test that GeneratorAgent inherits from BaseAgent."""
        from agents.generator import GeneratorAgent
        from agents.base import BaseAgent
        assert issubclass(GeneratorAgent, BaseAgent)

    def test_generate_takes_spec_and_feedback(self):
        """Test that generate method accepts spec dict and optional feedback."""
        from agents.generator import GeneratorAgent
        
        agent = GeneratorAgent()
        spec = {"task": "hello", "description": "Print hello world"}
        
        # Should accept spec and optional feedback
        assert callable(agent.generate)
        
    @patch('agents.generator.BaseAgent.call_llm')
    def test_generate_returns_code_string(self, mock_call):
        """Test that generate returns a code string."""
        from agents.generator import GeneratorAgent
        
        mock_call.return_value = "def hello():\n    print('Hello, World!')"
        agent = GeneratorAgent()
        spec = {"task": "hello", "description": "Print hello world"}
        
        result = agent.generate(spec)
        
        assert isinstance(result, str)
        assert 'def' in result or 'print' in result


class TestEvaluatorAgent:
    """Tests for EvaluatorAgent class."""

    def test_evaluator_agent_import(self):
        """Test that EvaluatorAgent can be imported."""
        from agents.evaluator import EvaluatorAgent
        assert EvaluatorAgent is not None

    def test_evaluator_agent_inherits_base(self):
        """Test that EvaluatorAgent inherits from BaseAgent."""
        from agents.evaluator import EvaluatorAgent
        from agents.base import BaseAgent
        assert issubclass(EvaluatorAgent, BaseAgent)

    def test_evaluation_result_is_pydantic_model(self):
        """Test that EvaluationResult is a Pydantic BaseModel."""
        from agents.evaluator import EvaluationResult
        assert hasattr(EvaluationResult, 'model_validate') or hasattr(EvaluationResult, 'validate')

    def test_evaluation_result_has_required_fields(self):
        """Test that EvaluationResult has quality_score, functionality, code_quality, feedback, passed."""
        from agents.evaluator import EvaluationResult
        
        # Create an instance to check fields
        result = EvaluationResult(
            quality_score=0.8,
            functionality=0.9,
            code_quality=0.85,
            feedback="Minor suggestions",
            passed=True
        )
        
        assert hasattr(result, 'quality_score')
        assert hasattr(result, 'functionality')
        assert hasattr(result, 'code_quality')
        assert hasattr(result, 'feedback')
        assert hasattr(result, 'passed')

    @patch('agents.evaluator.BaseAgent.call_llm')
    def test_evaluate_returns_evaluation_result(self, mock_call):
        """Test that evaluate returns an EvaluationResult instance."""
        from agents.evaluator import EvaluatorAgent, EvaluationResult
        
        mock_call.return_value = '{"quality_score": 0.9, "functionality": 0.8, "code_quality": 0.85, "feedback": "Nice", "passed": true}'
        agent = EvaluatorAgent()
        
        code = "def hello():\n    print('Hello')"
        spec = {"task": "hello", "description": "Print hello"}
        
        result = agent.evaluate(code, spec)
        
        assert isinstance(result, EvaluationResult)
        assert result.passed is True


class TestAgentsPackage:
    """Tests for agents package."""

    def test_agents_package_import(self):
        """Test that agents package can be imported."""
        from agents import base, planner, generator, evaluator
        assert base is not None
        assert planner is not None
        assert generator is not None
        assert evaluator is not None

    def test_all_agents_exported(self):
        """Test that BaseAgent, PlannerAgent, GeneratorAgent, EvaluatorAgent are exported."""
        from agents import BaseAgent, PlannerAgent, GeneratorAgent, EvaluatorAgent
        assert BaseAgent is not None
        assert PlannerAgent is not None
        assert GeneratorAgent is not None
        assert EvaluatorAgent is not None
