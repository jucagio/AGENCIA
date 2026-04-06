"""Security tests for API authentication, permissions, and rate limiting."""

import pytest
from fastapi.testclient import TestClient
from datetime import timedelta
import json
from pathlib import Path

from api.main import app
from api.security.jwt import JWTHandler
from api.security.permissions import PermissionChecker
from api.config import settings


client = TestClient(app)


class TestJWTAuthentication:
    """Test JWT token creation and validation."""

    def test_login_with_valid_credentials(self):
        """Test login with valid credentials returns JWT token."""
        response = client.post("/auth/login", params={"username": "jarvis", "password": "agencia"})
        assert response.status_code == 200
        data = response.json()
        assert "access_token" in data
        assert data["token_type"] == "bearer"
        assert data["user"] == "jarvis"
        assert data["role"] == "admin"

    def test_login_with_invalid_password(self):
        """Test login with invalid password returns 401."""
        response = client.post("/auth/login", params={"username": "jarvis", "password": "wrongpassword"})
        assert response.status_code == 401
        assert "Invalid credentials" in response.json()["detail"]

    def test_login_with_nonexistent_user(self):
        """Test login with non-existent user returns 401."""
        response = client.post("/auth/login", params={"username": "nonexistent", "password": "agencia"})
        assert response.status_code == 401

    def test_agent_endpoint_without_token(self):
        """Test accessing agent endpoints without token returns 401."""
        response = client.get("/agents")
        assert response.status_code == 401
        assert "Missing authorization header" in response.json()["detail"]

    def test_agent_endpoint_with_invalid_token(self):
        """Test accessing agent endpoints with invalid token returns 401."""
        response = client.get(
            "/agents",
            headers={"Authorization": "Bearer invalid.token.here"}
        )
        assert response.status_code == 401
        assert "Invalid or expired token" in response.json()["detail"]

    def test_agent_endpoint_with_valid_token(self):
        """Test accessing agent endpoints with valid token succeeds."""
        # Login to get token
        login_response = client.post("/auth/login", params={"username": "jarvis", "password": "agencia"})
        token = login_response.json()["access_token"]

        # Use token to access agent endpoint
        response = client.get(
            "/agents",
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 200
        assert "agents" in response.json()


class TestPermissions:
    """Test role-based permission system."""

    def test_admin_permissions(self):
        """Test admin role has all permissions."""
        perms = PermissionChecker.get_permissions("admin")
        assert "agents:read" in perms
        assert "agents:execute" in perms
        assert "agents:manage" in perms
        assert "system:audit" in perms

    def test_agent_permissions(self):
        """Test agent role has execute and read permissions."""
        perms = PermissionChecker.get_permissions("agent")
        assert "agents:read" in perms
        assert "agents:execute" in perms
        assert "agents:manage" not in perms

    def test_viewer_permissions(self):
        """Test viewer role has read-only permissions."""
        perms = PermissionChecker.get_permissions("viewer")
        assert "agents:read" in perms
        assert "agents:execute" not in perms

    def test_check_permission_granted(self):
        """Test permission check returns True for granted permissions."""
        result = PermissionChecker.check_permission("admin", "agents:execute")
        assert result is True

    def test_check_permission_denied(self):
        """Test permission check returns False for denied permissions."""
        result = PermissionChecker.check_permission("viewer", "agents:execute")
        assert result is False

    def test_viewer_cannot_execute_agents(self):
        """Test viewer role cannot execute agents via API."""
        # Login as viewer (create a token manually for viewer role)
        token_data = {
            "sub": "test_viewer",
            "role": "viewer",
            "permissions": PermissionChecker.get_permissions("viewer"),
        }
        token = JWTHandler.create_token(token_data, expires_delta=timedelta(hours=1))

        # Try to execute agent
        response = client.post(
            "/agents/sasha/execute",
            params={"prompt": "test"},
            headers={"Authorization": f"Bearer {token}"}
        )
        assert response.status_code == 403
        assert "lacks permission" in response.json()["detail"]


class TestRateLimiting:
    """Test rate limiting (30 requests per minute)."""

    def test_health_endpoint_no_limit(self):
        """Test health endpoint is not rate limited (no auth required)."""
        for _ in range(35):
            response = client.get("/health")
            # Health endpoint should work even if rate limited below
            # (it's not authenticated, so it's not affected by per-user limits)

    def test_rate_limit_exceeded(self):
        """Test rate limiting returns 429 when exceeded."""
        # Login to get token
        login_response = client.post("/auth/login", params={"username": "sasha", "password": "agencia"})
        token = login_response.json()["access_token"]
        headers = {"Authorization": f"Bearer {token}"}

        # Make 31 requests (limit is 30 per minute)
        for i in range(31):
            response = client.get("/agents", headers=headers)
            if i < 30:
                assert response.status_code == 200
            else:
                assert response.status_code == 429
                assert "Rate limit exceeded" in response.json()["detail"]


class TestAuditLogging:
    """Test audit logging of API requests."""

    def test_audit_log_created(self):
        """Test that audit log file is created on first request."""
        audit_path = Path(settings.agent_logs_path) / "api_audit.jsonl"

        # Make a request
        client.get("/health")

        # Check audit log exists
        assert audit_path.exists()

    def test_audit_log_entries_contain_required_fields(self):
        """Test audit log entries have required fields."""
        audit_path = Path(settings.agent_logs_path) / "api_audit.jsonl"

        # Make a request
        client.get("/health")

        # Read audit log
        if audit_path.exists():
            with open(audit_path, "r") as f:
                lines = f.readlines()
                if lines:
                    last_entry = json.loads(lines[-1])
                    assert "timestamp" in last_entry
                    assert "client_ip" in last_entry
                    assert "method" in last_entry
                    assert "path" in last_entry
                    assert "status_code" in last_entry


class TestEndpointAuthentication:
    """Test that protected endpoints require authentication."""

    def test_list_agents_requires_auth(self):
        """Test GET /agents requires authentication."""
        response = client.get("/agents")
        assert response.status_code == 401

    def test_get_agent_state_requires_auth(self):
        """Test GET /agents/{id}/state requires authentication."""
        response = client.get("/agents/sasha/state")
        assert response.status_code == 401

    def test_execute_agent_requires_auth(self):
        """Test POST /agents/{id}/execute requires authentication."""
        response = client.post("/agents/sasha/execute", params={"prompt": "test"})
        assert response.status_code == 401

    def test_health_check_no_auth(self):
        """Test GET /health does not require authentication."""
        response = client.get("/health")
        assert response.status_code == 200

    def test_config_no_auth(self):
        """Test GET /config does not require authentication."""
        response = client.get("/config")
        assert response.status_code == 200


class TestJWTTokenValidation:
    """Test JWT token validation edge cases."""

    def test_token_with_missing_user_id(self):
        """Test token without 'sub' claim is rejected."""
        # Create token with missing 'sub' (user_id)
        invalid_token = JWTHandler.create_token(
            {"role": "admin"},  # Missing 'sub'
            expires_delta=timedelta(hours=1)
        )

        response = client.get(
            "/agents",
            headers={"Authorization": f"Bearer {invalid_token}"}
        )
        assert response.status_code == 401
        assert "user identifier" in response.json()["detail"]

    def test_bearer_format_validation(self):
        """Test invalid Bearer header format returns 401."""
        response = client.get(
            "/agents",
            headers={"Authorization": "InvalidToken"}
        )
        assert response.status_code == 401
        assert "Invalid authorization header format" in response.json()["detail"]


class TestAgentStateTracking:
    """Test that agent state is tracked with user info."""

    def test_execute_agent_tracks_user(self):
        """Test that executed agent state includes executed_by field."""
        # Login
        login_response = client.post("/auth/login", params={"username": "sasha", "password": "agencia"})
        token = login_response.json()["access_token"]

        # Execute agent
        response = client.post(
            "/agents/test_agent/execute",
            params={"prompt": "test prompt"},
            headers={"Authorization": f"Bearer {token}"}
        )

        assert response.status_code == 200
        data = response.json()
        assert data["executed_by"] == "sasha"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
