"""Shared test assertions for asprom domain model."""

from __future__ import annotations

import MySQLdb


def assert_in_exposed(db: MySQLdb.Connection, service_id: int) -> None:
    cur = db.cursor()
    cur.execute("SELECT COUNT(*) FROM exposed WHERE id = %s", (service_id,))
    count = cur.fetchone()[0]
    assert count == 1, f"service {service_id} not in exposed view"


def assert_not_in_exposed(db: MySQLdb.Connection, service_id: int) -> None:
    cur = db.cursor()
    cur.execute("SELECT COUNT(*) FROM exposed WHERE id = %s", (service_id,))
    count = cur.fetchone()[0]
    assert count == 0, f"service {service_id} still in exposed view"


def assert_in_baseline(db: MySQLdb.Connection, service_id: int) -> None:
    cur = db.cursor()
    cur.execute(
        "SELECT COUNT(*) FROM neatline WHERE serviceId = %s AND neat = 1",
        (service_id,),
    )
    count = cur.fetchone()[0]
    assert count == 1, f"service {service_id} not in baseline"


def assert_not_in_baseline(db: MySQLdb.Connection, service_id: int) -> None:
    cur = db.cursor()
    cur.execute(
        "SELECT neat FROM neatline WHERE serviceId = %s ORDER BY id DESC LIMIT 1",
        (service_id,),
    )
    row = cur.fetchone()
    assert row is None or row[0] == 0, f"service {service_id} still in baseline"


def count_servicelog_entries(db: MySQLdb.Connection, service_id: int) -> int:
    cur = db.cursor()
    cur.execute("SELECT COUNT(*) FROM servicelog WHERE serviceId = %s", (service_id,))
    return cur.fetchone()[0]


def current_service_open(db: MySQLdb.Connection, service_id: int) -> bool:
    cur = db.cursor()
    cur.execute(
        "SELECT openp FROM servicelogCur WHERE serviceId = %s",
        (service_id,),
    )
    row = cur.fetchone()
    return bool(row[0]) if row else False
