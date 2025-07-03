import json
import jsonschema
from typing import Dict, Any, List
from .base_agent import BaseAgent
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from schemas.validator import load_schema


class ResearcherAgent(BaseAgent):
    """
    Researcher Agent - Refines and improves optimization problems.
    
    This agent receives a structured problem from the Meaning Agent and:
    1. Analyzes the problem for completeness and clarity
    2. Identifies missing data, inconsistencies, or ambiguities
    3. Suggests improvements to make the problem more robust
    4. Refines the problem structure for better mathematical modeling
    5. Maintains all original information while adding enhancements
    """
    
    def __init__(self):
        """Initialize the Researcher Agent."""
        super().__init__(name="Researcher")
        self.refined_schema = load_schema("refined_problem_schema.json")
    
    def _load_prompt(self) -> str:
        """Load the Researcher Agent prompt."""
        try:
            with open("prompts/researcher.txt", "r", encoding="utf-8") as f:
                return f.read()
        except FileNotFoundError:
            raise FileNotFoundError("Prompt file 'prompts/researcher.txt' not found")
    
    def get_system_prompt(self) -> str:
        return self._load_prompt()
    
    def refine_problem(self, meaning_output: Dict[str, Any]) -> Dict[str, Any]:
        """
        Refine a problem received from the Meaning Agent.
        
        Args:
            meaning_output: JSON output from the Meaning Agent
            
        Returns:
            Dict containing the refined problem with improvements and analysis
        """
        try:
            # Validate input is a valid problem structure
            if not isinstance(meaning_output, dict):
                return {
                    "success": False,
                    "error": "Input must be a dictionary from Meaning Agent"
                }
            
            # Check if it's a valid problem
            if not meaning_output.get("is_valid_problem", False):
                return {
                    "success": False,
                    "error": "Cannot refine invalid problem from Meaning Agent"
                }
            
            # Prepare the input for the LLM
            input_data = {
                "meaning_output": meaning_output,
                "task": "refine_and_improve_optimization_problem"
            }
            
            # Process with LLM
            result = self.process(input_data)
            
            if not result["success"]:
                return result
            
            # Log the raw response from LLM
            # print(f"\n🔍 RAW LLM RESPONSE:")
            # print(f"Response type: {type(result['result'])}")
            # print(f"Response content: {repr(result['result'])}")
            # print(f"Response length: {len(str(result['result']))}")
            
            # Clean the response from markdown code blocks
            raw_response = result["result"]
            cleaned_response = raw_response.strip()
            
            # Remove markdown code blocks if present
            if cleaned_response.startswith("```json"):
                cleaned_response = cleaned_response[7:]  # Remove "```json"
            if cleaned_response.startswith("```"):
                cleaned_response = cleaned_response[3:]  # Remove "```"
            if cleaned_response.endswith("```"):
                cleaned_response = cleaned_response[:-3]  # Remove "```"
            
            cleaned_response = cleaned_response.strip()
            print(f"Cleaned response: {cleaned_response[:200]}...")
            
            # Parse the JSON response
            try:
                refined_data = json.loads(cleaned_response)
            except json.JSONDecodeError as e:
                print(f"❌ JSON PARSE ERROR: {str(e)}")
                return {
                    "success": False,
                    "error": f"Invalid JSON response from LLM: {str(e)}"
                }
            
            # Validate against refined schema
            is_valid, validation_error = self._validate_refined_output(refined_data)
            if not is_valid:
                return {
                    "success": False,
                    "error": f"Output validation failed: {validation_error}"
                }
            
            return {
                "success": True,
                "result": refined_data
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error in refine_problem: {str(e)}"
            }
    
    def _validate_refined_output(self, output: Dict[str, Any]) -> tuple[bool, str]:
        """
        Validate the refined output against the refined problem schema.
        
        Args:
            output: The output to validate
            
        Returns:
            Tuple of (is_valid, error_message)
        """
        try:
            jsonschema.validate(instance=output, schema=self.refined_schema)
            return True, None
        except jsonschema.ValidationError as e:
            return False, str(e)
    
    def analyze_problem_quality(self, meaning_output: Dict[str, Any]) -> Dict[str, Any]:
        """
        Analyze the quality of a problem without refining it.
        
        Args:
            meaning_output: JSON output from the Meaning Agent
            
        Returns:
            Dict containing quality analysis
        """
        try:
            analysis = {
                "completeness_score": 0.0,
                "clarity_score": 0.0,
                "robustness_score": 0.0,
                "issues": [],
                "suggestions": []
            }
            
            # Analyze decision variables
            decision_vars = meaning_output.get("decision_variables", {})
            for var_name, var_data in decision_vars.items():
                if "bounds" not in var_data or not var_data["bounds"]:
                    analysis["issues"].append(f"Variable {var_name} lacks bounds")
                    analysis["suggestions"].append(f"Add reasonable bounds for {var_name}")
            
            # Analyze constraints
            constraints = meaning_output.get("constraints", [])
            for i, constraint in enumerate(constraints):
                if "expression" not in constraint:
                    analysis["issues"].append(f"Constraint {i+1} lacks mathematical expression")
            
            # Analyze data completeness
            data = meaning_output.get("data", {})
            if not data:
                analysis["issues"].append("No data parameters provided")
                analysis["suggestions"].append("Add parameter values for objective and constraints")
            
            # Calculate scores
            total_checks = len(decision_vars) + len(constraints) + 1  # +1 for data
            issues_count = len(analysis["issues"])
            analysis["completeness_score"] = max(0.0, 1.0 - (issues_count / total_checks))
            analysis["clarity_score"] = 0.8 if meaning_output.get("confidence", 0) > 0.7 else 0.5
            analysis["robustness_score"] = 0.7 if len(analysis["suggestions"]) < 3 else 0.4
            
            return {
                "success": True,
                "result": analysis
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Error in analyze_problem_quality: {str(e)}"
            }
    
    def get_improvement_suggestions(self, meaning_output: Dict[str, Any]) -> List[str]:
        """
        Get specific improvement suggestions for a problem.
        
        Args:
            meaning_output: JSON output from the Meaning Agent
            
        Returns:
            List of improvement suggestions
        """
        suggestions = []
        
        try:
            # Check for unbounded variables
            decision_vars = meaning_output.get("decision_variables", {})
            for var_name, var_data in decision_vars.items():
                if "bounds" not in var_data or not var_data["bounds"]:
                    suggestions.append(f"Add bounds for variable {var_name} to ensure numerical stability")
            
            # Check for missing data
            data = meaning_output.get("data", {})
            if not data:
                suggestions.append("Provide parameter values for objective and constraint coefficients")
            
            # Check for complex expressions that might benefit from auxiliary variables
            objective = meaning_output.get("objective", "")
            if "*" in objective and objective.count("*") > 2:
                suggestions.append("Consider using auxiliary variables to linearize complex objective")
            
            # Check constraints for potential issues
            constraints = meaning_output.get("constraints", [])
            for i, constraint in enumerate(constraints):
                expr = constraint.get("expression", "")
                if "/" in expr and "0" in expr:
                    suggestions.append(f"Check constraint {i+1} for potential division by zero")
            
            # Add general suggestions
            if len(suggestions) == 0:
                suggestions.append("Problem structure looks good for mathematical modeling")
            
            return suggestions
            
        except Exception as e:
            return [f"Error generating suggestions: {str(e)}"] 