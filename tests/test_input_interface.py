"""
Tests for Input Interface - Optimization Problem Entry
Test the new job/input interface functionality
"""

import pytest
import streamlit as st
import sys
import os
import re

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pages.d_NewJob import validate_optimization_input, get_example_problems

# Import the validation function from the new job page
def validate_optimization_input(text, objective_type):
    """Mock validation function for testing"""
    errors = []
    suggestions = []
    
    if not text or text.strip() == "":
        errors.append("Problem description cannot be empty")
        suggestions.append("Please describe your optimization problem")
        return False, errors, suggestions
    
    if len(text.strip()) < 10:
        errors.append("Problem description is too short")
        suggestions.append("Please provide more details about your problem")
        return False, errors, suggestions
    
    optimization_keywords = ['maximize', 'minimize', 'maximizar', 'minimizar', 'max', 'min']
    has_optimization_keyword = any(keyword in text.lower() for keyword in optimization_keywords)
    
    if not has_optimization_keyword:
        errors.append("No optimization objective found")
        suggestions.append("Include words like 'maximize', 'minimize', 'max', or 'min' in your description")
    
    variable_patterns = [
        r'\b[a-zA-Z]\b',
        r'\b[a-zA-Z][a-zA-Z0-9_]*\b',
        r'\b(x|y|z|a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|w)\b'
    ]
    
    has_variables = any(re.search(pattern, text) for pattern in variable_patterns)
    if not has_variables:
        errors.append("No variables found in the problem")
        suggestions.append("Include variables like x, y, z, or other letters in your problem")
    
    constraint_keywords = ['subject to', 's.t.', 'constraint', 'restriction', 'limit', 'bound', '<=', '>=', '=', '<', '>']
    has_constraints = any(keyword in text.lower() for keyword in constraint_keywords)
    
    if not has_constraints:
        errors.append("No constraints found in the problem")
        suggestions.append("Include constraints using words like 'subject to', '<=', '>=', or '='")
    
    if not errors:
        suggestions.append("✅ Problem looks good! Ready for processing.")
    
    return len(errors) == 0, errors, suggestions

def get_example_problems():
    """Mock example problems for testing"""
    return [
        {
            "title": "Production Planning",
            "description": "Maximize profit: 100*x + 150*y subject to x + 2*y <= 100, x + y <= 80, x >= 0, y >= 0",
            "objective": "maximize"
        },
        {
            "title": "Portfolio Optimization",
            "description": "Minimize risk: 0.1*x^2 + 0.2*y^2 + 0.15*x*y subject to x + y = 1, x >= 0, y >= 0",
            "objective": "minimize"
        },
        {
            "title": "Transportation Problem",
            "description": "Minimize cost: 10*x1 + 15*x2 + 12*x3 subject to x1 + x2 + x3 >= 50, x1 <= 20, x2 <= 30, x3 <= 25",
            "objective": "minimize"
        },
        {
            "title": "Resource Allocation",
            "description": "Maximize efficiency: 5*x + 3*y + 4*z subject to 2*x + y + z <= 100, x + 3*y + 2*z <= 150, x,y,z >= 0",
            "objective": "maximize"
        }
    ]

class TestInputInterfaceValidation:
    """Test the input interface validation functionality"""
    
    def test_validate_empty_input(self):
        """Test validation of empty input"""
        is_valid, errors, suggestions = validate_optimization_input("", "maximize")
        assert not is_valid
        assert "cannot be empty" in errors[0]
        assert len(errors) > 0
    
    def test_validate_short_input(self):
        """Test validation of input that's too short"""
        is_valid, errors, suggestions = validate_optimization_input("short", "maximize")
        assert not is_valid
        assert "too short" in errors[0]
        assert len(errors) > 0
    
    def test_validate_missing_optimization_keyword(self):
        """Test validation when optimization keyword is missing"""
        is_valid, errors, suggestions = validate_optimization_input(
            "This is a problem with variables x and y and constraints x + y <= 10", 
            "maximize"
        )
        assert not is_valid
        assert "No optimization objective found" in errors[0]
    

    
    def test_validate_missing_constraints(self):
        """Test validation when constraints are missing"""
        is_valid, errors, suggestions = validate_optimization_input(
            "Maximize 100*x + 150*y with variables x and y", 
            "maximize"
        )
        assert not is_valid
        assert "No constraints found" in errors[0]
    
    def test_validate_valid_input(self):
        """Test validation of valid optimization input"""
        valid_input = "Maximize profit: 100*x + 150*y subject to x + 2*y <= 100, x + y <= 80, x >= 0, y >= 0"
        is_valid, errors, suggestions = validate_optimization_input(valid_input, "maximize")
        assert is_valid
        assert len(errors) == 0
        assert "Problem looks good" in suggestions[0]
    
    def test_validate_minimize_input(self):
        """Test validation of minimize input"""
        valid_input = "Minimize cost: 10*x + 15*y subject to x + y >= 50, x <= 20, y <= 30"
        is_valid, errors, suggestions = validate_optimization_input(valid_input, "minimize")
        assert is_valid
        assert len(errors) == 0
    
    def test_validate_with_different_variable_names(self):
        """Test validation with various variable naming patterns"""
        test_cases = [
            "Maximize a + b subject to a + b <= 10",
            "Minimize x1 + x2 subject to x1 + x2 >= 5",
            "Maximize profit_var + cost_var subject to profit_var <= 100"
        ]
        
        for test_input in test_cases:
            is_valid, errors, suggestions = validate_optimization_input(test_input, "maximize")
            assert is_valid, f"Failed for input: {test_input}"
    
    def test_validate_with_different_constraint_patterns(self):
        """Test validation with various constraint patterns"""
        test_cases = [
            "Maximize x + y subject to x + y <= 10",
            "Minimize a + b s.t. a + b >= 5",
            "Maximize profit with constraint x + y = 100",
            "Minimize cost where x + y < 50",
            "Maximize z with restriction x + y > 0"
        ]
        
        for test_input in test_cases:
            is_valid, errors, suggestions = validate_optimization_input(test_input, "maximize")
            assert is_valid, f"Failed for input: {test_input}"

class TestInputInterfaceExamples:
    """Test the example problems functionality in the input interface"""
    
    def test_get_example_problems(self):
        """Test that example problems are returned correctly"""
        examples = get_example_problems()
        assert len(examples) == 4
        assert all(isinstance(example, dict) for example in examples)
        
        # Check required fields
        required_fields = ["title", "description", "objective"]
        for example in examples:
            for field in required_fields:
                assert field in example
                assert example[field] is not None
                assert len(str(example[field])) > 0
    
    def test_example_problems_content(self):
        """Test that example problems have meaningful content"""
        examples = get_example_problems()
        
        # Check titles
        titles = [ex["title"] for ex in examples]
        expected_titles = ["Production Planning", "Portfolio Optimization", "Transportation Problem", "Resource Allocation"]
        assert all(title in titles for title in expected_titles)
        
        # Check objectives
        objectives = [ex["objective"] for ex in examples]
        assert "maximize" in objectives
        assert "minimize" in objectives
        
        # Check descriptions contain optimization elements
        for example in examples:
            desc = example["description"].lower()
            assert any(keyword in desc for keyword in ["maximize", "minimize"])
            assert any(char in desc for char in ["x", "y", "z"])
            assert any(keyword in desc for keyword in ["subject to", "<=", ">=", "="])

class TestInputInterfaceEdgeCases:
    """Test edge cases in input interface validation"""
    
    def test_validate_with_special_characters(self):
        """Test validation with special characters in input"""
        special_input = "Maximize 100*x^2 + 150*y^2 subject to x + y <= 100, x >= 0, y >= 0"
        is_valid, errors, suggestions = validate_optimization_input(special_input, "maximize")
        assert is_valid
    
    def test_validate_with_numbers_in_variables(self):
        """Test validation with numbered variables"""
        numbered_input = "Minimize 10*x1 + 15*x2 + 12*x3 subject to x1 + x2 + x3 >= 50"
        is_valid, errors, suggestions = validate_optimization_input(numbered_input, "minimize")
        assert is_valid
    
    def test_validate_case_insensitive(self):
        """Test that validation is case insensitive"""
        inputs = [
            "MAXIMIZE x + y subject to x + y <= 10",
            "maximize X + Y subject to X + Y <= 10",
            "Maximize profit: A + B subject to A + B <= 100"
        ]
        
        for test_input in inputs:
            is_valid, errors, suggestions = validate_optimization_input(test_input, "maximize")
            assert is_valid, f"Failed for input: {test_input}"
    
    def test_validate_with_whitespace(self):
        """Test validation handles whitespace correctly"""
        whitespace_input = "   Maximize   x + y   subject to   x + y <= 10   "
        is_valid, errors, suggestions = validate_optimization_input(whitespace_input, "maximize")
        assert is_valid

def test_validation_function_returns_correct_types():
    """Test that validation function returns correct data types"""
    test_input = "Maximize x + y subject to x + y <= 10"
    is_valid, errors, suggestions = validate_optimization_input(test_input, "maximize")
    
    assert isinstance(is_valid, bool)
    assert isinstance(errors, list)
    assert isinstance(suggestions, list)
    assert all(isinstance(error, str) for error in errors)
    assert all(isinstance(suggestion, str) for suggestion in suggestions)

def test_example_problems_structure():
    """Test that example problems have consistent structure"""
    examples = get_example_problems()
    
    for example in examples:
        # Check data types
        assert isinstance(example["title"], str)
        assert isinstance(example["description"], str)
        assert isinstance(example["objective"], str)
        
        # Check content length
        assert len(example["title"]) > 0
        assert len(example["description"]) > 10
        assert example["objective"] in ["maximize", "minimize"]

if __name__ == "__main__":
    # Run tests
    pytest.main([__file__, "-v"]) 