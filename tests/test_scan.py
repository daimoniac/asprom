"""Integration tests for scan()."""

from unittest.mock import MagicMock, patch

from inc.asprom import scan


def _mock_nmap_result():
    mock_ps = MagicMock()
    mock_ps.all_hosts.return_value = ["10.0.0.5"]
    mock_ps.__getitem__ = lambda self, host: {
        "hostname": "scanned-host",
        "tcp": {
            22: {"state": "open", "product": "ssh", "version": "2.0", "extrainfo": ""},
            80: {"state": "closed", "product": "", "version": "", "extrainfo": ""},
        },
    }
    return mock_ps


@patch("inc.asprom.nmap.PortScanner")
def test_scan_creates_machine_and_service(mock_scanner, db_connection):
    mock_scanner.return_value = _mock_nmap_result()

    state = scan("10.0.0.5", "22", "", "test-job-id")
    assert state == "OK"

    cur = db_connection.cursor()
    cur.execute("SELECT COUNT(*) FROM machines WHERE ip = %s", ("10.0.0.5",))
    assert cur.fetchone()[0] == 1

    cur.execute(
        """SELECT COUNT(*) FROM services s
           INNER JOIN machines m ON s.machineId = m.id
           WHERE m.ip = %s AND s.port = 22""",
        ("10.0.0.5",),
    )
    assert cur.fetchone()[0] == 1

    cur.execute(
        "SELECT state FROM scanlog WHERE jobid = %s ORDER BY id DESC LIMIT 1",
        ("test-job-id",),
    )
    assert cur.fetchone()[0] == "OK"


@patch("inc.asprom.nmap.PortScanner")
def test_scan_marks_stale_in_progress_as_timeout(mock_scanner, db_connection):
    mock_scanner.return_value = _mock_nmap_result()
    cur = db_connection.cursor()
    cur.execute(
        """INSERT INTO scanlog (jobid, state, startdate, iprange)
           VALUES ('stale', 'IN PROGRESS', DATE_SUB(NOW(), INTERVAL 2 DAY), '10.0.0.0/24')"""
    )
    db_connection.commit()

    scan("10.0.0.5", "22", "", "fresh-job")
    cur.execute("SELECT state FROM scanlog WHERE jobid = 'stale'")
    assert cur.fetchone()[0] == "TIMEOUT"
