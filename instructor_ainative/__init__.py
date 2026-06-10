"""
instructor-ainative — Structured output extraction via AINative's free LLM API.

Pre-configured instructor client that connects to AINative's OpenAI-compatible
endpoint. Supports Llama, Qwen, and DeepSeek models with auto-provisioning.

Usage:
    from instructor_ainative import get_client
    from pydantic import BaseModel

    class User(BaseModel):
        name: str
        age: int

    client = get_client()
    user = client.chat.completions.create(
        model="meta-llama/Llama-3.3-70B-Instruct",
        response_model=User,
        messages=[{"role": "user", "content": "Extract: John is 30"}],
    )
    print(user)  # User(name='John', age=30)

Refs #3950
"""

from instructor_ainative.client import get_client, get_async_client
from instructor_ainative.models import MODELS, get_model

__all__ = ["get_client", "get_async_client", "MODELS", "get_model"]
__version__ = "0.1.0"
