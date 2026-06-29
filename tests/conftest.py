"""Pytest fixtures for asprom integration tests."""

from __future__ import annotations

import os
import re
from pathlib import Path

import MySQLdb
import pytest

ROOT = Path(__file__).resolve().parent.parent
DDL_PATH = ROOT / "db" / "ddl.sql"


class DbTestCfg:
    """Minimal configuration for test database connections."""

    def __init__(self, host: str, port: int, user: str, password: str, database: str):
        self.maindir = str(ROOT)
        self.db = type(
            "DbSection",
            (),
            {
                "data": {
                    "host": host,
                    "port": port,
                    "user": user,
                    "passwd": password,
                    "db": database,
                }
            },
        )()
        self.misc = type("MiscSection", (), {"url": "http://localhost:8080"})()


def _load_schema(connection: MySQLdb.Connection) -> None:
    sql = DDL_PATH.read_text(encoding="utf-8")
    # Unwrap MySQL conditional comments (preserve VIEW definitions)
    sql = re.sub(r"/\*!50001\s+(.*?)\s*\*/", r"\1", sql, flags=re.DOTALL)
    sql = re.sub(r"/\*![0-9]+\s+(.*?)\s*\*/", r"\1", sql, flags=re.DOTALL)
    sql = re.sub(r"/\*![0-9]+.*?\*/", "", sql, flags=re.DOTALL)
    statements = [s.strip() for s in sql.split(";") if s.strip()]
    cur = connection.cursor()
    cur.execute("SET FOREIGN_KEY_CHECKS = 0")
    for statement in statements:
        upper = statement.upper()
        if (
            upper.startswith("USE ")
            or upper.startswith("SET @")
            or "CHARACTER_SET" in upper
            or "COLLATION_CONNECTION" in upper
            or "SQL_MODE" in upper
            or "FOREIGN_KEY_CHECKS=@OLD" in upper
            or "UNIQUE_CHECKS=@OLD" in upper
            or "TIME_ZONE=@OLD" in upper
            or "SQL_NOTES=@OLD" in upper
        ):
            continue
        try:
            cur.execute(statement)
        except MySQLdb.Error as exc:
            if exc.args[0] not in (1050, 1051):
                raise
    cur.execute("SET FOREIGN_KEY_CHECKS = 1")
    connection.commit()


def _default_params() -> dict:
    return {
        "host": os.environ.get("ASPROM_TEST_DB_HOST", "127.0.0.1"),
        "port": int(os.environ.get("ASPROM_TEST_DB_PORT", "3306")),
        "user": os.environ.get("ASPROM_TEST_DB_USER", "asprom"),
        "passwd": os.environ.get("ASPROM_TEST_DB_PASSWORD", "asprom"),
        "db": os.environ.get("ASPROM_TEST_DB_NAME", "asprom_test"),
    }


@pytest.fixture(scope="session")
def mysql_params():
    params = _default_params()
    use_testcontainers = os.environ.get("ASPROM_USE_TESTCONTAINERS", "").lower() in (
        "1",
        "true",
        "yes",
    )
    container = None

    if use_testcontainers:
        from testcontainers.mysql import MySqlContainer

        container = MySqlContainer("mysql:8.0")
        container.start()
        params = {
            "host": container.get_container_host_ip(),
            "port": int(container.get_exposed_port(3306)),
            "user": container.username,
            "passwd": container.password,
            "db": container.dbname,
        }

    try:
        conn = MySQLdb.connect(**params)
        _load_schema(conn)
        conn.close()
    except MySQLdb.Error as exc:
        if container is not None:
            container.stop()
        pytest.skip(f"MySQL not available for integration tests: {exc}")

    yield params

    if container is not None:
        container.stop()


@pytest.fixture
def db_connection(mysql_params):
    from inc.db import close_db, set_cfg, set_db

    conn = MySQLdb.connect(
        host=mysql_params["host"],
        port=mysql_params["port"],
        user=mysql_params["user"],
        passwd=mysql_params["passwd"],
        db=mysql_params["db"],
    )
    _truncate_tables(conn)
    cfg = DbTestCfg(
        host=mysql_params["host"],
        port=mysql_params["port"],
        user=mysql_params["user"],
        password=mysql_params["passwd"],
        database=mysql_params["db"],
    )
    set_cfg(cfg)
    set_db(conn)
    yield conn
    close_db()


def _truncate_tables(conn: MySQLdb.Connection) -> None:
    cur = conn.cursor()
    cur.execute("SET FOREIGN_KEY_CHECKS = 0")
    for table in (
        "changelog",
        "criticality",
        "machinelog",
        "scanlog",
        "servicelog",
        "services",
        "machines",
    ):
        cur.execute(f"TRUNCATE TABLE `{table}`")
    cur.execute("SET FOREIGN_KEY_CHECKS = 1")
    conn.commit()


@pytest.fixture
def seed_machine(db_connection):
    from inc.asprom import Machine

    def _seed(name: str = "host1", ip: str = "10.0.0.1") -> Machine:
        return Machine.create(name, ip)

    return _seed


@pytest.fixture
def seed_service(db_connection, seed_machine):
    from inc.asprom import Service

    def _seed(port: int = 22, product: str = "ssh", machine=None) -> Service:
        mach = machine or seed_machine()
        return Service.create(mach, port, product=product)

    return _seed


@pytest.fixture
def asprom_model(db_connection):
    from inc.asprom import AspromModel

    return AspromModel(username="testuser")
