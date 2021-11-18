'''
Created on Oct 23, 2014

@author stefankn
@namespace asprom.aspromScan
this file is invoked on the CLI as a wrapper script to nmap.
when invoked from the command line, the scan() method is called.
'''
import argparse
import re
from inc.asprom import scan, initDB, closeDB, Cfg


def main():
    '''
    parse arguments from command line.


>        usage:

    aspromScan.py [-h] [-o EXTRA_OPTIONS] [-s SENSOR] [-p PORT_RANGE]
    [-j JOB_ID] TARGET

    Scans an IP Range for asprom. Needs nmap installed on the sensor host.


    positional arguments:
      TARGET                the hostname/ip/ip range to be scanned

    optional arguments:

      -h, --help            show this help message and exit

      -o EXTRA_OPTIONS, --extra-options EXTRA_OPTIONS
                            extra options to be passed to nmap

      -s SENSOR, --sensor SENSOR
                            start scanning on another sensor

      -p PORT_RANGE, --port-range PORT_RANGE
                            set custom port range to be scanned

      -j JOB_ID, --job-id JOB_ID
                            set arbitrary job id (used by aspromGUI and cron)
    '''
    parser = argparse.ArgumentParser(description='''Scans an IP Range for
    asprom. Needs nmap installed on the sensor host.''')
    parser.add_argument('target', metavar="TARGET", 
                   help='the hostname/ip/ip range to be scanned')
    parser.add_argument('-o', '--extra-options', default='',
                   help='extra options to be passed to nmap')
    parser.add_argument('-s', '--sensor', default='localhost',
                   help='start scanning on another sensor')
    parser.add_argument('-p', '--port-range', default=None,
                   help='set custom port range to be scanned')
    parser.add_argument('-j', '--job-id', default=None,
                   help='set arbitrary job id (used by aspromGUI and cron)')

    args = parser.parse_args()

    localconf = Cfg()
    initDB(localconf)
    scan(args.target, args.port_range, args.extra_options, args.job_id)
    closeDB()

if __name__ == '__main__':
    main()
