#!/usr/bin/env bash
# Run aspromGUI locally against the production MySQL database in Kubernetes.
#
# Discovers the MySQL service name via kubectl, port-forwards it to localhost,
# and starts the Bottle GUI pointed at the forwarded connection.
#
# Prerequisites:
#   - kubectl configured with access to the target cluster
#   - Python deps installed (pip install -r requirements.txt)
#
# Usage:
#   ./scripts/dev-prod.sh
#
# Override defaults:
#   KUBE_CONTEXT=internal1 KUBE_NAMESPACE=asprom LOCAL_MYSQL_PORT=3307 ./scripts/dev-prod.sh
#
# WARNING: You are connecting to the production database. Scans, baseline
# changes, and deletions affect live data.

set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

KUBE_CONTEXT="${KUBE_CONTEXT:-internal1}"
KUBE_NAMESPACE="${KUBE_NAMESPACE:-asprom}"
LOCAL_MYSQL_PORT="${LOCAL_MYSQL_PORT:-3307}"
GUI_PORT="${GUI_PORT:-8080}"
MYSQL_SERVICE="${MYSQL_SERVICE:-}"
DB_USER="${ASPROM_DB_USER:-asprom}"
DB_NAME="${ASPROM_DB_NAME:-asprom}"
DB_PASSWORD="${ASPROM_DB_PASSWORD:-}"

PF_PID=""
TMP_CFG=""
cleanup() {
  if [ -n "$PF_PID" ] && kill -0 "$PF_PID" 2>/dev/null; then
    kill "$PF_PID" 2>/dev/null || true
    wait "$PF_PID" 2>/dev/null || true
  fi
  if [ -n "$TMP_CFG" ] && [ -f "$TMP_CFG" ]; then
    rm -f "$TMP_CFG"
  fi
}
trap cleanup EXIT INT TERM

require_cmd() {
  if ! command -v "$1" >/dev/null 2>&1; then
    echo "error: required command not found: $1" >&2
    exit 1
  fi
}

kubectl_ctx() {
  kubectl --context "$KUBE_CONTEXT" -n "$KUBE_NAMESPACE" "$@"
}

discover_mysql_service() {
  if [ -n "$MYSQL_SERVICE" ]; then
    echo "$MYSQL_SERVICE"
    return
  fi

  if kubectl_ctx get svc mysql >/dev/null 2>&1; then
    echo mysql
    return
  fi

  local mysql_named
  mysql_named="$(kubectl_ctx get svc -o jsonpath='{range .items[*]}{.metadata.name}{"\n"}{end}' \
    | grep -i mysql | head -1 || true)"
  if [ -n "$mysql_named" ]; then
    echo "$mysql_named"
    return
  fi

  local port_match
  port_match="$(kubectl_ctx get svc -o json \
    | python3 -c "
import json, sys
data = json.load(sys.stdin)
matches = []
for item in data.get('items', []):
    for port in item.get('spec', {}).get('ports', []):
        if port.get('port') == 3306:
            matches.append(item['metadata']['name'])
if len(matches) == 1:
    print(matches[0])
elif len(matches) > 1:
    print('MULTIPLE:' + ','.join(matches), file=sys.stderr)
    sys.exit(2)
")"

  if [ -n "$port_match" ]; then
    echo "$port_match"
    return
  fi

  echo "error: could not discover a MySQL service in context=$KUBE_CONTEXT namespace=$KUBE_NAMESPACE" >&2
  echo "Services in namespace:" >&2
  kubectl_ctx get svc >&2 || true
  echo "Set MYSQL_SERVICE explicitly, e.g. MYSQL_SERVICE=mysql ./scripts/dev-prod.sh" >&2
  exit 1
}

discover_mysql_port() {
  local svc="$1"
  kubectl_ctx get svc "$svc" -o jsonpath='{.spec.ports[?(@.port==3306)].port}'
}

discover_db_password() {
  if [ -n "$DB_PASSWORD" ]; then
    echo "$DB_PASSWORD"
    return
  fi

  local secret_keys secret_name value
  for secret_name in mysql asprom-mysql asprom; do
    if ! kubectl_ctx get secret "$secret_name" >/dev/null 2>&1; then
      continue
    fi
    for secret_keys in password mysql-password MYSQL_PASSWORD; do
      value="$(kubectl_ctx get secret "$secret_name" -o "jsonpath={.data.${secret_keys}}" 2>/dev/null || true)"
      if [ -n "$value" ]; then
        echo "$value" | base64 -d
        return
      fi
    done
  done

  value="$(kubectl_ctx get deploy -o json \
    | python3 -c "
import base64, json, sys
data = json.load(sys.stdin)
keys = ('MYSQL_PASSWORD', 'DB_PASSWORD', 'password')
for item in data.get('items', []):
    for container in item.get('spec', {}).get('template', {}).get('spec', {}).get('containers', []):
        for env in container.get('env', []):
            name = env.get('name', '')
            if name in keys and env.get('value'):
                print(env['value'])
                sys.exit(0)
            ref = env.get('valueFrom', {}).get('secretKeyRef', {})
            if ref.get('key') in keys:
                print(f\"SECRET:{ref.get('name')}:{ref.get('key')}\")
                sys.exit(0)
" 2>/dev/null || true)"

  if [[ "$value" == SECRET:* ]]; then
    IFS=: read -r _ secret_name secret_key <<<"$value"
    value="$(kubectl_ctx get secret "$secret_name" -o "jsonpath={.data.${secret_key}}" | base64 -d)"
    echo "$value"
    return
  fi

  if [ -n "$value" ]; then
    echo "$value"
    return
  fi

  echo "error: could not discover database password; set ASPROM_DB_PASSWORD" >&2
  exit 1
}

write_local_config() {
  local port="$1"
  TMP_CFG="$(mktemp "${TMPDIR:-/tmp}/asprom-prod-local.XXXXXX.cfg")"
  cat >"$TMP_CFG" <<EOF
db: {
  'host': '127.0.0.1'
  'port': ${port}
  'user': '${DB_USER}'
  'passwd': '${DB_PASSWORD}'
  'db': '${DB_NAME}'
}
server: {
  'listen': '127.0.0.1'
  'port': ${GUI_PORT}
  'debug': True
}
misc: {
  'url': 'http://127.0.0.1:${GUI_PORT}'
}
EOF
  export ASPROM_CFG="$TMP_CFG"
}

wait_for_mysql() {
  local port="$1"
  python3 - "$port" <<'PY'
import socket
import sys
import time

port = int(sys.argv[1])
for _ in range(30):
    with socket.socket() as sock:
        sock.settimeout(1)
        try:
            sock.connect(("127.0.0.1", port))
            sys.exit(0)
        except OSError:
            time.sleep(0.5)
print("error: timed out waiting for port-forward on 127.0.0.1:%s" % port, file=sys.stderr)
sys.exit(1)
PY
}

main() {
  require_cmd kubectl
  require_cmd python3

  echo "Discovering MySQL service (context=$KUBE_CONTEXT, namespace=$KUBE_NAMESPACE)..."
  MYSQL_SERVICE="$(discover_mysql_service)"
  REMOTE_PORT="$(discover_mysql_port "$MYSQL_SERVICE")"
  if [ -z "$REMOTE_PORT" ]; then
    REMOTE_PORT=3306
  fi

  DB_PASSWORD="$(discover_db_password)"

  echo "MySQL service: $MYSQL_SERVICE (remote port $REMOTE_PORT -> localhost:$LOCAL_MYSQL_PORT)"
  echo "Database: $DB_USER@127.0.0.1:$LOCAL_MYSQL_PORT/$DB_NAME"
  echo
  echo "WARNING: connected to production data. Press Ctrl+C to stop."
  echo

  kubectl_ctx port-forward "svc/$MYSQL_SERVICE" "${LOCAL_MYSQL_PORT}:${REMOTE_PORT}" >/dev/null &
  PF_PID=$!

  wait_for_mysql "$LOCAL_MYSQL_PORT"
  write_local_config "$LOCAL_MYSQL_PORT"

  exec python3 aspromGUI.py
}

main "$@"
