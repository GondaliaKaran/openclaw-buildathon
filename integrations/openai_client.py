"""
OpenAI API Client Wrapper
Integration Layer

Provides clean interface to OpenAI API for:
- Chat completions (GPT-4)
- Prompt management
- Error handling and retries
"""

import logging
from typing import List, Dict, Optional
from openai import AsyncOpenAI
from tenacity import retry, stop_after_attempt, wait_exponential
from config import config

logger = logging.getLogger(__name__)


class OpenAIClient:
    """Wrapper for OpenAI API with error handling and retries."""
    
    def __init__(self):
        """Initialize OpenAI client."""
        self.api_key = config.openai.api_key
        self.model = config.openai.model
        self.temperature = config.openai.temperature
        self.max_tokens = config.openai.max_tokens
        
        if not self.api_key:
            raise ValueError("OpenAI API key not configured. Set OPENAI_API_KEY in .env")
        
        self.client = AsyncOpenAI(api_key=self.api_key)
        logger.info(f"OpenAI client initialized with model: {self.model}")
    
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10)
    )
    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        response_format: Optional[Dict] = None
    ) -> str:
        """
        Get chat completion from OpenAI.
        
        Args:
            messages: List of message dicts with 'role' and 'content'
            temperature: Temperature for generation (overrides default)
            max_tokens: Max tokens for response (overrides default)
            response_format: Optional response format (e.g., {"type": "json_object"})
        
        Returns:
            Generated text response
        """
        try:
            temp = temperature if temperature is not None else self.temperature
            tokens = max_tokens if max_tokens is not None else self.max_tokens
            
            logger.debug(f"Sending chat completion request (temp={temp}, max_tokens={tokens})")
            
            kwargs = {
                "model": self.model,
                "messages": messages,
                "temperature": temp,
                "max_tokens": tokens
            }
            
            if response_format:
                kwargs["response_format"] = response_format
            
            response = await self.client.chat.completions.create(**kwargs)
            
            content = response.choices[0].message.content
            
            logger.debug(f"Received response ({len(content)} chars)")
            return content
        
        except Exception as e:
            logger.error(f"OpenAI API error: {str(e)}")
            raise
    
    async def chat_completion_with_json(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None
    ) -> str:
        """
        Get chat completion with JSON response format.
        
        Args:
            messages: List of message dicts
            temperature: Temperature for generation
        
        Returns:
            JSON string response
        """
        return await self.chat_completion(
            messages=messages,
            temperature=temperature,
            response_format={"type": "json_object"}
        )
    
    async def analyze_with_context(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.3
    ) -> str:
        """
        Simple analysis with system and user prompts.
        
        Args:
            system_prompt: System role/context
            user_prompt: User query
            temperature: Generation temperature
        
        Returns:
            Analysis response
        """
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        return await self.chat_completion(messages, temperature=temperature)
    
    async def batch_completions(
        self,
        requests: List[Dict[str, any]]
    ) -> List[str]:
        """
        Process multiple completion requests in parallel.
        
        Args:
            requests: List of dicts with 'messages', 'temperature', etc.
        
        Returns:
            List of responses in same order as requests
        """
        import asyncio
        
        tasks = [
            self.chat_completion(**request)
            for request in requests
        ]
        
        return await asyncio.gather(*tasks)
    
    def format_messages(
        self,
        system: str,
        user: str,
        assistant_history: Optional[List[str]] = None
    ) -> List[Dict[str, str]]:
        """
        Helper to format messages list.
        
        Args:
            system: System prompt
            user: User message
            assistant_history: Optional list of assistant responses
        
        Returns:
            Formatted messages list
        """
        messages = [{"role": "system", "content": system}]
        
        if assistant_history:
            for msg in assistant_history:
                messages.append({"role": "assistant", "content": msg})
        
        messages.append({"role": "user", "content": user})
        
        return messages


def create_openai_client() -> OpenAIClient:
    """Create an OpenAI client instance."""
    return OpenAIClient()
