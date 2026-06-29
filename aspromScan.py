"""
Created on Oct 23, 2014

@author stefankn
@namespace asprom.aspromScan
this file is invoked on the CLI as a wrapper script to nmap.
"""

import argparse

from inc.asprom import Cfg, closeDB, initDB, scan
from inc.logging import configure_logging, get_logger

configure_logging()
logger = get_logger(__name__)


def main():
    parser = argparse.ArgumentParser(
        description="Scans an IP Range for asprom. Needs nmap installed on the sensor host."
    )
    parser.add_argument("target", metavar="TARGET", help="the hostname/ip/ip range to be scanned")
    parser.add_argument(
        "-o", "--extra-options", default="", help="extra options to be passed to nmap"
    )
    parser.add_argument(
        "-s", "--sensor", default="localhost", help="start scanning on another sensor"
    )
    parser.add_argument(
        "-p", "--port-range", default=None, help="set custom port range to be scanned"
    )
    parser.add_argument(
        "-j", "--job-id", default=None, help="set arbitrary job id (used by aspromGUI and cron)"
    )

    args = parser.parse_args()
    logger.info(
        "scan_start",
        target=args.target,
        port_range=args.port_range,
        job_id=args.job_id,
        sensor=args.sensor,
    )

    localconf = Cfg()
    initDB(localconf)
    state = scan(args.target, args.port_range, args.extra_options, args.job_id)
    closeDB()
    logger.info("scan_complete", state=state)


if __name__ == "__main__":
    main()
