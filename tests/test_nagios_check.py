"""Tests for aspromNagiosCheck exit codes."""

from unittest.mock import patch

import pytest

from inc.asprom import genMessages


def test_nagios_check_ok():
    with patch("aspromNagiosCheck.AspromModel") as mock_model:
        mock_model.return_value.getAlertsExposed.return_value = []
        mock_model.return_value.getAlertsClosed.return_value = []
        with patch("aspromNagiosCheck.genMessages", return_value=([], [])):
            with patch("aspromNagiosCheck.initDB"):
                with patch("aspromNagiosCheck.closeDB"):
                    with patch("aspromNagiosCheck.Cfg") as mock_cfg:
                        mock_cfg.return_value.__getitem__ = lambda s, k: {
                            "misc": {"url": "http://x"}
                        }[k]
                        with patch("aspromNagiosCheck.logger"):
                            with pytest.raises(SystemExit) as exc:
                                import aspromNagiosCheck

                                aspromNagiosCheck.main()
                            assert exc.value.code == 0


def test_nagios_exit_logic_critical():
    rows = [{"service": "ssh", "port": 22, "hostname": "h", "ip": "1.1.1.1", "crit": True}]
    crit, warn = genMessages(rows)
    exitstate = 0
    if len(crit):
        exitstate = 2
    elif len(warn):
        exitstate = 1
    assert exitstate == 2


def test_nagios_exit_logic_warning():
    rows = [{"service": "ssh", "port": 22, "hostname": "h", "ip": "1.1.1.1", "crit": False}]
    crit, warn = genMessages(rows)
    exitstate = 0
    if len(crit):
        exitstate = 2
    elif len(warn):
        exitstate = 1
    assert exitstate == 1
