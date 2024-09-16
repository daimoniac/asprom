'''
Created on Sep 05, 2024

@author stefankn
@namespace asprom.aspromNagiosCheck
small and nice metrics server for asprom
'''
from inc.asprom import initDB, closeDB, AspromModel, Cfg, genMessages
import sys
from time import sleep
from prometheus_client import start_http_server, Gauge

localconf = Cfg()
initDB(localconf)
M = AspromModel()

def getcounter():
    #exposed services
    messageCritExposed, messageWarnExposed = genMessages(M.getAlertsExposed())

    return len(messageCritExposed)+len(messageWarnExposed)

g = Gauge('alerts_open', 'These Ports are unintentionally open and therefore to be checked with the highest priority.')

g.set(0)

if __name__ == '__main__':

    # Start up the server to expose the metrics.
    start_http_server(5000)
    while(True) :
      g.set(getcounter())
      sleep (1000)
