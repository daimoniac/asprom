'''
Created on Oct 23, 2014

@author: stefankn
\namespace asprom.aspromNagiosCheck
This file is invoked from the CLI and can be directly used as a nagios plugin.
if any of the services on the alerts-exposed or alerts-closed views are marked as critical,
this script terminates with a return value of 2.
if none are marked as critical, but at least one is marked as warning,
this script terminates with a return value of 1.
Else, it terminates with a value of 0 signalling everything is alright.
'''
#import argparse, re
from inc.asprom import initDB, closeDB, AspromModel
import sys


def main(argv):
    
    exitstate=0
    messageCritExposed=[]
    messageWarnExposed=[]
    messageCritClosed=[]
    messageWarnClosed=[]
    msg=""
    
    initDB()
    M = AspromModel()

    exp = M.getAlertsExposed()
    clo = M.getAlertsClosed()
    
    closeDB()

    #exposed services    
    for row in exp:
        alertFmt = (row['service'] if row['service'] else row['port']) + ' on ' + (row['hostname'] if row['hostname'] else row['ip'])
        if row['crit']:
            messageCritExposed.append(alertFmt)
        else:
            messageWarnExposed.append(alertFmt)
    
    #closed services
    for row in clo:
        alertFmt = (row['service'] if row['service'] else row['port']) + ' on ' + (row['hostname'] if row['hostname'] else row['ip'])
        if row['crit']:
            messageCritClosed.append(alertFmt)
        else:
            messageWarnClosed.append(alertFmt)


    if len(messageCritExposed):
        msg += 'CRITICAL-EXPOSED: ' + "|".join(messageCritExposed) + "\n"
        exitstate = 2
    if len(messageCritClosed):
        msg += 'CRITICAL-CLOSED: ' + "|".join(messageCritClosed) + "\n"
        exitstate = 2
    if len(messageWarnExposed):
        msg += 'WARNING-EXPOSED: ' + "|".join(messageWarnExposed) + "\n"
        exitstate = exitstate or 1
    if len(messageWarnClosed):
        msg += 'WARNING-CLOSED: ' + "|".join(messageWarnClosed) + "\n"
        exitstate = exitstate or 1

    if not exitstate:
        msg = 'all Profiles nominal.'
 
    msg += 'Profiling URL: ' + M.getProfilingURL()
    
    print msg    
    sys.exit(exitstate)
    

if __name__ == '__main__':
    from sys import argv
    main(argv)
    