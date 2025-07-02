#!/usr/bin/env python3
"""
Test script for JSON Schema validation
"""

import json
import sys
import os

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from schemas.validator import SchemaValidator

def test_schema_validation():
    """Test the schema validation"""
    print("🧪 Testing JSON Schema Validation...")
    
    # Load validator
    validator = SchemaValidator()
    print(f"✅ Loaded schemas: {validator.list_schemas()}")
    
    # Load example problem
    with open('schemas/example_problem.json', 'r', encoding='utf-8') as f:
        example_problem = json.load(f)
    
    print("📋 Example problem loaded")
    
    # Test validation
    is_valid, error = validator.validate_problem(example_problem)
    
    if is_valid:
        print("✅ Schema validation PASSED!")
        print(f"📊 Problem type: {example_problem['problem_type']}")
        print(f"🎯 Objective: {example_problem['objective']}")
        print(f"📈 Confidence: {example_problem['confidence']}")
        print(f"🔢 Decision variables: {len(example_problem.get('decision_variables', {}))}")
        print(f"🔧 Auxiliary variables: {len(example_problem.get('auxiliary_variables', {}))}")
    else:
        print("❌ Schema validation FAILED!")
        print(f"Error: {error}")
    
    # Test invalid JSON
    invalid_data = {"problem_type": "INVALID", "sense": "invalid"}
    is_valid, error = validator.validate_problem(invalid_data)
    
    if not is_valid:
        print("✅ Invalid data correctly rejected!")
    else:
        print("❌ Invalid data should have been rejected!")

if __name__ == "__main__":
    test_schema_validation() 