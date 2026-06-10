"""
Tests for instructor-ainative client factory.

Refs #3950
"""

import os
from unittest.mock import patch, MagicMock

import pytest
import instructor

from instructor_ainative.client import get_client, get_async_client, BASE_URL


class TestGetClient:
    """Tests for the synchronous get_client() factory."""

    @patch("instructor_ainative.client.resolve_api_key")
    @patch("instructor_ainative.client.instructor.from_openai")
    def test_returns_instructor_client(self, mock_from_openai, mock_resolve):
        mock_resolve.return_value = "test-key-123"
        mock_from_openai.return_value = MagicMock(spec=instructor.Instructor)

        client = get_client(api_key="test-key-123")

        assert client is not None
        mock_from_openai.assert_called_once()

    @patch("instructor_ainative.client.resolve_api_key")
    @patch("instructor_ainative.client.OpenAI")
    @patch("instructor_ainative.client.instructor.from_openai")
    def test_passes_api_key_to_openai(self, mock_from_openai, mock_openai, mock_resolve):
        mock_resolve.return_value = "my-key"

        get_client(api_key="my-key")

        mock_openai.assert_called_once_with(api_key="my-key", base_url=BASE_URL)

    @patch("instructor_ainative.client.resolve_api_key")
    @patch("instructor_ainative.client.OpenAI")
    @patch("instructor_ainative.client.instructor.from_openai")
    def test_custom_base_url(self, mock_from_openai, mock_openai, mock_resolve):
        mock_resolve.return_value = "key"

        get_client(api_key="key", base_url="https://custom.api/v1")

        mock_openai.assert_called_once_with(
            api_key="key", base_url="https://custom.api/v1"
        )

    @patch("instructor_ainative.client.resolve_api_key")
    @patch("instructor_ainative.client.OpenAI")
    @patch("instructor_ainative.client.instructor.from_openai")
    def test_default_mode_is_json(self, mock_from_openai, mock_openai, mock_resolve):
        mock_resolve.return_value = "key"

        get_client(api_key="key")

        call_kwargs = mock_from_openai.call_args
        assert call_kwargs[1]["mode"] == instructor.Mode.JSON

    @patch("instructor_ainative.client.resolve_api_key")
    @patch("instructor_ainative.client.OpenAI")
    @patch("instructor_ainative.client.instructor.from_openai")
    def test_custom_mode(self, mock_from_openai, mock_openai, mock_resolve):
        mock_resolve.return_value = "key"

        get_client(api_key="key", mode=instructor.Mode.TOOLS)

        call_kwargs = mock_from_openai.call_args
        assert call_kwargs[1]["mode"] == instructor.Mode.TOOLS

    @patch("instructor_ainative.client.resolve_api_key")
    @patch("instructor_ainative.client.OpenAI")
    @patch("instructor_ainative.client.instructor.from_openai")
    def test_extra_kwargs_passed_through(self, mock_from_openai, mock_openai, mock_resolve):
        mock_resolve.return_value = "key"

        get_client(api_key="key", max_retries=5)

        call_kwargs = mock_from_openai.call_args
        assert call_kwargs[1]["max_retries"] == 5


class TestGetAsyncClient:
    """Tests for the async get_async_client() factory."""

    @patch("instructor_ainative.client.resolve_api_key")
    @patch("instructor_ainative.client.AsyncOpenAI")
    @patch("instructor_ainative.client.instructor.from_openai")
    def test_uses_async_openai(self, mock_from_openai, mock_async_openai, mock_resolve):
        mock_resolve.return_value = "key"

        get_async_client(api_key="key")

        mock_async_openai.assert_called_once_with(api_key="key", base_url=BASE_URL)

    @patch("instructor_ainative.client.resolve_api_key")
    @patch("instructor_ainative.client.AsyncOpenAI")
    @patch("instructor_ainative.client.instructor.from_openai")
    def test_custom_base_url_async(self, mock_from_openai, mock_async_openai, mock_resolve):
        mock_resolve.return_value = "key"

        get_async_client(api_key="key", base_url="https://other.api/v1")

        mock_async_openai.assert_called_once_with(
            api_key="key", base_url="https://other.api/v1"
        )
