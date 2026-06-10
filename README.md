# instructor-ainative

Pre-configured [instructor](https://github.com/jxnl/instructor) client for structured output extraction using AINative's free LLM API.

**Zero setup.** Works with Llama 3.3 70B, Qwen3, DeepSeek 4, and Kimi K2 — all free.

## Install

```bash
pip install instructor-ainative
```

## Quick Start

```python
from instructor_ainative import get_client
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int

client = get_client()  # Auto-provisions free API key
user = client.chat.completions.create(
    model="meta-llama/Llama-3.3-70B-Instruct",
    response_model=User,
    messages=[{"role": "user", "content": "Extract: John is 30"}],
)
print(user)  # User(name='John', age=30)
```

## How It Works

`instructor-ainative` wraps [instructor](https://python.useinstructor.com/) with a pre-configured OpenAI client pointing at AINative's free, OpenAI-compatible API. You get structured Pydantic output extraction from open-source models without any API key setup.

On first use, the package auto-provisions a free API key (72-hour TTL). Claim your account at [ainative.studio/signup](https://ainative.studio/signup) for permanent access.

## Available Models

Use aliases or full model IDs:

```python
from instructor_ainative import get_model, MODELS

# Aliases
get_model("llama")     # meta-llama/Llama-3.3-70B-Instruct
get_model("qwen")      # qwen3-coder-flash
get_model("deepseek")  # deepseek-4-flash
get_model("kimi")      # kimi-k2
```

## Async Support

```python
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
```

## Configuration

### API Key Resolution Order

1. Explicit `api_key` parameter
2. `AINATIVE_API_KEY` environment variable
3. `ZERODB_API_KEY` environment variable
4. `~/.zerodb/credentials.json` (shared with ZeroDB ecosystem)
5. Auto-provision (free, 72-hour TTL)

### Bring Your Own Key

```bash
export AINATIVE_API_KEY=your-key-here
```

```python
# Or pass directly
client = get_client(api_key="your-key-here")
```

### Custom Base URL

```python
client = get_client(base_url="https://your-proxy.example.com/v1")
```

### Instructor Mode

```python
import instructor
client = get_client(mode=instructor.Mode.TOOLS)  # Default is JSON mode
```

## Complex Extraction

```python
from instructor_ainative import get_client
from pydantic import BaseModel, Field
from typing import List

class Address(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str = Field(description="5-digit ZIP code")

class Contact(BaseModel):
    name: str
    email: str
    phone: str
    addresses: List[Address]

client = get_client()
contact = client.chat.completions.create(
    model="meta-llama/Llama-3.3-70B-Instruct",
    response_model=Contact,
    messages=[{
        "role": "user",
        "content": """
        Extract contact info: Jane Smith, jane@example.com, 555-0123.
        Lives at 123 Main St, Austin TX 78701 and
        456 Oak Ave, Denver CO 80202.
        """
    }],
)
```

## Why instructor-ainative?

| Feature | instructor + OpenAI | instructor-ainative |
|---------|-------------------|-------------------|
| Setup | Get API key, set env var | `pip install` and go |
| Cost | Pay per token | Free |
| Models | GPT-4o, etc. | Llama 70B, Qwen, DeepSeek |
| Structured output | Yes | Yes |
| Auto-provisioning | No | Yes |

## License

MIT
