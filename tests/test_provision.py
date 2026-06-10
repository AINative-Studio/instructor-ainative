"""
Tests for instructor-ainative auto-provisioning.

Refs #3950
"""

import json
import os
from pathlib import Path
from unittest.mock import patch, MagicMock

import pytest

from instructor_ainative.provision import (
    resolve_api_key,
    _load_credentials,
    _auto_provision,
    _save_credentials,
    ZERODB_DIR,
    CREDS_PATH,
    CONFIG_PATH,
    CLOUD_API_URL,
)


class TestResolveApiKey:
    """Tests for the multi-source API key resolution."""

    def test_explicit_key_takes_priority(self):
        result = resolve_api_key(explicit_key="explicit-key")
        assert result == "explicit-key"

    @patch.dict(os.environ, {"AINATIVE_API_KEY": "env-key"}, clear=False)
    def test_ainative_env_var(self):
        result = resolve_api_key()
        assert result == "env-key"

    @patch.dict(os.environ, {"ZERODB_API_KEY": "zerodb-key"}, clear=False)
    def test_zerodb_env_var(self):
        # Clear AINATIVE_API_KEY if set
        env = os.environ.copy()
        env.pop("AINATIVE_API_KEY", None)
        with patch.dict(os.environ, env, clear=True):
            os.environ["ZERODB_API_KEY"] = "zerodb-key"
            result = resolve_api_key()
            assert result == "zerodb-key"

    @patch.dict(os.environ, {"AINATIVE_API_KEY": "ainative", "ZERODB_API_KEY": "zerodb"}, clear=False)
    def test_ainative_key_preferred_over_zerodb(self):
        result = resolve_api_key()
        assert result == "ainative"

    def test_explicit_key_beats_env(self):
        with patch.dict(os.environ, {"AINATIVE_API_KEY": "env-key"}, clear=False):
            result = resolve_api_key(explicit_key="explicit")
            assert result == "explicit"


class TestLoadCredentials:
    """Tests for credential file loading."""

    def test_returns_none_when_no_files(self, tmp_path):
        with patch("instructor_ainative.provision.CREDS_PATH", tmp_path / "missing.json"):
            with patch("instructor_ainative.provision.CONFIG_PATH", tmp_path / "missing2.json"):
                result = _load_credentials()
                assert result is None

    def test_reads_credentials_json(self, tmp_path):
        creds_file = tmp_path / "credentials.json"
        creds_file.write_text(json.dumps({"api_key": "file-key"}))

        with patch("instructor_ainative.provision.CREDS_PATH", creds_file):
            with patch("instructor_ainative.provision.CONFIG_PATH", tmp_path / "missing.json"):
                result = _load_credentials()
                assert result == "file-key"

    def test_reads_config_json_fallback(self, tmp_path):
        config_file = tmp_path / "config.json"
        config_file.write_text(json.dumps({"api_key": "config-key"}))

        with patch("instructor_ainative.provision.CREDS_PATH", tmp_path / "missing.json"):
            with patch("instructor_ainative.provision.CONFIG_PATH", config_file):
                result = _load_credentials()
                assert result == "config-key"

    def test_handles_corrupt_json(self, tmp_path):
        creds_file = tmp_path / "credentials.json"
        creds_file.write_text("not valid json{{{")

        with patch("instructor_ainative.provision.CREDS_PATH", creds_file):
            with patch("instructor_ainative.provision.CONFIG_PATH", tmp_path / "missing.json"):
                result = _load_credentials()
                assert result is None


class TestAutoProvision:
    """Tests for the auto-provisioning endpoint."""

    @patch("instructor_ainative.provision.requests")
    @patch("instructor_ainative.provision._save_credentials")
    @patch("instructor_ainative.provision._print_success")
    def test_successful_provision(self, mock_print, mock_save, mock_requests):
        mock_resp = MagicMock()
        mock_resp.status_code = 201
        mock_resp.json.return_value = {
            "api_key": "new-key-12345678",
            "project_id": "proj-1",
            "claim_url": "https://ainative.studio/claim/abc",
        }
        mock_requests.post.return_value = mock_resp

        result = _auto_provision()

        assert result == "new-key-12345678"
        mock_save.assert_called_once()
        mock_print.assert_called_once()

    @patch("instructor_ainative.provision.requests")
    def test_rate_limited(self, mock_requests):
        import requests as real_requests
        mock_requests.RequestException = real_requests.RequestException
        mock_resp = MagicMock()
        mock_resp.status_code = 429
        mock_requests.post.return_value = mock_resp

        with pytest.raises(RuntimeError, match="Rate limited"):
            _auto_provision()

    @patch("instructor_ainative.provision.requests")
    def test_server_error(self, mock_requests):
        import requests as real_requests
        mock_requests.RequestException = real_requests.RequestException
        mock_resp = MagicMock()
        mock_resp.status_code = 500
        mock_requests.post.return_value = mock_resp

        with pytest.raises(RuntimeError, match="Provisioning failed"):
            _auto_provision()

    @patch("instructor_ainative.provision.requests")
    def test_empty_api_key(self, mock_requests):
        import requests as real_requests
        mock_requests.RequestException = real_requests.RequestException
        mock_resp = MagicMock()
        mock_resp.status_code = 200
        mock_resp.json.return_value = {"api_key": ""}
        mock_requests.post.return_value = mock_resp

        with pytest.raises(RuntimeError, match="empty API key"):
            _auto_provision()

    @patch("instructor_ainative.provision.requests")
    def test_network_error(self, mock_requests):
        import requests as real_requests
        mock_requests.RequestException = real_requests.RequestException
        mock_requests.post.side_effect = real_requests.ConnectionError("fail")

        with pytest.raises(RuntimeError, match="Network error"):
            _auto_provision()


class TestSaveCredentials:
    """Tests for credential persistence."""

    def test_saves_to_file(self, tmp_path):
        creds_dir = tmp_path / ".zerodb"
        creds_path = creds_dir / "credentials.json"

        with patch("instructor_ainative.provision.ZERODB_DIR", creds_dir):
            with patch("instructor_ainative.provision.CREDS_PATH", creds_path):
                _save_credentials({
                    "api_key": "saved-key",
                    "project_id": "proj-1",
                    "claim_url": "https://ainative.studio/claim/abc",
                })

        assert creds_path.exists()
        data = json.loads(creds_path.read_text())
        assert data["api_key"] == "saved-key"
        assert data["source"] == "instructor-ainative"
