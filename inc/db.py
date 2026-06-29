from __future__ import annotations

import threading
from typing import TYPE_CHECKING, Any

import MySQLdb as mdb
from bottle import request

if TYPE_CHECKING:
    from inc.asprom import Cfg

_local = threading.local()


def set_db(conn: Any) -> None:
    """Set the active connection for non-Bottle contexts (tests, CLI)."""
    _local.connection = conn


def set_cfg(cfg: Cfg) -> None:
    """Set the active configuration for non-Bottle contexts."""
    _local.cfg = cfg


def get_db() -> Any:
    """Return the active database connection."""
    try:
        return request.db
    except (AttributeError, RuntimeError):
        conn = getattr(_local, "connection", None)
        if conn is None:
            raise RuntimeError("No database connection available")
        return conn


def get_cfg() -> Cfg:
    """Return the active configuration object."""
    try:
        return request.cfg
    except (AttributeError, RuntimeError):
        cfg = getattr(_local, "cfg", None)
        if cfg is None:
            raise RuntimeError("No configuration available")
        return cfg


def init_db(localconf: Cfg) -> None:
    """Open a database connection and bind it to the current context."""
    try:
        request.cfg = localconf
        request.db = mdb.connect(**localconf.db.data)
    except (AttributeError, RuntimeError):
        set_cfg(localconf)
        set_db(mdb.connect(**localconf.db.data))


def close_db() -> None:
    """Commit and close the active database connection."""
    try:
        db = get_db()
        db.commit()
        db.close()
    except mdb.OperationalError:
        pass
    except RuntimeError:
        pass
    finally:
        if hasattr(_local, "connection"):
            del _local.connection
        if hasattr(_local, "cfg"):
            del _local.cfg
        try:
            del request.db
        except (AttributeError, RuntimeError):
            pass
