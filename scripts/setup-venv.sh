#!/usr/bin/env bash
# Create a local venv and install asprom Python dependencies.
#
# Debian/Ubuntu (PEP 668): use a venv; mysqlclient also needs MySQL client dev headers.
#
# Usage:
#   ./scripts/setup-venv.sh
#   source venv/bin/activate
#   ./scripts/dev-prod.sh

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

PYTHON="${PYTHON:-}"
if [ -z "$PYTHON" ]; then
  for candidate in python3.12 python3.11 python3; do
    if command -v "$candidate" >/dev/null 2>&1; then
      PYTHON="$candidate"
      break
    fi
  done
fi

if [ -z "$PYTHON" ]; then
  echo "error: no python3 interpreter found" >&2
  exit 1
fi

if ! "$PYTHON" -c "import sys; sys.exit(0 if sys.version_info >= (3, 10) else 1)"; then
  echo "error: $PYTHON must be Python 3.10 or newer" >&2
  exit 1
fi

missing_pkgs=()
for pkg in default-libmysqlclient-dev pkg-config build-essential; do
  if ! dpkg -s "$pkg" >/dev/null 2>&1; then
    missing_pkgs+=("$pkg")
  fi
done

if [ "${#missing_pkgs[@]}" -gt 0 ]; then
  echo "Missing system packages required to build mysqlclient:" >&2
  printf '  %s\n' "${missing_pkgs[@]}" >&2
  echo >&2
  echo "Install on Debian/Ubuntu:" >&2
  echo "  sudo apt install -y python3-venv ${missing_pkgs[*]} nmap" >&2
  exit 1
fi

if [ ! -d venv ]; then
  echo "Creating venv with $PYTHON ..."
  "$PYTHON" -m venv venv
fi

echo "Installing Python dependencies into venv ..."
venv/bin/pip install --upgrade pip
venv/bin/pip install -r requirements.txt

echo
echo "Done. Activate the venv with:"
echo "  source venv/bin/activate"
echo
echo "Then run:"
echo "  ./scripts/dev-prod.sh"
