#!/usr/bin/env bash
set -euo pipefail
DEMO_ROOT=$(cd "$(dirname "$0")/.." && pwd)
CLI_FILE=${APIOPS_CLI:-"$DEMO_ROOT/vendor/apiops-cli/dist/cli/index.js"}
if [[ ! -f "$CLI_FILE" ]]; then
  echo 'Run bash scripts/install.sh first, or set APIOPS_CLI to the built CLI entry point.' >&2
  exit 2
fi
cd "$DEMO_ROOT"
exec node "$CLI_FILE" "$@"
