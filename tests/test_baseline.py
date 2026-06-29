"""Integration tests for baseline approve/remove workflow."""

from tests.helpers import (
    assert_in_baseline,
    assert_in_exposed,
    assert_not_in_baseline,
    assert_not_in_exposed,
)


def test_approve_moves_to_baseline(seed_service, db_connection, asprom_model):
    svc = seed_service(port=2222, product="ssh")
    assert_in_exposed(db_connection, svc.id)

    svc.approve("business need", "testuser")
    assert_not_in_exposed(db_connection, svc.id)
    assert_in_baseline(db_connection, svc.id)

    cur = db_connection.cursor()
    cur.execute(
        "SELECT justification, username FROM changelog WHERE serviceId = %s ORDER BY id DESC LIMIT 1",
        (svc.id,),
    )
    row = cur.fetchone()
    assert row[0] == "business need"
    assert row[1] == "testuser"


def test_remove_from_baseline(seed_service, db_connection):
    svc = seed_service(port=3333)
    svc.approve("approved", "admin")
    assert_in_baseline(db_connection, svc.id)

    svc.remove("no longer needed", "admin")
    assert_not_in_baseline(db_connection, svc.id)
    assert_in_exposed(db_connection, svc.id)


def test_get_neatline_after_approve(seed_service, asprom_model):
    svc = seed_service(port=4444, product="mysql")
    svc.approve("db server", "ops")
    rows = asprom_model.getNeatline()
    ids = [r["id"] for r in rows]
    assert svc.id in ids
