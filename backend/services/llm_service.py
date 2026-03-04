"""
LLM Service
===========
This service handles communication with OpenAI-compatible LLM APIs.

Prompt Engineering Best Practices Used:
1. System Role: Defines the AI's persona and constraints
2. User Role: Provides the specific task and context
3. Temperature Control:
   - Lower temperature (0.0-0.3): More deterministic, factual responses
   - Medium temperature (0.4-0.7): Creative but controlled
   - Higher temperature (0.8-1.0): More random/creative

For evaluation tasks, we use low temperature for consistency.
For question generation, we use medium temperature for variety.

JSON Output: We request JSON format for structured parsing.

Author: AI Interview Coach Team
"""

import os
import json
from typing import Optional, List, Dict, Any
from openai import OpenAI


class LLMService:
    """
    Service for interacting with OpenAI-compatible LLM APIs.
    
    Supports both OpenAI and compatible APIs (like local models,
    Azure OpenAI, etc.) through configuration.
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: Optional[str] = None,
        default_temperature: float = 0.7,
        default_max_tokens: int = 2000
    ):
        """
        Initialize the LLM service.
        
        Args:
            api_key: API key for authentication (defaults to env var)
            base_url: Base URL for API endpoint
            model: Model identifier to use (defaults to llama2)
            default_temperature: Default temperature for generations
            default_max_tokens: Default max tokens for response
        """
        # Get API configuration - use provided key or from environment
        self.api_key = api_key or os.getenv("OPENAI_API_KEY") or "ollama"
        self.base_url = base_url or os.getenv("OPENAI_BASE_URL", "http://localhost:11434/v1")
        # Use provided model, or env var, or default to llama2
        self.model = model if model else os.getenv("OPENAI_MODEL", "llama2")
        self.default_temperature = default_temperature
        self.default_max_tokens = default_max_tokens
        
        # Initialize OpenAI client
        self.client = OpenAI(
            api_key=self.api_key,
            base_url=self.base_url
        )
        
        print(f"🤖 LLM service initialized with model: {self.model}")
        print(f"   Base URL: {self.base_url}")
    
    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        response_format: Optional[Dict] = None
    ) -> str:
        """
        Generate a response from the LLM.
        
        This method implements the core prompt engineering pattern:
        1. System prompt defines the AI's behavior and constraints
        2. User prompt provides the specific task
        
        Args:
            system_prompt: System-level instructions (AI persona, rules)
            user_prompt: User's specific request
            temperature: Controls randomness (0=deterministic, 1=random)
            max_tokens: Maximum tokens in response
            response_format: Expected format (e.g., {"type": "json_object"})
            
        Returns:
            Generated text response
        """
        # Use defaults if not specified
        temp = temperature if temperature is not None else self.default_temperature
        tokens = max_tokens if max_tokens is not None else self.default_max_tokens
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        # Build request parameters
        params = {
            "model": self.model,
            "messages": messages,
            "temperature": temp,
            "max_tokens": tokens
        }
        
        # Add response format if specified (for JSON)
        if response_format:
            params["response_format"] = response_format
        
        try:
            response = self.client.chat.completions.create(**params)
            return response.choices[0].message.content
        except Exception as e:
            print(f"❌ Error generating response: {str(e)}")
            raise
    
    def generate_json(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Generate a JSON response from the LLM.
        
        Uses JSON mode to ensure valid JSON output that's easy to parse.
        
        Args:
            system_prompt: System-level instructions
            user_prompt: User's specific request
            temperature: Controls randomness
            max_tokens: Maximum tokens in response
            
        Returns:
            Parsed JSON response as dictionary
        """
        response = self.generate(
            system_prompt=system_prompt,
            user_prompt=user_prompt,
            temperature=temperature,
            max_tokens=max_tokens,
            response_format={"type": "json_object"}
        )
        
        # Parse JSON response
        try:
            return json.loads(response)
        except json.JSONDecodeError:
            # Try to extract JSON from response
            try:
                # Look for JSON in markdown code blocks
                import re
                json_match = re.search(r'\{.*\}', response, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group())
            except:
                pass
            raise ValueError(f"Failed to parse JSON response: {response}")
    
    def generate_with_retry(
        self,
        system_prompt: str,
        user_prompt: str,
        max_retries: int = 3,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Generate response with automatic retry on failure.
        
        Args:
            system_prompt: System-level instructions
            user_prompt: User's specific request
            max_retries: Maximum number of retry attempts
            temperature: Controls randomness
            max_tokens: Maximum tokens in response
            
        Returns:
            Generated text response
        """
        for attempt in range(max_retries):
            try:
                return self.generate(
                    system_prompt=system_prompt,
                    user_prompt=user_prompt,
                    temperature=temperature,
                    max_tokens=max_tokens
                )
            except Exception as e:
                if attempt == max_retries - 1:
                    raise
                print(f"⚠️ Attempt {attempt + 1} failed, retrying...")
                import time
                time.sleep(1 * (attempt + 1))  # Exponential backoff
