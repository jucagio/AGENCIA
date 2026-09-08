"""Zero-trust permission checking for API."""

from typing import List, Optional


class PermissionChecker:
    """Zero-trust permission system — all start with no permissions."""

    # Define roles and their permissions
    PERMISSIONS = {
        "admin": {
            "agents:read",
            "agents:execute",
            "agents:manage",
            "system:audit",
        },
        "agent": {
            "agents:read",
            "agents:execute",
        },
        "viewer": {
            "agents:read",
        },
        "none": set(),
    }

    @staticmethod
    def check_permission(user_role: str, required_permission: str) -> bool:
        """
        Check if a role has a required permission.

        Args:
            user_role: User's role (e.g., "admin", "agent", "viewer")
            required_permission: Permission required (e.g., "agents:execute")

        Returns:
            True if user has permission, False otherwise
        """
        permissions = PermissionChecker.PERMISSIONS.get(user_role, set())
        return required_permission in permissions

    @staticmethod
    def get_permissions(user_role: str) -> List[str]:
        """Get all permissions for a role."""
        return list(PermissionChecker.PERMISSIONS.get(user_role, set()))


# Default roles for common operations
ROLE_PERMISSIONS = {
    "jarvis": "admin",      # Can do everything
    "sasha": "agent",       # Can execute and read
    "brook": "agent",       # Can execute and read
    "erik": "agent",        # Can execute and read
    "admin": "admin",       # Full access
}
