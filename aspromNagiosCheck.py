"""
Created on Oct 23, 2014

@author stefankn
@namespace asprom.aspromNagiosCheck
This file is invoked from the CLI and can be directly used as a nagios plugin.
"""

import sys

from inc.asprom import AspromModel, Cfg, closeDB, genMessages, initDB
from inc.logging import configure_logging, get_logger

configure_logging()
logger = get_logger(__name__)


def main():
    exitstate = 0
    msg = ""

    localconf = Cfg()
    initDB(localconf)
    model = AspromModel()

    message_crit_exposed, message_warn_exposed = genMessages(model.getAlertsExposed())
    message_crit_closed, message_warn_closed = genMessages(model.getAlertsClosed())

    closeDB()

    if len(message_crit_exposed):
        msg += "CRITICAL-EXPOSED: " + " | ".join(message_crit_exposed) + "\n"
        exitstate = 2
    if len(message_crit_closed):
        msg += "CRITICAL-CLOSED: " + " | ".join(message_crit_closed) + "\n"
        exitstate = 2
    if len(message_warn_exposed):
        msg += "WARNING-EXPOSED: " + " | ".join(message_warn_exposed) + "\n"
        exitstate = exitstate or 1
    if len(message_warn_closed):
        msg += "WARNING-CLOSED: " + " | ".join(message_warn_closed) + "\n"
        exitstate = exitstate or 1

    if not exitstate:
        msg = "all Profiles nominal."

    msg += "Profiling URL: " + localconf["misc"]["url"]

    logger.info("nagios_check_complete", exitstate=exitstate, message=msg)
    sys.exit(exitstate)


if __name__ == "__main__":
    main()
