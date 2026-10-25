#!/usr/bin/env bash
set -euo pipefail
DEMO_ROOT=$(cd "$(dirname "$0")/.." && pwd)
CLI_SOURCE="$DEMO_ROOT/vendor/apiops-cli"
DEMO_COMMIT=129fb326e6878c2bedd45e8ae4ccb8526de688a4
command -v node >/dev/null
node -e 'if(Number(process.versions.node.split(".")[0]) < 22) process.exit(1)'
mkdir -p "$DEMO_ROOT/vendor"
if [[ ! -d "$CLI_SOURCE/.git" ]]; then
  git init "$CLI_SOURCE"
  git -C "$CLI_SOURCE" remote add origin https://github.com/Azure/apiops-cli.git
fi
git -C "$CLI_SOURCE" fetch --depth 1 origin "$DEMO_COMMIT"
git -C "$CLI_SOURCE" checkout --detach "$DEMO_COMMIT"
cd "$CLI_SOURCE"
npm ci --ignore-scripts --cache "$DEMO_ROOT/.npm-cache"
npm run build
node dist/cli/index.js --version
