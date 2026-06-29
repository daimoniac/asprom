"""Integration tests for SQL views."""


def test_exposed_view_lists_open_unapproved(seed_service, db_connection, asprom_model):
    exposed = seed_service(port=10001, product="test-a")
    approved = seed_service(port=10002, product="test-b")
    approved.approve("ok", "user")

    rows = asprom_model.getAlertsExposed()
    ids = [r["id"] for r in rows]
    assert exposed.id in ids
    assert approved.id not in ids


def test_servicelog_cur_reflects_latest_state(seed_service, db_connection):
    svc = seed_service(port=10003)
    cur = db_connection.cursor()
    cur.execute("SELECT openp FROM servicelogCur WHERE serviceId = %s", (svc.id,))
    assert cur.fetchone()[0] == 1

    svc.delete()
    cur.execute("SELECT openp FROM servicelogCur WHERE serviceId = %s", (svc.id,))
    assert cur.fetchone()[0] == 0


def test_neatline_view_after_approval(seed_service, db_connection):
    svc = seed_service(port=10004)
    svc.approve("justified", "user")
    cur = db_connection.cursor()
    cur.execute(
        "SELECT neat, justification FROM neatline WHERE serviceId = %s",
        (svc.id,),
    )
    row = cur.fetchone()
    assert row[0] == 1
    assert row[1] == "justified"
