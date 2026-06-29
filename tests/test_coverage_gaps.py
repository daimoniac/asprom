"""Additional coverage for metrics and controller paths."""

from unittest.mock import patch

import aspromMetrics


def test_refresh_metrics_sets_gauges():
    with patch.object(aspromMetrics.alertsExposed, "set") as mock_exposed:
        with patch.object(aspromMetrics.alertsClosed, "set") as mock_closed:
            with patch.object(aspromMetrics, "_ensure_model") as mock_model:
                mock_model.return_value.getAlertsExposed.return_value = [{"id": 1}]
                mock_model.return_value.getAlertsClosed.return_value = [
                    {"id": 2},
                    {"id": 3},
                ]
                aspromMetrics.refreshMetrics()
    mock_exposed.assert_called_once_with(1)
    mock_closed.assert_called_once_with(2)


@patch("inc.asprom.scan", return_value="OK")
def test_controller_rescan_job(mock_scan):
    from inc.asprom import Controller

    with patch("inc.asprom.AspromScheduleModel") as mock_sm:
        instance = mock_sm.return_value
        instance.promoteToIndex.return_value = {
            "job-1": {"iprange": "10.0.0.0/24", "ports": "22", "params": ""}
        }
        result = Controller.rescanJob("job-1")
        assert result == "OK"
        mock_scan.assert_called_once()
