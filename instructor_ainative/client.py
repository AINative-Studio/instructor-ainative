"""
instructor-ainative — Client Factory

Creates pre-configured instructor clients that connect to AINative's
OpenAI-compatible API for structured output extraction.

Refs #3950
"""

from typing import Optional

import instructor
from openai import OpenAI, AsyncOpenAI

from instructor_ainative.provision import resolve_api_key

BASE_URL = "https://api.ainative.studio/api/v1"


def get_client(
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
    mode: instructor.Mode = instructor.Mode.JSON,
    **kwargs,
) -> instructor.Instructor:
    """
    Create a pre-configured instructor client for structured output extraction.

    Uses AINative's free OpenAI-compatible API. If no API key is provided,
    auto-provisions a free account.

    Args:
        api_key: Explicit API key. Falls back to env vars, credentials file,
                 or auto-provisioning.
        base_url: Override the API base URL. Defaults to AINative's endpoint.
        mode: instructor mode for structured output. Defaults to JSON mode
              which works best with open-source models.
        **kwargs: Additional arguments passed to instructor.from_openai().

    Returns:
        An instructor-patched OpenAI client ready for structured output.

    Example:
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
    """
    key = resolve_api_key(api_key)
    base = base_url or BASE_URL

    base_client = OpenAI(
        api_key=key,
        base_url=base,
    )

    return instructor.from_openai(base_client, mode=mode, **kwargs)


def get_async_client(
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
    mode: instructor.Mode = instructor.Mode.JSON,
    **kwargs,
) -> instructor.AsyncInstructor:
    """
    Create a pre-configured async instructor client for structured output extraction.

    Same as get_client() but uses AsyncOpenAI for async/await usage.

    Args:
        api_key: Explicit API key. Falls back to env vars, credentials file,
                 or auto-provisioning.
        base_url: Override the API base URL. Defaults to AINative's endpoint.
        mode: instructor mode for structured output. Defaults to JSON mode.
        **kwargs: Additional arguments passed to instructor.from_openai().

    Returns:
        An async instructor-patched OpenAI client.

    Example:
        import asyncio
        from instructor_ainative import get_async_client
        from pydantic import BaseModel

        class User(BaseModel):
            name: str
            age: int

        async def main():
            client = get_async_client()
            user = await client.chat.completions.create(
                model="meta-llama/Llama-3.3-70B-Instruct",
                response_model=User,
                messages=[{"role": "user", "content": "Extract: John is 30"}],
            )
            print(user)

        asyncio.run(main())
    """
    key = resolve_api_key(api_key)
    base = base_url or BASE_URL

    base_client = AsyncOpenAI(
        api_key=key,
        base_url=base,
    )

    return instructor.from_openai(base_client, mode=mode, **kwargs)
