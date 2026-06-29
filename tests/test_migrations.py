"""Alembic migration tests."""

import os
import subprocess

import pytest


@pytest.mark.integration
def test_alembic_upgrade_head(mysql_params):
    env = os.environ.copy()
    env.update(
        {
            "ASPROM_TEST_DB_HOST": mysql_params["host"],
            "ASPROM_TEST_DB_PORT": str(mysql_params["port"]),
            "ASPROM_TEST_DB_USER": mysql_params["user"],
            "ASPROM_TEST_DB_PASSWORD": mysql_params["passwd"],
            "ASPROM_TEST_DB_NAME": mysql_params["db"],
        }
    )
    result = subprocess.run(
        ["alembic", "upgrade", "head"],
        cwd="/workspace",
        env=env,
        capture_output=True,
        text=True,
        check=False,
    )
    assert result.returncode == 0, result.stderr
