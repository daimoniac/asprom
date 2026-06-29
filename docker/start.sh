#!/bin/bash
if [ "${ASPROM_RUN_MIGRATIONS:-}" = "1" ]; then
  alembic upgrade head
fi
cron
python3 aspromGUI.py
