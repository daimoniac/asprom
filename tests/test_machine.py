"""Integration tests for Machine model."""

from inc.asprom import Machine


def test_machine_create_upsert_by_ip(db_connection):
    m1 = Machine.create("host-a", "10.1.1.1")
    m2 = Machine.create("host-a-renamed", "10.1.1.1")
    assert m1.id == m2.id
    assert m2.hostname == "host-a-renamed"


def test_get_services_exposed_only(seed_service, db_connection):
    mach = seed_service(port=22).machine
    open_svc = seed_service(port=80, machine=mach)
    open_svc.delete()

    exposed = mach.getServices(exposedOnly=True)
    assert all(s.port == 22 for s in exposed)


def test_delete_machine(seed_service, db_connection):
    mach = seed_service(port=9000).machine
    machine_id = mach.id
    for service in mach.getServices():
        service.delete()
    mach.delete()

    cur = db_connection.cursor()
    cur.execute("SELECT COUNT(*) FROM machines WHERE id = %s", (machine_id,))
    assert cur.fetchone()[0] == 0
