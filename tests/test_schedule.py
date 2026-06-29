"""Tests for schedule model helpers."""

from datetime import datetime
from unittest.mock import MagicMock

import pytest

from inc.asprom import AspromScheduleModel, NoJoibIDException


def test_promote_to_index_dicts():
    rows = [
        {"id": "a", "ip": "10.0.0.1", "port": "22"},
        {"id": "b", "ip": "10.0.0.2", "port": "80"},
    ]
    result = AspromScheduleModel.promoteToIndex(rows, "id")
    assert result["a"]["ip"] == "10.0.0.1"
    assert result["b"]["port"] == "80"


def test_promote_to_index_lists():
    rows = [[1, 2, 3], [4, 5, 6]]
    result = AspromScheduleModel.promoteToIndex(rows, 1)
    assert result[2] == [1, 3]
    assert result[5] == [4, 6]


def test_fetch_job_parses_command():
    sm = AspromScheduleModel.__new__(AspromScheduleModel)
    sm.scheduleLog = {}

    job = MagicMock()
    job.is_enabled.return_value = True
    job.command = (
        "python /asprom/aspromScan.py -j "
        '550e8400-e29b-41d4-a716-446655440000 -o="-sV" -p 1-1024 10.0.0.0/24'
    )
    job.slices.render.return_value = "0 0 * * *"
    job.schedule.return_value.get_next.return_value = datetime(2026, 1, 1, 12, 0)

    spec = sm._AspromScheduleModel__fetchJob(job)
    assert spec["id"] == "550e8400-e29b-41d4-a716-446655440000"
    assert spec["iprange"] == "10.0.0.0/24"
    assert spec["ports"] == "1-1024"
    assert spec["params"] == "-sV"


def test_fetch_job_raises_for_non_asprom():
    sm = AspromScheduleModel.__new__(AspromScheduleModel)
    sm.scheduleLog = {}
    job = MagicMock()
    job.is_enabled.return_value = False
    job.command = "/bin/true"
    with pytest.raises(NoJoibIDException):
        sm._AspromScheduleModel__fetchJob(job)


def test_get_scanned_ranges():
    sm = AspromScheduleModel.__new__(AspromScheduleModel)
    sm.schedule = [
        {"iprange": "10.0.0.0/24"},
        {"iprange": "192.168.1.0/24"},
    ]
    sm.getSchedule = lambda: sm.schedule
    result = sm.getScannedRanges()
    assert result == "10.0.0.0/24\n192.168.1.0/24"
