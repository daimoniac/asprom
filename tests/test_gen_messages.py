"""Tests for genMessages alert formatting."""

from inc.asprom import genMessages


def test_gen_messages_empty():
    crit, warn = genMessages([])
    assert crit == []
    assert warn == []


def test_gen_messages_critical_only():
    rows = [
        {"service": "ssh", "port": 22, "hostname": "host1", "ip": "10.0.0.1", "crit": True},
    ]
    crit, warn = genMessages(rows)
    assert crit == ["ssh[22] on host1"]
    assert warn == []


def test_gen_messages_warning_only():
    rows = [
        {"service": "http", "port": 80, "hostname": "", "ip": "10.0.0.2", "crit": False},
    ]
    crit, warn = genMessages(rows)
    assert crit == []
    assert warn == ["http[80] on 10.0.0.2"]


def test_gen_messages_mixed():
    rows = [
        {"service": "ssh", "port": 22, "hostname": "a", "ip": "10.0.0.1", "crit": True},
        {"service": "", "port": 443, "hostname": "", "ip": "10.0.0.2", "crit": False},
    ]
    crit, warn = genMessages(rows)
    assert len(crit) == 1
    assert len(warn) == 1
    assert "443" in warn[0]
