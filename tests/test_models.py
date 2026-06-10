"""
Tests for instructor-ainative model catalog.

Refs #3950
"""

from instructor_ainative.models import MODELS, get_model, list_models, DEFAULT_MODEL


class TestModels:
    """Tests for model alias resolution."""

    def test_llama_alias(self):
        assert get_model("llama") == "meta-llama/Llama-3.3-70B-Instruct"

    def test_qwen_alias(self):
        assert get_model("qwen") == "qwen3-coder-flash"

    def test_deepseek_alias(self):
        assert get_model("deepseek") == "deepseek-4-flash"

    def test_kimi_alias(self):
        assert get_model("kimi") == "kimi-k2"

    def test_full_model_id_passthrough(self):
        full_id = "meta-llama/Llama-3.3-70B-Instruct"
        assert get_model(full_id) == full_id

    def test_unknown_alias_passthrough(self):
        assert get_model("some-custom-model") == "some-custom-model"

    def test_default_model_is_llama(self):
        assert DEFAULT_MODEL == "meta-llama/Llama-3.3-70B-Instruct"

    def test_list_models_returns_all(self):
        models = list_models()
        assert isinstance(models, dict)
        assert "llama" in models
        assert "qwen" in models
        assert "deepseek" in models

    def test_models_dict_not_empty(self):
        assert len(MODELS) >= 5
