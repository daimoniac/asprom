"""
Created on Sep 05, 2024

@author stefankn
@namespace asprom.aspromMetrics
small and nice metrics server for asprom
"""

from time import sleep

from prometheus_client import Gauge, start_http_server

from inc.asprom import AspromModel, Cfg, initDB
from inc.logging import configure_logging, get_logger

configure_logging()
logger = get_logger(__name__)

alertsExposed = Gauge(
    "alerts_exposed",
    "These Ports are unintentionally open and therefore to be checked with the highest priority.",
)
alertsClosed = Gauge(
    "alerts_closed",
    "These Ports are unintentionally open and therefore to be checked with the highest priority.",
)

M = None


def _ensure_model():
    global M
    if M is None:
        initDB(Cfg())
        M = AspromModel()
    return M


def refreshMetrics():
    model = _ensure_model()
    alertsExposed.set(len(model.getAlertsExposed()))
    alertsClosed.set(len(model.getAlertsClosed()))


if __name__ == "__main__":
    logger.info("starting asprom metrics server")
    _ensure_model()
    start_http_server(5000)

    while True:
        sleep(5)
        refreshMetrics()
