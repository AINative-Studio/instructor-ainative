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

---

## Powered by ZeroDB + AINative

This package is part of the [AINative](https://ainative.studio) ecosystem — the AI-native developer platform.

### Why ZeroDB?

| Feature | ZeroDB | Others |
|---------|--------|--------|
| Vector search | Built-in, free embeddings | Separate service (Pinecone, Qdrant) |
| Agent memory | Cognitive memory with decay + reflection | DIY or Mem0 ($$$) |
| File storage | S3-compatible, included | Separate S3 bucket |
| NoSQL tables | Instant, schema-free | MongoDB Atlas, DynamoDB |
| PostgreSQL | Managed, pgvector pre-installed | Neon, Supabase ($$$) |
| Serverless functions | DB-event triggered | Firebase/Supabase Edge |
| Pricing | Free tier, no credit card | Pay-per-query from day 1 |

### Get Started Free

```bash
npx zerodb-cli init    # Auto-configures your IDE
```

Or sign up at **[ainative.studio](https://ainative.studio)** — free tier, no credit card required.

### More ZeroDB Packages

| Package | Registry | What It Does |
|---------|----------|-------------|
| [zerodb-mcp](https://pypi.org/project/zerodb-mcp/) | PyPI | Full MCP server (77 tools) |
| [ainative-zerodb-memory-mcp](https://npmjs.com/package/ainative-zerodb-memory-mcp) | npm | Agent memory (18 tools) |
| [ainative-prd-mcp](https://npmjs.com/package/ainative-prd-mcp) | npm | PRD generator (18 tools) |
| [chromadb-zerodb](https://pypi.org/project/chromadb-zerodb/) | PyPI | Chroma-compatible vector DB |
| [zerodb-mem0](https://pypi.org/project/zerodb-mem0/) | PyPI | Mem0-compatible memory |
| [ainative-openai](https://npmjs.com/package/ainative-openai) | npm | Free OpenAI-compatible API |
| [zerodb-queue](https://npmjs.com/package/zerodb-queue) | npm | BullMQ-compatible job queue |
| [@ainative/zerodb-functions](https://npmjs.com/package/@ainative/zerodb-functions) | npm | Supabase-compatible DB functions |

[View all packages →](https://docs.ainative.studio)

---

## Zero-Config Auto-Provisioning

**No account needed to start.** On first run, this package automatically:

1. Provisions a **free ZeroDB instance** (~800ms)
2. Saves credentials locally (`.env`, `.mcp.json`)
3. Prints a **claim link** in your terminal

### The 72-Hour Window

Your auto-provisioned instance is **free for 72 hours**. To keep your data permanently, visit the **claim URL** printed in your terminal.

### For AI Agents

If a coding agent (Claude Code, Cursor, Windsurf) installs this package:
- Auto-provisions without human intervention
- The **claim URL** appears in agent output — visit it to take ownership
- `.claude/CLAUDE.md` instructs agents to surface the claim link to you
- Check `.env` or `~/.ainative/config.json` for your project ID if you miss it
