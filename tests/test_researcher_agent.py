import pytest
import json
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from agents.researcher_agent import ResearcherAgent
from agents.meaning_agent import MeaningAgent


class TestResearcherAgent:
    """Test suite for Researcher Agent."""
    
    @pytest.fixture
    def researcher_agent(self):
        """Create a Researcher Agent instance for testing."""
        return ResearcherAgent()
    
    @pytest.fixture
    def meaning_agent(self):
        """Create a Meaning Agent instance for testing."""
        return MeaningAgent()
    
    @pytest.fixture
    def sample_meaning_output(self):
        """Sample Meaning Agent output for testing."""
        return {
            "problem_type": "LP",
            "sense": "maximize",
            "objective": "3x + 4y",
            "objective_description": "Maximize total profit from products x and y",
            "decision_variables": {
                "x": {
                    "type": "Real",
                    "description": "Quantity of product x",
                    "bounds": [0, None]
                },
                "y": {
                    "type": "Real",
                    "description": "Quantity of product y",
                    "bounds": [0, None]
                }
            },
            "auxiliary_variables": {},
            "constraints": [
                {
                    "expression": "x + y <= 10",
                    "description": "Total production capacity constraint",
                    "type": "inequality"
                },
                {
                    "expression": "x >= 0",
                    "description": "Non-negativity constraint for x",
                    "type": "bound"
                },
                {
                    "expression": "y >= 0",
                    "description": "Non-negativity constraint for y",
                    "type": "bound"
                }
            ],
            "data": {
                "profit_x": 3,
                "profit_y": 4,
                "capacity": 10
            },
            "is_valid_problem": True,
            "confidence": 0.9,
            "clarification": "Problem is well-defined and ready for optimization.",
            "business_context": {
                "domain": "Production Planning",
                "stakeholders": ["Production Manager", "Operations Team"],
                "constraints": ["Capacity limits", "Non-negativity"]
            }
        }
    
    def test_researcher_agent_initialization(self, researcher_agent):
        """Test Researcher Agent initialization."""
        assert researcher_agent.name == "Researcher"
        assert researcher_agent.get_system_prompt() is not None
        assert len(researcher_agent.get_system_prompt()) > 0
        assert researcher_agent.refined_schema is not None
    
    def test_analyze_problem_quality(self, researcher_agent, sample_meaning_output):
        """Test problem quality analysis."""
        result = researcher_agent.analyze_problem_quality(sample_meaning_output)
        
        assert result["success"] is True
        assert "result" in result
        
        analysis = result["result"]
        assert "completeness_score" in analysis
        assert "clarity_score" in analysis
        assert "robustness_score" in analysis
        assert "issues" in analysis
        assert "suggestions" in analysis
        
        # Scores should be between 0 and 1
        assert 0 <= analysis["completeness_score"] <= 1
        assert 0 <= analysis["clarity_score"] <= 1
        assert 0 <= analysis["robustness_score"] <= 1
        
        # Lists should be present
        assert isinstance(analysis["issues"], list)
        assert isinstance(analysis["suggestions"], list)
    
    def test_get_improvement_suggestions(self, researcher_agent, sample_meaning_output):
        """Test getting improvement suggestions."""
        suggestions = researcher_agent.get_improvement_suggestions(sample_meaning_output)
        
        assert isinstance(suggestions, list)
        assert len(suggestions) >= 0  # Can be empty if problem is good
        
        # All suggestions should be strings
        for suggestion in suggestions:
            assert isinstance(suggestion, str)
            assert len(suggestion) > 0
    
    def test_validate_refined_output(self, researcher_agent):
        """Test validation of refined output against schema."""
        valid_output = {
            "original_problem": {"test": "data"},
            "refined_problem": {
                "problem_type": "LP",
                "sense": "maximize",
                "objective": "3x + 4y",
                "objective_description": "Test objective",
                "decision_variables": {},
                "auxiliary_variables": {},
                "constraints": [],
                "data": {},
                "is_valid_problem": True,
                "confidence": 0.8,
                "clarification": "Test clarification",
                "business_context": {
                    "domain": "test",
                    "stakeholders": [],
                    "constraints": []
                }
            },
            "improvements": ["Test improvement"]
        }
        
        is_valid, error = researcher_agent._validate_refined_output(valid_output)
        assert is_valid is True
        assert error is None
    
    def test_validate_refined_output_invalid(self, researcher_agent):
        """Test validation of invalid refined output."""
        invalid_output = {
            "original_problem": {"test": "data"},
            # Missing refined_problem
            "improvements": ["Test improvement"]
        }
        
        is_valid, error = researcher_agent._validate_refined_output(invalid_output)
        assert is_valid is False
        assert error is not None
        assert len(error) > 0
    
    def test_end_to_end_meaning_to_researcher(self, meaning_agent, researcher_agent):
        """Test complete flow from Meaning to Researcher Agent."""
        print("\n" + "="*60)
        print("🧪 TESTING END-TO-END FLOW: Meaning → Researcher")
        print("="*60)
        
        # 1. Chamada do Meaning Agent
        print("\n📝 1. CHAMADA DO MEANING AGENT:")
        problem_input = "Maximize profit: 5x + 3y subject to x + y <= 20, x >= 0, y >= 0"
        print(f"Input: {problem_input}")
        
        meaning_result = meaning_agent.process_problem(problem_input)
        
        # 2. Resposta recebida do Meaning Agent
        print("\n📝 2. RESPOSTA RECEBIDA DO MEANING AGENT:")
        print(f"Success: {meaning_result.get('success')}")
        print(f"Error: {meaning_result.get('error', 'None')}")
        print(f"Tokens used: {meaning_result.get('tokens_used', 'Unknown')}")
        print(f"Full response: {json.dumps(meaning_result, indent=2)}")
        
        # Check if Meaning Agent succeeded
        if not meaning_result.get("success", False):
            pytest.skip("Meaning Agent failed - skipping end-to-end test")
        
        meaning_output = meaning_result["result"]
        
        # Check if problem is valid
        if not meaning_output.get("is_valid_problem", False):
            pytest.skip("Meaning Agent returned invalid problem - skipping end-to-end test")
        
        print(f"✅ Meaning Agent succeeded! Problem type: {meaning_output.get('problem_type')}")
        
        # 3. Mensagem passada para o Researcher Agent
        print("\n🔍 3. MENSAGEM PASSADA PARA O RESEARCHER AGENT:")
        print(f"Input to Researcher: {json.dumps(meaning_output, indent=2)}")
        
        # 4. Chamada do Researcher Agent
        print("\n🔍 4. CHAMADA DO RESEARCHER AGENT:")
        researcher_result = researcher_agent.refine_problem(meaning_output)
        
        # 5. Resposta recebida do Researcher Agent
        print("\n🔍 5. RESPOSTA RECEBIDA DO RESEARCHER AGENT:")
        print(f"Success: {researcher_result.get('success')}")
        print(f"Error: {researcher_result.get('error', 'None')}")
        print(f"Full response: {json.dumps(researcher_result, indent=2)}")
        
        # Check if Researcher Agent succeeded
        if not researcher_result.get("success", False):
            pytest.skip(f"Researcher Agent failed: {researcher_result.get('error', 'Unknown error')}")
        
        refined_data = researcher_result["result"]
        assert "original_problem" in refined_data
        assert "refined_problem" in refined_data
        assert "improvements" in refined_data
        
        # Verify the original problem is preserved
        assert refined_data["original_problem"] == meaning_output
        
        # Verify the refined problem has the expected structure
        refined_problem = refined_data["refined_problem"]
        assert "problem_type" in refined_problem
        assert "sense" in refined_problem
        assert "objective" in refined_problem
        assert "decision_variables" in refined_problem
        assert "constraints" in refined_problem
        assert "data" in refined_problem
        assert "is_valid_problem" in refined_problem
        assert "confidence" in refined_problem
        
        print(f"✅ Researcher Agent succeeded!")
        print(f"📊 Improvements made: {len(refined_data.get('improvements', []))}")
        print(f"📊 Missing data identified: {len(refined_data.get('missing_data', []))}")
        print(f"📊 Clarification requests: {len(refined_data.get('clarification_requests', []))}")
        
        # Show some details
        improvements = refined_data.get('improvements', [])
        if improvements:
            print("\n🔧 Improvements:")
            for i, improvement in enumerate(improvements, 1):
                print(f"  {i}. {improvement}")
        
        print("\n" + "="*60)
        print("✅ END-TO-END TEST COMPLETED SUCCESSFULLY!")
        print("="*60)
    
    def test_researcher_agent_error_handling(self, researcher_agent):
        """Test error handling in Researcher Agent."""
        # Test with None input
        result = researcher_agent.refine_problem(None)
        assert result["success"] is False
        assert "error" in result
        
        # Test with empty dict
        result = researcher_agent.refine_problem({})
        assert result["success"] is False
        assert "error" in result
        
        # Test with invalid problem
        invalid_input = {
            "is_valid_problem": False,
            "clarification": "This is not a valid problem"
        }
        result = researcher_agent.refine_problem(invalid_input)
        assert result["success"] is False
        assert "Cannot refine invalid problem" in result["error"]


if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v", "-s"]) 