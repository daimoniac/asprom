"""Integration tests for Service lifecycle."""

from tests.helpers import count_servicelog_entries, current_service_open


def test_service_create_opens_servicelog(seed_service, db_connection):
    svc = seed_service(port=22)
    assert svc.port == 22
    assert current_service_open(db_connection, svc.id) is True


def test_service_create_and_delete_lifecycle(seed_service, db_connection):
    svc = seed_service(port=8080, product="http-proxy")
    assert current_service_open(db_connection, svc.id) is True
    assert count_servicelog_entries(db_connection, svc.id) >= 1

    svc.delete()
    assert current_service_open(db_connection, svc.id) is False


def test_service_create_idempotent(seed_service, db_connection):
    mach = seed_service(port=22).machine
    svc1 = seed_service(port=22, machine=mach)
    svc2 = seed_service(port=22, machine=mach)
    assert svc1.id == svc2.id
