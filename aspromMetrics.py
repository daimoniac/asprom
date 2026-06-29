"""
Created on Sep 05, 2024

@author stefankn
@namespace asprom.aspromNagiosCheck
small and nice metrics server for asprom
"""

from pprint import pprint
from time import sleep

from prometheus_client import Gauge, start_http_server

from inc.asprom import AspromModel, Cfg, initDB

localconf = Cfg()

alertsExposed = Gauge(
    "alerts_exposed",
    "These Ports are unintentionally open and therefore to be checked with the highest priority.",
)
alertsClosed = Gauge(
    "alerts_closed",
    "These Ports are unintentionally open and therefore to be checked with the highest priority.",
)

initDB(localconf)
M = AspromModel()


def refreshMetrics():

    alertsExposed.set(len(M.getAlertsExposed()))
    alertsClosed.set(len(M.getAlertsClosed()))


if __name__ == "__main__":
    pprint("starting asprom metrics server")
    # Start up the server to expose the metrics.
    start_http_server(5000)

    while True:
        sleep(5)
        refreshMetrics()
