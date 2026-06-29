"""Tests for inc.db connection context."""

import MySQLdb

from inc.db import close_db, get_db, set_cfg, set_db
from tests.conftest import DbTestCfg


def test_get_db_outside_bottle(db_connection, mysql_params):
    cfg = DbTestCfg(
        host=mysql_params["host"],
        port=mysql_params["port"],
        user=mysql_params["user"],
        password=mysql_params["passwd"],
        database=mysql_params["db"],
    )
    conn = MySQLdb.connect(**mysql_params)
    set_cfg(cfg)
    set_db(conn)
    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT 1")
    assert cur.fetchone()[0] == 1
    close_db()
