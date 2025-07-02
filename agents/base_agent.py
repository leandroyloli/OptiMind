"""
Base Agent Class for OptiMind
Provides common functionality for all agents
"""

import json
import time
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, Tuple
from openai import OpenAI
import streamlit as st

class BaseAgent(ABC):
    """Base class for all OptiMind agents"""
    
    def __init__(self, name: str, model: str = "gpt-4o-mini"):
        """
        Initialize base agent
        
        Args:
            name: Agent name
            model: OpenAI model to use
        """
        self.name = name
        self.model = model
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """Initialize OpenAI client"""
        try:
            # Try to get API key from Streamlit secrets
            api_key = st.secrets.get("OPENAI", {}).get("OPENAI_API_KEY")
            if not api_key:
                # Fallback to environment variable
                import os
                api_key = os.getenv("OPENAI_API_KEY")
            
            if api_key:
                self.client = OpenAI(api_key=api_key)
            else:
                st.error("OpenAI API key not found. Please configure it in Streamlit secrets or environment variables.")
                self.client = None
        except Exception as e:
            st.error(f"Failed to initialize OpenAI client: {str(e)}")
            self.client = None
    
    @abstractmethod
    def get_system_prompt(self) -> str:
        """Get the system prompt for this agent"""
        pass
    
    def process(self, input_data: Any, **kwargs) -> Dict[str, Any]:
        """
        Process input data and return result
        
        Args:
            input_data: Input data to process
            **kwargs: Additional arguments
            
        Returns:
            Dictionary with processing result
        """
        if not self.client:
            return {
                "success": False,
                "error": "OpenAI client not initialized",
                "agent": self.name
            }
        
        try:
            # Get system prompt
            system_prompt = self.get_system_prompt()
            
            # Prepare user message
            user_message = self._prepare_user_message(input_data, **kwargs)
            
            # Call OpenAI
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                temperature=0.1,  # Low temperature for consistent results
                max_tokens=2000
            )
            
            # Extract response
            result = response.choices[0].message.content
            
            # Process response
            processed_result = self._process_response(result, input_data, **kwargs)
            
            return {
                "success": True,
                "result": processed_result,
                "agent": self.name,
                "model": self.model,
                "tokens_used": response.usage.total_tokens
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "agent": self.name
            }
    
    def _prepare_user_message(self, input_data: Any, **kwargs) -> str:
        """
        Prepare user message from input data
        
        Args:
            input_data: Input data
            **kwargs: Additional arguments
            
        Returns:
            Formatted user message
        """
        if isinstance(input_data, str):
            return input_data
        elif isinstance(input_data, dict):
            return json.dumps(input_data, indent=2, ensure_ascii=False)
        else:
            return str(input_data)
    
    def _process_response(self, response: str, input_data: Any, **kwargs) -> Any:
        """
        Process the raw response from OpenAI
        
        Args:
            response: Raw response from OpenAI
            input_data: Original input data
            **kwargs: Additional arguments
            
        Returns:
            Processed result
        """
        # Default implementation - try to parse as JSON
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            # If not JSON, return as string
            return response
    
    def validate_output(self, output: Any) -> Tuple[bool, Optional[str]]:
        """
        Validate agent output
        
        Args:
            output: Agent output to validate
            
        Returns:
            (is_valid, error_message)
        """
        # Default implementation - always valid
        return True, None
    
    def get_status(self) -> Dict[str, Any]:
        """Get agent status"""
        return {
            "name": self.name,
            "model": self.model,
            "client_initialized": self.client is not None
        } 