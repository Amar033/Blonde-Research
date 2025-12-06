import httpx
import asyncio
from typing import List, Dict, Optional, AsyncIterator
from app.core.config import settings
import json

class AIService:
    def __init__(self):
        self.use_mock = settings.VLLM_API_URL == "mock"
        self.base_url = settings.VLLM_API_URL
        self.api_key = settings.VLLM_API_KEY
    
    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        stream: bool = False,
        temperature: float = 0.7,
        max_tokens: int = 2048
    ) -> AsyncIterator[str]:
        """
        Unified chat completion - works with mock or real vLLM
        """
        if self.use_mock:
            async for chunk in self._mock_stream(messages):
                yield chunk
        else:
            async for chunk in self._real_vllm_stream(messages, temperature, max_tokens):
                yield chunk
    
    async def _mock_stream(self, messages: List[Dict[str, str]]) -> AsyncIterator[str]:
        """
        Mock AI responses for local testing
        """
        user_message = messages[-1]["content"].lower()
        
        # Simulate thinking time
        await asyncio.sleep(0.3)
        
        # Generate contextual response
        if "hello" in user_message or "hi" in user_message:
            response = "Hello! I'm your LLaMA assistant (running in mock mode). How can I help you today?"
        elif "weather" in user_message:
            response = "I don't have real-time data in mock mode, but when connected to the GPU, I'll be able to search the web for current weather information!"
        elif "who are you" in user_message:
            response = "I'm a LLaMA-3.3-70B model running through your custom backend. Right now I'm in mock mode for testing, but I'll be powered by the real model on Runpod soon!"
        else:
            response = f"You asked: '{messages[-1]['content']}'\n\nI'm in MOCK MODE for testing. When deployed to Runpod with the real LLaMA-70B model, I'll provide intelligent responses with web search capabilities!"
        
        # Stream word by word
        words = response.split()
        for word in words:
            yield word + " "
            await asyncio.sleep(0.05)  # Simulate streaming delay
    
    async def _real_vllm_stream(
        self,
        messages: List[Dict[str, str]],
        temperature: float,
        max_tokens: int
    ) -> AsyncIterator[str]:
        """
        Real vLLM API streaming
        """
        async with httpx.AsyncClient(timeout=120.0) as client:
            payload = {
                "model": settings.DEFAULT_MODEL,
                "messages": messages,
                "temperature": temperature,
                "max_tokens": max_tokens,
                "stream": True
            }
            
            headers = {}
            if self.api_key:
                headers["Authorization"] = f"Bearer {self.api_key}"
            
            async with client.stream(
                "POST",
                f"{self.base_url}/chat/completions",
                json=payload,
                headers=headers
            ) as response:
                async for line in response.aiter_lines():
                    if line.startswith("data: "):
                        data = line[6:]
                        if data == "[DONE]":
                            break
                        try:
                            chunk = json.loads(data)
                            if "choices" in chunk:
                                delta = chunk["choices"][0].get("delta", {})
                                if "content" in delta:
                                    yield delta["content"]
                        except json.JSONDecodeError:
                            continue

# Global AI service instance
ai_service = AIService()