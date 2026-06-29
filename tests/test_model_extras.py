"""Tests for AspromModel HTML changelog rendering."""

from inc.asprom import AspromScheduleModel


def test_get_last_log_html(seed_service, asprom_model):
    svc = seed_service(port=5500, product="http")
    svc.approve("test justification", "auditor")
    html = asprom_model.getLastLog(5)
    assert "5500" in html
    assert "test justification" in html
    assert "auditor" in html


def test_get_scanned_ranges_plaintext():
    instance = AspromScheduleModel.__new__(AspromScheduleModel)
    instance.schedule = [
        {"iprange": "10.0.0.0/24"},
        {"iprange": "192.168.0.0/16"},
    ]
    instance.getSchedule = lambda: instance.schedule
    assert instance.getScannedRanges() == "10.0.0.0/24\n192.168.0.0/16"
