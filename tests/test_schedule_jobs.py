"""Tests for AspromScheduleModel job management with mocked crontab."""

from unittest.mock import MagicMock, patch

from inc.asprom import AspromScheduleModel


@patch.object(AspromScheduleModel, "render")
@patch.object(AspromScheduleModel, "write")
@patch.object(AspromScheduleModel, "read")
def test_change_job_updates_command(mock_read, mock_write, mock_render):
    sm = AspromScheduleModel.__new__(AspromScheduleModel)
    sm.jobsByID = {}
    job = MagicMock()
    job.is_enabled.return_value = True
    sm.getJobByID = MagicMock(return_value=job)

    with patch("inc.asprom.get_cfg") as mock_cfg:
        mock_cfg.return_value.maindir = "/asprom"
        sm.changeJob(
            "550e8400-e29b-41d4-a716-446655440000",
            "0 0 * * *",
            "10.0.0.0/24",
            "22",
            "-sV",
            job=job,
        )

    job.set_command.assert_called_once()
    assert "10.0.0.0/24" in job.set_command.call_args[0][0]
    mock_write.assert_called_once()
    mock_read.assert_called_once()


@patch.object(AspromScheduleModel, "write")
@patch.object(AspromScheduleModel, "read")
def test_delete_job_disables_entry(mock_read, mock_write):
    sm = AspromScheduleModel.__new__(AspromScheduleModel)
    job = MagicMock()
    sm.getJobByID = MagicMock(return_value=job)

    sm.deleteJob("550e8400-e29b-41d4-a716-446655440000")

    job.enable.assert_called_once_with(False)
    mock_write.assert_called_once()
