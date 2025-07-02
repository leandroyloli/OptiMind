"""
Meaning Agent for OptiMind
A conversational partner that helps users define optimization problems through natural dialogue
"""

import json
import re
from pathlib import Path
from typing import Dict, Any, Tuple, Optional, List
from .base_agent import BaseAgent
from schemas.validator import validate_problem_output

class MeaningAgent(BaseAgent):
    """Conversational agent that partners with users to define optimization problems"""
    
    def __init__(self, model: str = "gpt-4o-mini"):
        super().__init__(name="Meaning", model=model)
        self.prompt_path = Path(__file__).parent.parent / "prompts" / "meaning.txt"
        self.chat_history: List[Dict[str, str]] = []
        self.current_problem_state: Dict[str, Any] = {}
    
    def get_system_prompt(self) -> str:
        """Get the system prompt for the Meaning agent"""
        try:
            with open(self.prompt_path, 'r', encoding='utf-8') as f:
                return f.read()
        except FileNotFoundError:
            return self._get_fallback_prompt()
    
    def _get_fallback_prompt(self) -> str:
        """Fallback prompt if file not found"""
        return """You are the Meaning Agent of OptiMind, a conversational partner that helps users define optimization problems through natural dialogue.

## YOUR ROLE
You are a knowledgeable, patient, and encouraging partner who guides users step-by-step to define their optimization problems. You don't just extract information - you collaborate, ask clarifying questions, and help users think through their problems.

## CONVERSATION STYLE
- **Partner-like**: Work together with the user, not just extract information
- **Encouraging**: Celebrate progress and guide gently when stuck
- **Patient**: Build the problem gradually, don't rush
- **Knowledgeable**: Share insights about optimization when helpful
- **Natural**: Use everyday language, avoid jargon unless necessary

## YOUR APPROACH
1. **Listen and understand** what the user is trying to achieve
2. **Ask thoughtful questions** to help them clarify their thinking
3. **Suggest improvements** and point out potential issues
4. **Build together** - acknowledge each piece of information they provide
5. **Guide toward completion** without being pushy

## CRITICAL REQUIREMENT
You MUST ALWAYS return valid JSON in this exact format, even for casual conversations:

{
  "problem_type": "LP|MIP|NLP|Stochastic|Combinatorial|Network|Meta-Heuristics|Unknown",
  "sense": "maximize|minimize", 
  "objective": "mathematical expression",
  "objective_description": "description in English",
  "decision_variables": {
    "variable_name": {
      "type": "Real|Integer|Binary",
      "description": "variable description",
      "bounds": [min, max]
    }
  },
  "auxiliary_variables": {
    "variable_name": {
      "type": "Real|Integer|Binary",
      "description": "auxiliary variable description",
      "equation": "expression in terms of decision variables"
    }
  },
  "constraints": [
    {
      "expression": "mathematical expression",
      "description": "constraint description",
      "type": "inequality|equality|bound"
    }
  ],
  "is_valid_problem": true/false,
  "confidence": 0.0-1.0,
  "clarification": "your conversational response to the user",
  "business_context": {
    "domain": "problem domain",
    "stakeholders": ["stakeholder1", "stakeholder2"],
    "constraints": ["constraint1", "constraint2"]
  }
}

## RESPONSE GUIDELINES
- For casual greetings: Be warm and welcoming, guide toward optimization
- For unclear messages: Ask specific questions to understand their goal
- For partial problems: Acknowledge what you understand, ask for missing pieces
- For complete problems: Confirm understanding, suggest potential improvements
- Always be encouraging and collaborative

## VARIABLE CLASSIFICATION
- **Decision Variables**: What the user directly controls or decides
- **Auxiliary Variables**: Calculated from decision variables (totals, ratios, etc.)

Remember: You're a partner, not just a form-filler. Help users think through their optimization problems naturally."""
    
    def _process_response(self, response: str, input_data: Any, **kwargs) -> Any:
        """
        Process the raw response from OpenAI
        
        Args:
            response: Raw response from OpenAI
            input_data: Original input data
            **kwargs: Additional arguments
            
        Returns:
            Processed result (JSON dict)
        """
        try:
            # Try to parse as JSON
            result = json.loads(response)
            
            # Validate against schema
            is_valid, error = validate_problem_output(result)
            
            if not is_valid:
                # If validation fails, return error structure
                return {
                    "problem_type": "Unknown",
                    "sense": "maximize",
                    "objective": "",
                    "objective_description": "",
                    "decision_variables": {},
                    "auxiliary_variables": {},
                    "constraints": [],
                    "is_valid_problem": False,
                    "confidence": 0.0,
                    "clarification": f"Schema validation failed: {error}. Please provide a clearer problem description.",
                    "business_context": {
                        "domain": "Unknown",
                        "stakeholders": [],
                        "constraints": []
                    }
                }
            
            # Validate financial consistency if applicable
            if result.get('business_context', {}).get('domain', '').lower() in ['finance', 'cash flow', 'investment']:
                consistency_check = self._validate_financial_consistency(result)
                if not consistency_check['is_consistent']:
                    result['clarification'] = f"Please check unit consistency: {consistency_check['issues']}"
                    result['confidence'] = max(0.0, result.get('confidence', 0.0) - 0.2)
            
            # Update current problem state
            self.current_problem_state = result.copy()
            
            return result
            
        except json.JSONDecodeError as e:
            # If JSON parsing fails, return error structure
            return {
                "problem_type": "Unknown",
                "sense": "maximize",
                "objective": "",
                "objective_description": "",
                "decision_variables": {},
                "auxiliary_variables": {},
                "constraints": [],
                "is_valid_problem": False,
                "confidence": 0.0,
                "clarification": f"Failed to parse response as JSON: {str(e)}. Please provide a clearer problem description.",
                "business_context": {
                    "domain": "Unknown",
                    "stakeholders": [],
                    "constraints": []
                }
            }
    
    def _validate_financial_consistency(self, problem_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate financial consistency in the problem data
        
        Args:
            problem_data: Problem data to validate
            
        Returns:
            Validation result with issues
        """
        issues = []
        
        # Check for unit consistency in constraints
        constraints = problem_data.get('constraints', [])
        objective = problem_data.get('objective', '')
        
        # Look for potential unit mismatches
        values_in_constraints = []
        for constraint in constraints:
            expression = constraint.get('expression', '')
            # Extract numbers from expressions
            numbers = re.findall(r'\d+\.?\d*', expression)
            values_in_constraints.extend(numbers)
        
        # Check objective for numbers
        objective_numbers = re.findall(r'\d+\.?\d*', objective)
        
        # If we have very different scales, flag as potential issue
        if values_in_constraints and objective_numbers:
            constraint_scale = max([float(x) for x in values_in_constraints if x])
            objective_scale = max([float(x) for x in objective_numbers if x])
            
            if constraint_scale > 0 and objective_scale > 0:
                scale_ratio = max(constraint_scale, objective_scale) / min(constraint_scale, objective_scale)
                if scale_ratio > 100:  # Significant scale difference
                    issues.append(f"Potential unit inconsistency detected. Values range from {min(constraint_scale, objective_scale)} to {max(constraint_scale, objective_scale)}")
        
        return {
            "is_consistent": len(issues) == 0,
            "issues": "; ".join(issues) if issues else "No issues detected"
        }
    
    def validate_output(self, output: Any) -> Tuple[bool, Optional[str]]:
        """
        Validate Meaning Agent output
        
        Args:
            output: Agent output to validate
            
        Returns:
            (is_valid, error_message)
        """
        return validate_problem_output(output)
    
    def add_to_chat_history(self, message: str, sender: str = "user"):
        """
        Add a message to the chat history
        
        Args:
            message: The message content
            sender: Who sent the message ("user" or "assistant")
        """
        self.chat_history.append({
            "sender": sender,
            "message": message
        })
    
    def get_chat_context(self) -> str:
        """
        Get the formatted chat context for the prompt
        
        Returns:
            Formatted chat history as string
        """
        if not self.chat_history:
            return ""
        
        context_lines = ["## CONVERSATION HISTORY:"]
        for i, msg in enumerate(self.chat_history, 1):
            role = "User" if msg["sender"] == "user" else "Assistant"
            context_lines.append(f"{i}. {role}: {msg['message']}")
        
        context_lines.append("")
        context_lines.append("## CURRENT PROBLEM STATE:")
        if self.current_problem_state:
            context_lines.append(f"- Problem Type: {self.current_problem_state.get('problem_type', 'Unknown')}")
            context_lines.append(f"- Objective: {self.current_problem_state.get('objective', 'Not defined')}")
            context_lines.append(f"- Decision Variables: {list(self.current_problem_state.get('decision_variables', {}).keys())}")
            context_lines.append(f"- Auxiliary Variables: {list(self.current_problem_state.get('auxiliary_variables', {}).keys())}")
            context_lines.append(f"- Constraints: {len(self.current_problem_state.get('constraints', []))}")
        else:
            context_lines.append("- No problem state yet")
        
        context_lines.append("")
        context_lines.append("## CURRENT MESSAGE TO ANALYZE:")
        
        return "\n".join(context_lines)
    
    def clear_chat_history(self):
        """Clear the chat history and problem state"""
        self.chat_history = []
        self.current_problem_state = {}
    
    def process_problem(self, problem_text: str, objective_type: str = None) -> Dict[str, Any]:
        """
        Process optimization problem text with chat context
        
        Args:
            problem_text: Natural language description of the problem
            objective_type: Type of objective (maximize/minimize) - optional for context-aware processing
            
        Returns:
            Dictionary with processing result
        """
        # Add user message to chat history
        self.add_to_chat_history(problem_text, "user")
        
        # Prepare input with context
        chat_context = self.get_chat_context()
        
        # Build the full prompt with context
        if objective_type:
            input_data = f"{chat_context}{problem_text}\n\nObjective type: {objective_type}"
        else:
            input_data = f"{chat_context}{problem_text}"
        
        # Process with context
        result = self.process(input_data)
        
        # Add assistant response to chat history if successful
        if result.get('success', False):
            problem_data = result.get('result', {})
            
            # Get the conversational response from the model
            conversational_response = problem_data.get('clarification', 'I understand your problem. Please provide more details if needed.')
            
            # Add to chat history
            self.add_to_chat_history(conversational_response, "assistant")
        
        return result 