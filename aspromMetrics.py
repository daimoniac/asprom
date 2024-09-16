'''
Created on Sep 05, 2024

@author stefankn
@namespace asprom.aspromNagiosCheck
small and nice metrics server for asprom
'''
from inc.asprom import initDB, closeDB, AspromModel, Cfg
from time import sleep
from prometheus_client import start_http_server, Gauge
from pprint import pprint

localconf = Cfg()

alertsExposed = Gauge('alerts_exposed', 'These Ports are unintentionally open and therefore to be checked with the highest priority.')
alertsClosed = Gauge('alerts_closed', 'These Ports are unintentionally open and therefore to be checked with the highest priority.')

def refreshMetrics():
    initDB(localconf)
    M = AspromModel()

    alertsExposed.set(len(M.getAlertsExposed()))
    alertsClosed.set(len(M.getAlertsClosed()))

    closeDB()


if __name__ == '__main__':

    pprint("starting asprom metrics server")
    # Start up the server to expose the metrics.
    start_http_server(5000)

    while True:
        sleep(5)
        refreshMetrics()
