'''
Created on Oct 23, 2014

@author stefankn
@namespace asprom.aspromNagiosCheck
This file is invoked from the CLI and can be directly used as a nagios plugin.
if any of the services on the alerts-exposed or alerts-closed views
are marked as critical,
this script terminates with a return value of 2.
if none are marked as critical, but at least one is marked as warning,
this script terminates with a return value of 1.
Else, it terminates with a value of 0 signalling everything is alright.
'''
from inc.asprom import initDB, closeDB, AspromModel, Cfg, genMessages
import sys

def main():
    exitstate = 0
    msg = ""

    localconf = Cfg()
    initDB(localconf)
    M = AspromModel()

    #exposed services
    messageCritExposed, messageWarnExposed = genMessages(M.getAlertsExposed())

    #closed services
    messageCritClosed, messageWarnClosed = genMessages(M.getAlertsClosed())

    closeDB()

    # Start up the server to expose the metrics.
    start_http_server(5000)
    if len(messageCritExposed):
        msg += 'CRITICAL-EXPOSED: ' + " | ".join(messageCritExposed) + "\n"
        exitstate = 2
    if len(messageCritClosed):
        msg += 'CRITICAL-CLOSED: ' + " | ".join(messageCritClosed) + "\n"
        exitstate = 2
    if len(messageWarnExposed):
        msg += 'WARNING-EXPOSED: ' + " | ".join(messageWarnExposed) + "\n"
        exitstate = exitstate or 1
    if len(messageWarnClosed):
        msg += 'WARNING-CLOSED: ' + " | ".join(messageWarnClosed) + "\n"
        exitstate = exitstate or 1

    if not exitstate:
        msg = 'all Profiles nominal.'

    msg += 'Profiling URL: ' + localconf['misc']['url']

    print(msg)
    sys.exit(exitstate)


if __name__ == '__main__':
    main()
