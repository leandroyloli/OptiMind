"""
JSON Schema Validator for OptiMind
Validates output from agents against defined schemas
"""

import json
import jsonschema
from pathlib import Path
from typing import Dict, Any, Tuple, Optional

class SchemaValidator:
    """Validates JSON output against schemas"""
    
    def __init__(self):
        self.schemas = {}
        self._load_schemas()
    
    def _load_schemas(self):
        """Load all schema files from the schemas directory"""
        schemas_dir = Path(__file__).parent
        
        for schema_file in schemas_dir.glob("*.json"):
            schema_name = schema_file.stem
            with open(schema_file, 'r', encoding='utf-8') as f:
                self.schemas[schema_name] = json.load(f)
    
    def validate_problem(self, data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
        """
        Validate problem data against problem_schema.json
        
        Args:
            data: Dictionary containing problem data
            
        Returns:
            (is_valid, error_message)
        """
        try:
            jsonschema.validate(instance=data, schema=self.schemas["problem_schema"])
            return True, None
        except jsonschema.ValidationError as e:
            return False, str(e)
        except KeyError:
            return False, "Schema 'problem_schema' not found"
    
    def validate_json_string(self, json_string: str, schema_name: str = "problem_schema") -> Tuple[bool, Optional[str]]:
        """
        Validate JSON string against specified schema
        
        Args:
            json_string: JSON string to validate
            schema_name: Name of schema to validate against
            
        Returns:
            (is_valid, error_message)
        """
        try:
            data = json.loads(json_string)
            return self.validate_problem(data) if schema_name == "problem_schema" else (False, f"Schema '{schema_name}' not implemented")
        except json.JSONDecodeError as e:
            return False, f"Invalid JSON: {str(e)}"
    
    def get_schema(self, schema_name: str) -> Optional[Dict[str, Any]]:
        """Get schema by name"""
        return self.schemas.get(schema_name)
    
    def list_schemas(self) -> list:
        """List all available schemas"""
        return list(self.schemas.keys())

# Convenience function
def validate_problem_output(data: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
    """Quick validation function for problem output"""
    validator = SchemaValidator()
    return validator.validate_problem(data)

# Utility function to load a schema by name
def load_schema(schema_name: str):
    """Load a schema by name from the schemas directory."""
    validator = SchemaValidator()
    schema = validator.get_schema(schema_name.replace('.json', ''))
    if schema is None:
        raise ValueError(f"Schema '{schema_name}' not found in schemas directory.")
    return schema 