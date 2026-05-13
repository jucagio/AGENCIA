"""
Integration test: repository table names vs. migration 004 schema.

No live database required — this test parses the SQL migration file with
regex to extract the CREATE TABLE names, then asserts that every concrete
repository's `_table` attribute matches a table that actually exists in
the migration.

This static analysis test catches the H4 bug (body_analyses vs body_analysis)
at CI time without needing a running Supabase instance.

Run:
    pytest tests/integration/test_repos_real_schema.py -v
"""

from __future__ import annotations

import re
from pathlib import Path
from unittest.mock import MagicMock

import pytest

from app.core.admin_client import AdminClient
from app.repositories.repos import (
    BodyAnalysisRepository,
    ProfileRepository,
    RecommendationItemRepository,
    RecommendationRepository,
    SubscriptionRepository,
    TryOnRepository,
    UsageCounterRepository,
    UserStyleProfileRepository,
    WardrobeRepository,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

MIGRATION_004 = (
    Path(__file__).parent.parent.parent
    / "migrations"
    / "004_consolidated_schema_v2.sql"
)


def extract_table_names_from_migration(sql_path: Path) -> set[str]:
    """
    Parse *sql_path* and return the set of table names defined by
    CREATE TABLE (IF NOT EXISTS)? public.<name> statements.

    This regex intentionally ignores DROP TABLE to only capture tables
    that survive after the migration is applied.
    """
    sql = sql_path.read_text(encoding="utf-8")
    pattern = re.compile(
        r"CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?public\.(\w+)",
        re.IGNORECASE,
    )
    return {m.group(1) for m in pattern.finditer(sql)}


def make_admin() -> AdminClient:
    """AdminClient wrapping a throw-away MagicMock (no real DB needed)."""
    return AdminClient(MagicMock())


# ---------------------------------------------------------------------------
# Tests
# ---------------------------------------------------------------------------


class TestRepoTableNamesMatchMigration:
    """Every repository must reference a table that exists in migration 004."""

    @pytest.fixture(scope="class")
    def migration_tables(self) -> set[str]:
        assert MIGRATION_004.exists(), (
            f"Migration file not found: {MIGRATION_004}\n"
            "Run from the backend/ directory."
        )
        tables = extract_table_names_from_migration(MIGRATION_004)
        assert tables, "No CREATE TABLE statements found in migration 004"
        return tables

    def _assert_table_in_migration(self, repo_class, migration_tables: set[str]) -> None:
        admin = make_admin()
        repo = repo_class(admin)
        table = repo._table  # noqa: SLF001 — intentional private access in test
        assert table in migration_tables, (
            f"{repo_class.__name__}._table = {table!r} is NOT defined in "
            f"migration 004.\n"
            f"Tables in migration: {sorted(migration_tables)}"
        )

    def test_profile_repo_table(self, migration_tables):
        self._assert_table_in_migration(ProfileRepository, migration_tables)

    def test_wardrobe_repo_table(self, migration_tables):
        self._assert_table_in_migration(WardrobeRepository, migration_tables)

    def test_body_analysis_repo_table(self, migration_tables):
        """[H4] This test would have caught the body_analyses typo."""
        self._assert_table_in_migration(BodyAnalysisRepository, migration_tables)

    def test_recommendation_repo_table(self, migration_tables):
        self._assert_table_in_migration(RecommendationRepository, migration_tables)

    def test_recommendation_item_repo_table(self, migration_tables):
        self._assert_table_in_migration(RecommendationItemRepository, migration_tables)

    def test_try_on_repo_table(self, migration_tables):
        self._assert_table_in_migration(TryOnRepository, migration_tables)

    def test_subscription_repo_table(self, migration_tables):
        self._assert_table_in_migration(SubscriptionRepository, migration_tables)

    def test_user_style_profile_repo_table(self, migration_tables):
        self._assert_table_in_migration(UserStyleProfileRepository, migration_tables)

    def test_usage_counter_repo_table(self, migration_tables):
        self._assert_table_in_migration(UsageCounterRepository, migration_tables)

    def test_all_expected_tables_present_in_migration(self, migration_tables):
        """Sanity: migration 004 must define exactly these 12 tables."""
        expected = {
            "profiles",
            "subscriptions",
            "wardrobe_items",
            "body_analysis",
            "try_on_cache",
            "try_ons",
            "recommendations",
            "recommendation_items",
            "user_style_profile",
            "usage_counters",
            "idempotency_keys",
            "audit_log",
        }
        missing = expected - migration_tables
        assert not missing, (
            f"Migration 004 is missing expected tables: {sorted(missing)}"
        )
