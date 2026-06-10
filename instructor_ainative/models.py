"""
instructor-ainative — Supported Models

Model aliases and catalog for AINative's OpenAI-compatible endpoint.
All models support structured output extraction via instructor.

Refs #3950
"""

from typing import Optional

# Model aliases -> full model identifiers
MODELS = {
    # Meta Llama
    "llama": "meta-llama/Llama-3.3-70B-Instruct",
    "llama-70b": "meta-llama/Llama-3.3-70B-Instruct",
    "llama-8b": "meta-llama/Llama-3.1-8B-Instruct",
    # Qwen
    "qwen": "qwen3-coder-flash",
    "qwen-coder": "qwen3-coder-flash",
    # DeepSeek
    "deepseek": "deepseek-4-flash",
    "deepseek-flash": "deepseek-4-flash",
    # Kimi
    "kimi": "kimi-k2",
}

# Default model for get_client()
DEFAULT_MODEL = "meta-llama/Llama-3.3-70B-Instruct"


def get_model(alias: str) -> str:
    """
    Resolve a model alias to its full identifier.

    Args:
        alias: Short alias (e.g. "llama", "qwen") or full model ID.

    Returns:
        Full model identifier string.

    Examples:
        >>> get_model("llama")
        'meta-llama/Llama-3.3-70B-Instruct'
        >>> get_model("qwen")
        'qwen3-coder-flash'
        >>> get_model("meta-llama/Llama-3.3-70B-Instruct")
        'meta-llama/Llama-3.3-70B-Instruct'
    """
    return MODELS.get(alias, alias)


def list_models() -> dict:
    """Return all available model aliases and their full identifiers."""
    return dict(MODELS)
