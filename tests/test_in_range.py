"""Tests for Service.inRange and Machine.inRange."""

import pytest

from inc.asprom import Machine, Service


class TestServiceInRange:
    def test_single_port_int(self):
        svc = type("S", (), {"port": 22})()
        assert Service.inRange(svc, 22) is True
        assert Service.inRange(svc, 80) is False

    def test_single_port_string(self):
        svc = type("S", (), {"port": 443})()
        assert Service.inRange(svc, "443") is True

    def test_port_range(self):
        svc = type("S", (), {"port": 8080})()
        assert Service.inRange(svc, "8000-9000") is True
        assert Service.inRange(svc, "1-80") is False

    def test_invalid_range_raises(self):
        svc = type("S", (), {"port": 22})()
        with pytest.raises(Exception):
            Service.inRange(svc, "invalid")


class TestMachineInRange:
    def test_single_ip(self):
        assert Machine.inRange("10.0.0.1", "10.0.0.1") is True
        assert Machine.inRange("10.0.0.2", "10.0.0.1") is False

    def test_cidr_range(self):
        assert Machine.inRange("10.0.0.0/24", "10.0.0.50") is True
        assert Machine.inRange("10.0.0.0/24", "10.0.1.1") is False

    def test_invalid_range_raises(self):
        with pytest.raises(Exception):
            Machine.inRange("not-a-range", "10.0.0.1")
