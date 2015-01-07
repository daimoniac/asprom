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
    parser.add_argument('target', metavar="TARGET", type=__targetFormat,
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


def __targetFormat(v):
    '''
    internal method used by argparse to check if the target argument is in
    fact an IP, Hostname or CIDR Range.

    @param v: the string to check
    @return boolean.
    '''
    try:
        #cidr range
        return re.match(r"^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]\|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\(\/(\d|[1-2]\d|3[0-2]))?$", v).group(0)
    except:
        try:
            #hostname
            return re.match(r"^(([a-zA-Z]|[a-zA-Z][a-zA-Z0-9\-]*\
            [a-zA-Z0-9])\.)*([A-Za-z]|[A-Za-z][A-Za-z0-9\-]*[A-Za-z0-9])$",
            v).group(0)
        except Exception:
            raise argparse.ArgumentTypeError("String '%s' does not match \
             required format" % (v,))


if __name__ == '__main__':
    main()
