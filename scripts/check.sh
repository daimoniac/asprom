#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "$0")/.."

ruff check .
ruff format --check .

RUN_MYPY="${ASPROM_RUN_MYPY:-0}"
if [ "$RUN_MYPY" = "1" ]; then
  mypy inc/
fi

if [ -d tests ] && [ -n "$(find tests -name 'test_*.py' -print -quit 2>/dev/null)" ]; then
  COV_ARGS=(--cov=inc --cov-report=term-missing)
  if [ -n "${ASPROM_COV_FAIL_UNDER:-}" ]; then
    COV_ARGS+=(--cov-fail-under="${ASPROM_COV_FAIL_UNDER}")
  fi
  pytest "${COV_ARGS[@]}"
else
  echo "No tests yet — skipping pytest"
fi
